import argparse
import logging

from .executer import execute
from .settings import split_dict, protocols


def create_parser():
    """
    Creates the parser for the command line interface. The included arguments are:
    - split: the name of the split to use (from the available ones in FLIP). 
        Mandatory in order to select the correct configuration file, even if one has been selected using -c.

    - protocol: the name of the protocol to use (from the available ones in biotrainer). 
        Allows to change the specified one in the config file.

    - working_dir: the path to the folder where the needed files and results will be saved.

    - -e or --embedder: the name of the embedder to use (from the available ones in bio-embeddings).
        Allows to change the specified one in the config file.

    - -f or --embeddingsfile: the path to the file containing the embeddings.
        Allows to use precomputed embeddings.

    - -mask or --mask: if set, use the masks in the file mask.fasta from the working directory to filter the residues
    
    - -m or --model: the name of the model to use (from the available ones in biotrainer).
        Allows to change the specified one in the config file.
    
    - -c or --config: the path to the configuration file to use.
        If not provided, the default one for the split in configsbank will be used.

    - -mins or --minsize: the minimum size of the proteins to use.
    
    - -maxs or --maxsize: the maximum size of the proteins to use.
    """
    
    parser = argparse.ArgumentParser(description="Train and evaluate different bioembedding models using biotrainer.")
    parser.add_argument("split", choices = split_dict.keys(), type=str, help="The split to train and evaluate. Options: {}.".format(split_dict.keys()))
    parser.add_argument("protocol", choices=protocols, type=str, help="The protocol to use.")
    parser.add_argument("working_dir", type=str, help="The path to the folder to save the needed files and results.")
    parser.add_argument("-e", "--embedder", type=str, help="The embedder to use.")
    parser.add_argument("-f", "--embeddingsfile", type=str, help="The path to the file containing the embeddings.")
    parser.add_argument("-mask", "--mask", action='store_true', help="If set, use the masks in the file mask.fasta from the working directory to filter the residues")
    parser.add_argument("-m", "--model", type=str, help="The model to use.")
    parser.add_argument("-c", "--config", help="Config file different from the provided one in configsbank.", type=str, default=None)
    parser.add_argument("-mins", "--minsize", help="Use proteins with more than minsize residues.", type=int, default=None)
    parser.add_argument("-maxs", "--maxsize", help="Use proteins with less than maxsize residues.", type=int, default=None)

    return parser

def main(args=None):
    """
    Entry point to AutoEval
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.captureWarnings(True)

    # Create parser and catch arguments
    parser = create_parser()
    arguments = parser.parse_args()

    execute(arguments)
    
if __name__ == '__main__':
    main()