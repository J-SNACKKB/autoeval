import argparse
import logging

from .executer import execute
from .settings import init, split_dict, protocols


def create_parser():
    """
    Creates the parser for the command line interface. The included arguments are:
    - split: the name of the split to use (from the available ones in FLIP). 
        Mandatory in order to select the correct configuration file, even if one is specifie dusing -c.

    - protocol: the name of the protocol to use (from the available ones in biotrainer). 
        Allows to change the specified one in the config file.

    - working_dir: the path to the folder where the needed files and results will be saved.

    - -e or --embedder: the name of the embedder to use (from the available ones in bio-embeddings).
        Allows to change the specified one in the config file.
    
    - -m or --model: the name of the model to use (from the available ones in biotrainer).
        Allows to change the specified one in the config file.
    
    - -c or --config: the path to the configuration file to use.
        If not provided, the default one for the split in configsbank will be used.
    """
    
    parser = argparse.ArgumentParser(description="Train and evaluate different bioembedding models using biotrainer.")
    parser.add_argument("split", choices = split_dict.keys(), type=str, help="The split to train and evaluate. Options: {}.".format(split_dict.keys()))
    parser.add_argument("protocol", choices=protocols, type=str, help="The protocol to use. Options: residue_to_class, sequence_to_class, sequence_to_sequence.")
    parser.add_argument("working_dir", type=str, help="The path to the folder to save the needed files and results.")
    parser.add_argument("-e", "--embedder", type=str, help="The embedder to use.")
    parser.add_argument("-m", "--model", type=str, help="The model to use.")
    parser.add_argument("-c", "--config", help="Config file different from the provided one in configsbank.", type=str, default=None)

    return parser

def main():
    """
    Entry point to AutoEval
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.captureWarnings(True)

    # Initialize application settings
    init()

    # Create parser and catch arguments
    parser = create_parser()
    args = parser.parse_args()

    execute(args)
    
if __name__ == '__main__':
    main()