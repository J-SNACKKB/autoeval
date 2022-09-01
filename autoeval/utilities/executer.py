import os
import subprocess
from pathlib import Path

from typing import Dict

import logging

from .settings import configs_bank, split_dict
from ..managers.data import prepare_data
from ..managers.configfiles import prepare_configfile

logger = logging.getLogger(__name__)


def execute(args: Dict[str, any]):
    """
    Main AutoEval function. It manages the entire execution.

    :param args: dictionary with the execution arguments.
    """

    # Get path of the configuration file from configsbank or the provided one
    if args.config is None:
        config_file = configs_bank / (split_dict[args.split][0] + '.yml')
    else:
        config_file = Path(args.config).resolve()
    logger.info('The selected configuration file to load is in {}.'.format(config_file))

    # Create and set path to the folder to place the needed files and results (working directory)
    working_dir = Path(args.working_dir).resolve()
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir)
    logger.info('Needed files and results will be saved in {}.'.format(working_dir))

    # Prepare the data
    sequences, labels = prepare_data(args.split, args.protocol, working_dir, args.minsize, args.maxsize, args.mask)
    logger.info('Data prepared.')

    # Prepare configuration file with possible modifications (in args)
    prepare_configfile(working_dir, config_file, sequences, labels, args)

    # Run biotrainer
    logger.info('Executing biotrainer.')
    os.chdir(working_dir)
    subprocess.call(["python3", (Path(os.path.dirname(os.path.abspath(__file__))) / '../biotrainer/run-biotrainer.py').resolve(), (Path('') / 'config.yml').resolve()])
    logger.info('Done.')

