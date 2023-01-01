import argparse
import os
import logging

import torch
from fairscale.nn.data_parallel import FullyShardedDataParallel as FSDP
from fairscale.nn.wrap import enable_wrap, wrap
import esm

from Bio import SeqIO
import numpy as np
import pandas as pd
import h5py


def create_parser():
    parser = argparse.ArgumentParser(description = "Script to systematically embedd FLIP splits")
    parser.add_argument('--model_location', type=str, required=True)
    parser.add_argument('--representation_layer', type=int, required=True)
    parser.add_argument('--data_location', type=str, required=True)
    parser.add_argument('--output_location', type=str, required=True)
    parser.add_argument('--output_file_name', type=str, required=True)
    parser.add_argument('--local_rank', type=int, required=False)
    
    return parser

def get_data(file_path):    
    if '.fasta' in file_path:
        data = list(SeqIO.parse(file_path, "fasta"))
        data = [(record.id, str(record.seq)) for record in data]
        
    elif '.csv' in file_path:
        data = pd.read_csv(file_path)
        data["id"] = ["Sequence" + str(i) for i in range(0, len(data))]
        data = data[['id', 'sequence']]
        data = list(data.itertuples(index=False, name=None))
        
    return data

if __name__ == "__main__":
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
        model, alphabet, model_state = esm.pretrained._load_model_and_alphabet_core_v2(model_data)
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
    data = get_data(arguments.data_location)
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    # Embedd data
    logger.info("Embedding proteins.")
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[arguments.representation_layer], return_contacts=False)
    token_representations = results["representations"][arguments.representation_layer].cpu().numpy()

    logger.info("Proteins embedded. Formating a final dataset")
    all_data = {}
    for i in range(0, len(data)):
        all_data[data[i][0]] = {'sequence': data[i][1], 'embeddings': token_representations[i]}

    # Save data as h5 file
    output_file = os.path.join(arguments.output_location, arguments.output_file_name)
    logger.info("Saving embeddings in the h5 file {}.".format(output_file))
    with h5py.File(output_file, "w") as output_embeddings_file:
        idx = 0
        for seq_id, values in all_data.items():
            output_embeddings_file.create_dataset(str(idx),
                                                data=np.array(values['embeddings'])[1:len(values['sequence']) + 1], 
                                                compression="gzip",
                                                chunks=True, 
                                                maxshape=(len(values['sequence']) + 1, values['embeddings'].shape[1]))
            output_embeddings_file[str(idx)].attrs["original_id"] = seq_id
            idx += 1
