import argparse
import os
import logging
from tqdm import tqdm

import torch
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

    # Load ESM-2 model
    logger.info("Loading model from {}.".format(arguments.model_location))
    model_data = torch.load(arguments.model_location)
    model, alphabet, model_state = esm.pretrained._load_model_and_alphabet_core_v2(model_data)
    model = model.to(device)

    batch_converter = alphabet.get_batch_converter()
    model.eval() # Disables dropout for deterministic results

    # Get and prepare data
    logger.info("Loading data from {}.".format(arguments.data_location))
    data = get_data(arguments.data_location)
    batch_labels, batch_strs, batch_tokens = batch_converter(data)

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