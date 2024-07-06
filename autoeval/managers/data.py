import os
import logging
import shutil

from pathlib import Path
from typing import List, Tuple

from ..utilities.settings import splits, split_dict
from ..utilities.FASTA import read_FASTA, overwrite_FASTA, delete_entries_FASTA

logger = logging.getLogger(__name__)


def filter_fasta_entries(fasta_entries: List[any], min_size: int, max_size: int) -> Tuple[List[any], List[any]]:
    """
    Filters FASTA entries of the dataset depending on the minimum and maximum size.

    :param fasta_entries: a list of FASTA entries
    :param min_size: minimum size of the FASTA entry
    :param max_size: maximum size of the FASTA entry
    :return: a tuple of two lists: filtered FASTA entries and filtered FASTA entry ids
    """
    ids_deleted_proteins = []

    new_fasta_entries = []
    for entry in fasta_entries:
        if (min_size is not None and len(entry.seq) > min_size) or (max_size is not None and len(entry.seq) < max_size):
            new_fasta_entries.append(entry)
        else:
            logger.info('Deleted protein {}'.format(entry.id))
            ids_deleted_proteins.append(entry.id)

    return new_fasta_entries, ids_deleted_proteins


def equilibrate_sequences(destination_sequences_dir: str, destination_labels_dir: str):
    """
    Filters sequences.fasta keeping only IDs in labels.fasta

    :param destination_sequences_dir: path to sequences.fasta
    :param destination_labels_dir: path to labels.fasta
    :return: path to the sequences.fasta file and path to the labels.fasta file.
    """
    sequences_entries = read_FASTA(destination_sequences_dir)
    labels_entries = read_FASTA(destination_labels_dir)

    sequences_ids = set([entry.id for entry in sequences_entries])
    labels_ids = set([entry.id for entry in labels_entries])

    sequence_ids_to_delete = sequences_ids.difference(labels_ids)
    delete_entries_FASTA(sequence_ids_to_delete, destination_sequences_dir)


def prepare_data(split: str, protocol: str, working_dir: Path, min_size: int, max_size: int, mask: str) -> \
        Tuple[str, str]:
    """
    Copies the data files from FLIP to the working directory depending on the selected split and protocol. 
    The data files are then filtered according to the min_size and max_size parameters.

    :param split: valid FLIP split name.
    :param protocol: valid biotrainer protocol.
    :param working_dir: path to the working directory.
    :param min_size: minimum size of the proteins to be kept.
    :param max_size: maximum size of the proteins to be kept.
    :param mask: whether to mask the sequences or not.
    :return: path to the sequences.fasta file and path to the labels.fasta file.
    """
    destination_sequences_dir = str(working_dir / 'sequences.fasta')
    destination_labels_dir = str(working_dir / 'labels.fasta')
    destination_masks_dir = str(working_dir / 'mask.fasta')

    # Check if the splits of the dataset are unzipped. If not, unzip them
    if not os.path.isdir(splits / split_dict[split][0] / 'splits'):
        logger.info('Splits of the dataset are not unzipped. Unzipping them.')
        shutil.unpack_archive(splits / split_dict[split][0] / 'splits.zip', splits / split_dict[split][0],
                              "zip")
        logger.info('Splits of the dataset unzipped.')

    # Check if the required FASTA files are available
    # sequence_to_value, sequence_to_class, residues_to_class: SPLIT_NAME.fasta
    # residue_to_class: sequences.fasta + SPLIT_NAME.fasta
    if protocol in ('sequence_to_value', 'sequence_to_class', 'residues_to_class'):
        if os.path.exists(splits / split_dict[split][0] / 'splits' / f'{split_dict[split][1]}.fasta'):
            shutil.copyfile(splits / split_dict[split][0] / 'splits' / f'{split_dict[split][1]}.fasta',
                            destination_sequences_dir)
        else:
            raise Exception(f"Required files for protocol {protocol} not available.")
        destination_labels_dir = None
    elif protocol in 'residue_to_class':
        if (not os.path.exists(splits / split_dict[split][0] / 'splits' / f'{split_dict[split][1]}.fasta')
                and not os.path.exists(splits / split_dict[split][0] / 'splits' / 'sequences.fasta')):
            raise Exception(f"Required files for protocol {protocol} not available.")

        shutil.copyfile(splits / split_dict[split][0] / 'splits' / 'sequences.fasta', destination_sequences_dir)
        shutil.copyfile(splits / split_dict[split][0] / 'splits' / (split_dict[split][1] + '.fasta'),
                        destination_labels_dir)
    else:
        raise Exception(f"Invalid protocol ({protocol}).")

    # Check whether the mask file exist and copy it, if it was requested
    if mask:
        if os.path.exists(splits / split_dict[split][0] / 'splits' / f'{mask}'):
            shutil.copyfile(splits / split_dict[split][0] / 'splits' / f'{mask}', destination_masks_dir)
        else:
            raise Exception(f"Use of a mask has been requested but file {mask} is not available.")

    # Data already in FASTA format. Let's filter by minsize and maxsize
    if min_size is not None or max_size is not None:
        logger.info('Filtering proteins by criteria: minsize = {} and maxsize = {}.'.format(min_size, max_size))

        # Filter sequence.fasta
        logger.info("Filtering proteins from sequences.fasta.")
        fasta_sequences_entries = read_FASTA(destination_sequences_dir)
        new_fasta_entries, ids_deleted_proteins = filter_fasta_entries(fasta_sequences_entries, min_size, max_size)
        overwrite_FASTA(new_fasta_entries, destination_sequences_dir)

        # Filter labels.fasta if exists
        if destination_labels_dir is not None:
            logger.info("Filtering proteins from labels.fasta.")
            # fasta_sequences_entries = read_FASTA(destination_labels_dir)
            delete_entries_FASTA(ids_deleted_proteins, destination_labels_dir)

        logger.info('Proteins filtered.')

    # Splits with labels.fasta have a sequences.fasta with all the sequences in the datasets.
    # Those not in labels.fasta must be removed from sequences.fasta.
    if destination_labels_dir is not None:
        logger.info(
            'Equilibrating sequences.fasta according to labels.fasta as needed for biotrainer protocols with '
            'labels.fasta as input.')
        equilibrate_sequences(destination_sequences_dir, destination_labels_dir)

    return destination_sequences_dir, destination_labels_dir
