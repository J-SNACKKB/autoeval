import os
import logging

import shutil
from pandas import read_csv

from ..utilities.settings import splits, split_dict

logger = logging.getLogger(__name__)


def residue_to_class_fasta(split_dir, destination_sequences_dir, destination_labels_dir):
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

def residue_to_value_fasta(split_dir, destination_sequences_dir, destination_labels_dir):
    pass # TODO: Standardization pending in biotrainer

def protein_to_class_fasta(split_dir, destination_sequences_dir):
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'

            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'], row['set'], validation))
            sequences_file.write('{}\n'.format(row['sequence']))

def protein_to_value_fasta(split_dir, destination_sequences_dir):
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'
            
            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'], row['set'], validation))
            sequences_file.write('{}\n'.format(row['sequence']))

def prepare_data(split, protocol, working_dir):
    # TODO: Add other possible input files like masks
    # Check if the sequence.fasta and labels.fasta files exists
    if os.path.exists(working_dir / 'sequence.fasta') and os.path.exists(working_dir / 'labels.fasta'):
        logger.info('Sequence and labels files already exists. Skipping data preparation.')
    else:
        destination_sequences_dir = working_dir / 'sequences.fasta'
        destination_labels_dir = working_dir / 'labels.fasta'

        # Check if the split is already in FASTA format (sequences.fasta + name_of_split.fasta (with the labels))
        if os.path.exists(splits / split.split(' ')[0] / 'splits' / 'sequences.fasta') and os.path.exists(splits / split.split('_')[0] / 'splits' / (split_dict[split] + '.fasta')):
            shutil.copyfile(splits / split.split(' ')[0] / 'splits' / 'sequences.fasta', destination_sequences_dir)
            shutil.copyfile(splits / split.split('_')[0] / 'splits' / (split_dict[split] + '.fasta'), destination_labels_dir)
        else:
            # If the split is not already in FASTA format we convert CSV to FASTA
            split_dir = splits / split.split('_')[0] / 'splits' / (split_dict[split] + '.csv')
            
            if protocol == 'residue_to_class':
                logger.info('Converting CSV to FASTA for residue to class protocol.')
                residue_to_class_fasta(split_dir, destination_sequences_dir, destination_labels_dir)
                return destination_sequences_dir, destination_labels_dir
            elif protocol == 'sequence_to_class':
                logger.info('Converting CSV to FASTA for sequence to class protocol.')
                protein_to_value_fasta(split_dir, destination_sequences_dir, destination_labels_dir)
                return destination_sequences_dir, destination_labels_dir
            elif protocol == 'sequence_to_value':
                logger.info('Converting CSV to FASTA for sequence to value protocol.')
                protein_to_class_fasta(split_dir, destination_sequences_dir)
                return destination_sequences_dir, None
            elif protocol == 'residue_to_value':
                logger.info('Converting CSV to FASTA for residue to value protocol.')
                protein_to_value_fasta(split_dir, destination_sequences_dir)
                return destination_sequences_dir, None