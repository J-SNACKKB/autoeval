import os
from pathlib import Path


global split_dict
split_dict = {
    # split_abbreviation: [dataset_folder_name, split_name]
    'aav_des_mut': ['aav', 'des_mut'],
    'aav_mut_des': ['aav', 'mut_des'],
    'aav_one_vs_many': ['aav', 'one_vs_many'],
    'aav_two_vs_many': ['aav', 'two_vs_many'],
    'aav_seven_vs_many': ['aav', 'seven_vs_many'],
    'aav_low_vs_high': ['aav', 'low_vs_high'],
    'aav_sampled': ['aav', 'sampled'],
    'meltome_mixed_split' : ['meltome', 'mixed_split'],
    'meltome_human' : ['meltome', 'human'],
    'meltome_human_cell' : ['meltome', 'human_cell'],
    'gb1_one_vs_rest': ['gb1', 'one_vs_rest'],
    'gb1_two_vs_rest': ['gb1', 'two_vs_rest'],
    'gb1_three_vs_rest': ['gb1', 'three_vs_rest'],
    'gb1_low_vs_high': ['gb1', 'low_vs_high'],
    'gb1_sampled': ['gb1', 'sampled'],
    'scl_mixed_soft': ['scl', 'mixed_soft'],
    'scl_mixed_hard': ['scl', 'mixed_hard'],
    'scl_human_soft': ['scl', 'human_soft'],
    'scl_human_hard': ['scl', 'human_hard'],
    'scl_balanced': ['scl', 'balanced'],
    'scl_mixed_vs_human_2': ['scl', 'mixed_vs_human_2'],
    'bind_one_vs_many': ['bind', 'one_vs_many'],
    'bind_two_vs_many': ['bind', 'two_vs_many'],
    'bind_from_publication': ['bind', 'from_publication'],
    'bind_one_vs_sm': ['bind', 'one_vs_sm'],
    'bind_one_vs_mn': ['bind', 'one_vs_mn'],
    'bind_one_vs_sn': ['bind', 'one_vs_sn'],
    'sav_mixed': ['sav', 'mixed'],
    'sav_human': ['sav', 'human'],
    'sav_only_savs': ['sav', 'only_savs'],
    'secondary_structure_sampled': ['secondary_structure', 'sampled'],
    'conservation_sampled': ['conservation', 'sampled']
}

# Available protocols
global protocols
protocols = ['residue_to_class', 'sequence_to_class', 'sequence_to_value', 'residue_to_value', 'residues_to_class']

# Path to the configurations bank
global configs_bank
configs_bank = (Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'configsbank').resolve()

# Path to the splits
global splits
splits = (Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'FLIP' / 'splits').resolve()