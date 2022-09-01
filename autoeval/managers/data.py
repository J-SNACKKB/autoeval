import os
import logging

from typing import List, Tuple

import shutil
from pandas import read_csv

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

def equilibrate_sequences(destination_sequences_dir: str, destination_labels_dir: str) -> Tuple[str, str]:
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

def residue_to_class_fasta(split_dir: str, destination_sequences_dir: str, destination_labels_dir: str):
    """
    Converts FLIP CSV files to biotrainer FASTA files for the residue to class protocol.

    :param split_dir: path to a valid FLIP split directory
    :param destination_sequences_dir: path to the destination FASTA file for the sequences
    :param destination_labels_dir: path to the destination FASTA file for the labels
    """
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            sequences_file.write('>{}\n'.format('Sequence{}'.format(index)))
            sequences_file.write('{}\n'.format(row['sequence']))

    # Create labels.fasta
    with open(destination_labels_dir, 'w') as labels_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'
            labels_file.write('>{}\n'.format('Sequence{} SET={} VALIDATION={}'.format(index, row['set'], validation)))
            labels_file.write('{}\n'.format(row['target']))

def residue_to_value_fasta(split_dir: str, destination_sequences_dir: str, destination_labels_dir: str):
    """
    Converts FLIP CSV files to biotrainer FASTA files for the residue to class protocol.

    :param split_dir: path to a valid FLIP split directory
    :param destination_sequences_dir: path to the destination FASTA file for the sequences
    :param destination_labels_dir: path to the destination FASTA file for the labels
    """
    pass # TODO: Standardization pending in biotrainer

def protein_to_class_fasta(split_dir: str, destination_sequences_dir: str):
    """
    Converts FLIP CSV file to biotrainer FASTA file for the protein to class protocol.

    :param split_dir: path to a valid FLIP split directory
    :param destination_sequences_dir: path to the destination FASTA file for the sequences
    """
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'

            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'], row['set'], validation))
            sequences_file.write('{}\n'.format(row['sequence']))

def protein_to_value_fasta(split_dir: str, destination_sequences_dir: str):
    """
    Converts FLIP CSV file to biotrainer FASTA file for the protein to value protocol.

    :param split_dir: path to a valid FLIP split directory
    :param destination_sequences_dir: path to the destination FASTA file for the sequences
    """
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'
            
            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'], row['set'], validation))
            sequences_file.write('{}\n'.format(row['sequence']))

def prepare_data(split: str, protocol: str, working_dir: str, min_size: int, max_size: int, mask: bool) -> Tuple[str, str]:
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
    destination_sequences_dir = working_dir / 'sequences.fasta'
    destination_labels_dir = working_dir / 'labels.fasta'
    destination_masks_dir = working_dir / 'mask.fasta'

    # Check if the splits of the dataset are unzipped. If not, unzip them
    if not os.path.isdir(splits / split_dict[split][0] / 'splits'):
        logger.info('Splits of the dataset are not unzipped. Unzipping them.')
        shutil.unpack_archive(splits / split_dict[split][0] / 'splits.zip', splits / split_dict[split][0] / 'splits', "zip")
        logger.info('Splits of the dataset unzipped.')

    # Check if the split is already in FASTA format. If already in FASTA, it at least contains the sequences.fasta file
    if os.path.exists(splits / split_dict[split][0] / 'splits' / 'sequences.fasta'):
        logger.info('Split already in FASTA format. Conversion not needed. Copying files direclty.')
        shutil.copyfile(splits / split_dict[split][0] / 'splits' / 'sequences.fasta', destination_sequences_dir)
        
        if protocol == 'residue_to_class':
            shutil.copyfile(splits / split_dict[split][0] / 'splits' / (split_dict[split][1] + '.fasta'), destination_labels_dir)
        else:
            destination_labels_dir = None

        # Check if exists a mask file. If exists, copy it to the working directory
        if os.path.exists(splits / split_dict[split][0] / 'splits' / 'mask.fasta') and mask:
            shutil.copyfile(splits / split_dict[split][0] / 'splits' / 'mask.fasta', destination_masks_dir)

    else:
        # If the split is not already in FASTA format we convert CSV to FASTA
        logger.info('Split in CSV format.')

        split_dir = splits / split_dict[split][0] / 'splits' / (split_dict[split][1] + '.csv')

        if protocol == 'sequence_to_class':
            logger.info('Converting CSV to FASTA for sequence to class protocol.')
            protein_to_value_fasta(split_dir, destination_sequences_dir)
            destination_labels_dir = None
        elif protocol == 'sequence_to_value':
            logger.info('Converting CSV to FASTA for sequence to value protocol.')
            protein_to_class_fasta(split_dir, destination_sequences_dir)
            destination_labels_dir = None
        elif protocol == 'residue_to_class':
            logger.info('Converting CSV to FASTA for residue to class protocol.')
            residue_to_class_fasta(split_dir, destination_sequences_dir, destination_labels_dir)
        elif protocol == 'residue_to_value':
            logger.info('Converting CSV to FASTA for residue to value protocol.')
            # TODO: Standardization pending in biotrainer

    # Data already in FASTA format. Let's filter by minsize and maxsize
    if min_size is not None or max_size is not None:
        logger.info('Filtering proteins by citeria: minsize = {} and maxsize = {}.'.format(min_size, max_size))

        # Filter sequence.fasta
        logger.info("Filtering proteins from sequences.fasta.")
        fasta_sequences_entries = read_FASTA(destination_sequences_dir)
        new_fasta_entries, ids_deleted_proteins = filter_fasta_entries(fasta_sequences_entries, min_size, max_size)
        overwrite_FASTA(new_fasta_entries, destination_sequences_dir)

        # Flilter labels.fasta if exists
        if (destination_labels_dir is not None):
            logger.info("Filtering proteins from labels.fasta.")
            fasta_sequences_entries = read_FASTA(destination_labels_dir)
            delete_entries_FASTA(ids_deleted_proteins, destination_labels_dir)

        logger.info('Proteins filtered.')

    # Splits with labels.fasta have a sequences.fasta with all the sequences in the datasets. Those not in labes.fasta must be removed from sequences.fasta.
    if (destination_labels_dir is not None):
        logger.info('Equilibrating sequences.fasta according to labels.fasta as needed for biotrainer protocols with labels.fasta as input.')
        equilibrate_sequences(destination_sequences_dir, destination_labels_dir)

    return destination_sequences_dir, destination_labels_dir



