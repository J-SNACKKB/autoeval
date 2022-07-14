import os
from pathlib import Path

import subprocess
import logging

from .settings import configs_bank
from ..managers.data import prepare_data
from ..managers.configfiles import prepare_configfile

logger = logging.getLogger(__name__)


def execute(args):
    # Get path of the configuration file from configsbank or the provided one
    if args.config is None:
        config_file = configs_bank / (args.split + '.yml')
    else:
        config_file = Path(args.config)
    logger.info('The selected configuration file to load is in {}'.format(config_file))

    # Create and set path to the folder to place the needed files and results (working directory)
    if not os.path.isdir(args.working_dir):
        os.makedirs(args.working_dir)
    working_dir = Path(args.working_dir)
    logger.info('Needed files and results will be saved in {}'.format(working_dir))

    # Prepare the data
    sequences, labels = prepare_data(args.split, args.protocol, working_dir) 
    logger.info('Data prepared')

    # Prepare configuration file with possible modifications (in args)
    prepare_configfile(working_dir, config_file, sequences, labels, args)

    # TODO: Change execution of biotrainer
    # Run biotrainer
    logger.info('Executing biotrainer.')
    #subprocess.call(["poetry", "run", "biotrainer", "./results-{}/config.yml".format(args.split)])
    os.chdir(working_dir)
    subprocess.call(["python3", "../../../biotrainer/run-biotrainer.py", "./config.yml"])
    logger.info('Done.')

