import argparse
import os
import shutil
from pathlib import Path

from pandas import read_csv


def create_parser():
    parser = argparse.ArgumentParser(description = "Script to systematically convert FLIP CSV data to FASTA format")
    parser.add_argument('--protocol', type=str, required=True)
    parser.add_argument('--task_location', type=str, required=True)
    parser.add_argument('--split_file', type=str, required=True)
    parser.add_argument('--output_location', type=str, required=True)
    
    return parser

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

def residues_to_class_fasta(split_dir: str, destination_sequences_dir: str):
    """
    Converts FLIP CSV file to biotrainet FASTA file for the residues to class protocol.

    :param split_dir: path to a valid FLIP split directory
    :param destination_sequences_dir: path to the destination FASTA file for the sequences
    """
    split = read_csv(split_dir)

    # Create sequences.fasta
    with open(destination_sequences_dir, 'w') as sequences_file:
        for index, row in split.iterrows():
            validation = 'True' if row['validation'] == True else 'False'

            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'].replace(' ', '_'), row['set'], validation))
            sequences_file.write('{}\n'.format(row['sequence']))

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

            sequences_file.write('>Sequence{} TARGET={} SET={} VALIDATION={}\n'.format(index, row['target'].replace(' ', '_'), row['set'], validation))
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

if __name__ == "__main__":

    parser = create_parser()
    arguments = parser.parse_args()

    # Create output directory
    if not os.path.exists(arguments.output_location):
        os.makedirs(arguments.output_location, exist_ok=True)

    # Check if the split is already in FASTA format. If already in FASTA, it at least contains the sequences.fasta file
    if os.path.exists(Path(arguments.task_location) / 'sequences.fasta'):
        #logger.info('Split already in FASTA format. Conversion not needed. Copying files direclty.')
        shutil.copyfile(Path(arguments.task_location) / 'sequences.fasta', Path(arguments.output_location) / 'sequences.fasta')
        
        if arguments.protocol == 'residue_to_class':
            shutil.copyfile(Path(arguments.task_location) / arguments.split_file, Path(arguments.output_location) / arguments.split_file)

        # Check if exists a mask file. If exists, copy it to the working directory
        if os.path.exists(Path(arguments.task_location) / 'mask.fasta'):
            shutil.copyfile(Path(arguments.task_location) / 'mask.fasta', Path(arguments.output_location) / 'mask.fasta')

    else:
        # If the split is not already in FASTA format we convert CSV to FASTA
        split_dir = Path(arguments.task_location) / arguments.split_file
        sequences_dir = Path(arguments.output_location) / arguments.split_file.replace('.csv', '.fasta')

        if arguments.protocol == 'sequence_to_class':
            protein_to_class_fasta(split_dir, sequences_dir)
        elif arguments.protocol == 'sequence_to_value':
            protein_to_value_fasta(split_dir, sequences_dir)
        elif arguments.protocol == 'residues_to_class':
            residues_to_class_fasta(split_dir, sequences_dir)
        elif arguments.protocol == 'residue_to_class':
            residue_to_class_fasta(split_dir, sequences_dir, Path(arguments.output_location) / arguments.split_file)
