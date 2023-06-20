import yaml
import shutil

from typing import Dict

import logging

logger = logging.getLogger(__name__)


def prepare_configfile(working_dir: str, config_file: str, sequences: str, labels: str, args: Dict[str, any]):
    """
    Copies the config file to the working directory, replaces the paths to the sequences and labels files,
    and modifies the different biotrainer input parameters as indicated in the execution arguments.

    :param working_dir: path to the working diretory where the config file will be copied to
    :param config_file: path to the config file to copy and modify
    :param sequences: path to a valid FASTA file with the sequences
    :param labels: path to a valid FASTA file with the labels
    :param args: execution arguments
    """
    
    # Create copy of the configuration file
    shutil.copyfile(config_file, working_dir / 'config.yml')
    logger.info('Configuration file copied from {} to the working directory.'.format(config_file))

    # Modify copy of the config file with correct data of the selected split and configuration
    with open(working_dir / 'config.yml', 'r') as cfile:
        config = yaml.load(cfile, Loader=yaml.FullLoader)

    # Check mutually exclusion between embedder_name and embedder_file arguments
    if args.embedder and args.embeddingsfile:
        raise Exception("embedder_name and embedder_file are mutually exclusive. Provide just one as input argument.")
    if "embedder_name" in config and "embeddings_file" in config:
        raise Exception("embedder_name and embedder_file are mutually exclusive. Provide just one in the configuration file.")

    # Modify configuration file
    if config["sequence_file"] == "None":
        logger.info('Modifying config file with sequence file: {}'.format(sequences))
        config["sequence_file"] = str(sequences).split('/')[-1]
    if labels is not None and config["labels_file"] == "None":
        logger.info('Modifying config file with labels file: {}'.format(labels))
        config["labels_file"] = str(labels).split('/')[-1]
    if args.embedder is not None:
        logger.info('Embedder changed to {}'.format(args.embedder))
        config["embedder_name"] = args.embedder
        config["embeddings_file"] = None
    if args.embeddingsfile is not None:
        logger.info('Embeddings file changed to {}'.format(args.embeddingsfile))
        config["embeddings_file"] = args.embeddingsfile
        config["embedder_name"] = None
    if args.model is not None:
        logger.info('Config file uses {} model. Changed to {}'.format(config["model_choice"], args.model))
        config["model_choice"] = args.model
    if args.mask:
        logger.info('Config file does not use a mask. Changed to use {}'.format(working_dir / "mask.fasta"))
        config["mask_file"] = "mask.fasta"

    # Keep only embedder_name or embeddings_file
    if "embedder_name" in config and config["embedder_name"] is None:
        del config["embedder_name"]
    if "embeddings_file" in config and config["embeddings_file"] is None:
        del config["embeddings_file"]

    with open(working_dir / 'config.yml', 'w') as cfile:
        yaml.dump(config, cfile)