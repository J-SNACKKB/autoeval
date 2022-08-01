from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from typing import List

def read_FASTA(path: str) -> List[SeqRecord]:
    """
    Helper function to read FASTA file.

    :param path: path to a valid FASTA file
    :return: a list of SeqRecord objects.
    """
    return list(SeqIO.parse(path, "fasta"))

def overwrite_FASTA(sequences: List[SeqRecord], path: str):
    """
    Helper function to overwrite FASTA file.

    :param path: path to a valid FASTA file
    :param sequences: a list of SeqRecord objects.
    """
    SeqIO.write(sequences, path, "fasta")

def delete_entries_FASTA(ids: List[str], path: str):
    """
    Helper function to delete entries from FASTA file.

    :param ids: a list of ids to delete
    :param path: path to a valid FASTA file
    """
    sequences = read_FASTA(path)
    sequences = [sequence for sequence in sequences if sequence.id not in ids]
    overwrite_FASTA(sequences, path)