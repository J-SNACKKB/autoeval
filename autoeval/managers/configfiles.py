import logging

import yaml

import shutil

logger = logging.getLogger(__name__)


def prepare_configfile(working_dir, config_file, sequences, labels, args):
    # Create copy of the configuration file
    shutil.copyfile(config_file, working_dir / 'config.yml')
    logger.info('Configuration file copied from {} to the working directory.'.format(config_file))

    # Modify copy of the config file with correct data of the selected split and the selected embedding
    with open(working_dir / 'config.yml', 'r') as cfile:
        config = yaml.load(cfile, Loader=yaml.FullLoader)

    for item in config:
        if item == "sequence_file":
            logger.info('Modifying config file with sequence file: {}'.format(sequences))
            config["sequence_file"] = str(sequences).split('/')[-1]
        elif item == "labels_file" and labels is not None:
            logger.info('Modifying config file with labels file: {}'.format(labels))
            config["labels_file"] = str(labels).split('/')[-1]
        elif item == "embedder_name" and args.embedder is not None:
            logger.info('Config file uses {} embedder. Changed by {}'.format(item["value"], args.embedder))
            config["embedder_name"] = args.embedder
        elif item == "model_choice" and args.model is not None:
            logger = logger.info('Config file uses {} model. Changed by {}'.format(item["value"], args.model))
            config["model_choice"] = args.model

    with open(working_dir / 'config.yml', 'w') as cfile:
        yaml.dump(config, cfile)