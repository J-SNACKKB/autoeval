import argparse
import os
import logging
from tqdm import tqdm

import torch
from fairscale.nn.data_parallel import FullyShardedDataParallel as FSDP
from fairscale.nn.wrap import enable_wrap, wrap
import esm

from Bio import SeqIO
import numpy as np
import pandas as pd
import h5py


def create_parser():
    """
    Creates an argument parser for the script.
    """
    parser = argparse.ArgumentParser(description = "Script to systematically embedd FLIP splits")
    parser.add_argument('--model_location', type=str, required=True)
    parser.add_argument('--representation_layer', type=int, required=True)
    parser.add_argument('--data_location', type=str, required=True)
    parser.add_argument('--output_location', type=str, required=True)
    parser.add_argument('--output_file_name', type=str, required=True)
    parser.add_argument('--local_rank', type=int, required=False)
    parser.add_argument('--max_sequence_size', type=int, required=False, default=2048)
    
    return parser

def get_data(file_path: str, max_size: int = 2048):
    """
    Reads CSV or FASTA file and returns a list of tuples (id, sequence) with sequences of length <= max_size.

    Args:
        file_path (str): Path to the file to be read 
        max_size (int): Max sequence length to be considered

    Returns:
        list: List of tuples (id, sequence) with sequences of length <= max_size
    """
    if '.fasta' in file_path:
        data = list(SeqIO.parse(file_path, "fasta"))
        data = [(record.id, str(record.seq)) for record in data if len(str(record.seq)) <= max_size]
        
    elif '.csv' in file_path:
        data = pd.read_csv(file_path)
        data["length"] = data.sequence.str.len()
        data = data[data.length <= max_size]
        data["id"] = ["Sequence" + str(i) for i in range(0, len(data))]
        data = data[['id', 'sequence']]
        data = list(data.itertuples(index=False, name=None))
        
    return data

def main():
    """
    This script computes embeddings from ESM-2 and save them in a HDF5 file.
    The produced HDF5 follows the expectations of AutoEval/biotrainer.

    Usage example:
        python -m torch.distributed.launch --master_port 7771 --nproc_per_node=1 PATH_TO_SCRIPT/esm2_embedder --model_location PATH_TO_MODEL 
                                                                                                                --representation_layer 36 
                                                                                                                --data_location PATH_TO_SEQUENCES/sequences.fasta 
                                                                                                                --output_location OUTPUT_PATH 
                                                                                                                --output_file_name OUTPUT_FILENAME.h5
                                                                                                                --max_sequence_size MAX_SEQUENCE_SIZE
    """
     # Get arguments
    parser = create_parser()
    arguments = parser.parse_args()

    # Instantiate logger
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.captureWarnings(True)
    logger = logging.getLogger(__name__)

    # Select device
    logger.info("Selecting device: {}.".format("cuda" if torch.cuda.is_available() else "cpu"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Init the distributed world with world_size 1
    torch.distributed.init_process_group(backend="nccl", world_size=1, rank=0)

    # Initialize the model with FSDP wrapper
    logger.info("Loading model from {} with FSDP wrapper.".format(arguments.model_location))
    fsdp_params = dict(
        mixed_precision=True,
        flatten_parameters=True,
        state_dict_device=torch.device("cpu"),  # reduce GPU mem usage
        cpu_offload=True,  # enable cpu offloading
    )
    with enable_wrap(wrapper_cls=FSDP, **fsdp_params):
        model_data = torch.load(arguments.model_location)
        model, alphabet = esm.pretrained.load_model_and_alphabet_core(model_name=arguments.model_location.split('/')[-1].split('.')[0], model_data=model_data)
        batch_converter = alphabet.get_batch_converter()
        model.eval() # Disables dropout for deterministic results

        # Wrap each layer in FSDP separately
        for name, child in model.named_children():
            if name == "layers":
                for layer_name, layer in child.named_children():
                    wrapped_layer = wrap(layer)
                    setattr(child, layer_name, wrapped_layer)
        model = wrap(model)

    # Get and prepare data
    logger.info("Loading data from {}.".format(arguments.data_location))
    data = get_data(arguments.data_location, arguments.max_sequence_size)

    # Avoid to compute already computed embeddings
    partial = pd.DataFrame(columns=["key", "original_id", "representation"])
    data_to_compute = []
    if os.path.exists(os.path.join(arguments.output_location, arguments.output_file_name)):
        logger.info("Partial file exists. Loading data and skipping already computed embeddings.")
        
        # Look for partial results
        with h5py.File(arguments.output_location + arguments.output_file_name, "r") as f:
            for key in f.keys():
                new_row = {"key": key,
                            "original_id": f[key].attrs["original_id"],
                            "representation": f[key][()]}
                partial = pd.concat([partial, pd.DataFrame([new_row])], axis=0, ignore_index=True)

        # Remove from embeddings to compute these already computed
        already_computed = set(partial["original_id"])
        for (id, sequence) in data:
            if id not in already_computed:
                data_to_compute.append((id, sequence))
    else:
        data_to_compute = data

    batch_labels, batch_strs, batch_tokens = batch_converter(data_to_compute)
    # Instead of sending all the data to the GPU at once, we send it in batches of size 1, to avoid OOM errors
    #batch_tokens = batch_tokens.to(device)

    # Compute embeddings
    logger.info("Embedding proteins.")
    output_file = os.path.join(arguments.output_location, arguments.output_file_name)
    with h5py.File(output_file, "a") as output_embeddings_file:
        idx = len(partial)
        for label, seq, tokens in tqdm(zip(batch_labels, batch_strs, batch_tokens), total=len(batch_tokens)):
            if len(seq) <= 2048:
                with torch.no_grad():
                    results = model(torch.reshape(tokens, (1, tokens.shape[0])).to(device), repr_layers=[arguments.representation_layer])
                    representation = results["representations"][arguments.representation_layer].detach().cpu().numpy()[0]
                # Save embedding in an h5 file
                output_embeddings_file.create_dataset(str(idx),
                                                    data=representation[1:len(seq) + 1],
                                                    compression="gzip",
                                                    chunks=True)
                output_embeddings_file[str(idx)].attrs["original_id"] = label
                idx += 1

    logger.info("All the embedings have been domcputed and saved in {}.".format(output_file))

if __name__ == "__main__":
    main()