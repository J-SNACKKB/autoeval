import os
from pathlib import Path


global split_dict
split_dict = {
    # split_abbreviation: [dataset_folder_name, split_name]
    'aav_1': ['aav', 'des_mut'],
    'aav_2': ['aav', 'mut_des'],
    'aav_3': ['aav', 'one_vs_many'],
    'aav_4': ['aav', 'two_vs_many'],
    'aav_5': ['aav', 'seven_vs_many'],
    'aav_6': ['aav', 'low_vs_high'],
    'aav_7': ['aav', 'sampled'],
    'meltome_1' : ['meltome', 'mixed_split'],
    'meltome_2' : ['meltome', 'human'],
    'meltome_3' : ['meltome', 'human_cell'],
    'gb1_1': ['gb1', 'one_vs_rest'],
    'gb1_2': ['gb1', 'two_vs_rest'],
    'gb1_3': ['gb1', 'three_vs_rest'],
    'gb1_4': ['gb1', 'low_vs_high'],
    'gb1_5': ['gb1', 'sampled'],
    'scl_1': ['scl', 'mixed_soft'],
    'scl_2': ['scl', 'mixed_hard'],
    'scl_3': ['scl', 'human_soft'],
    'scl_4': ['scl', 'human_hard'],
    'scl_5': ['scl', 'balanced'],
    'scl_6': ['scl', 'mixed_vs_human_2'],
    'bind_1': ['bind', 'one_vs_many'],
    'bind_2': ['bind', 'two_vs_many'],
    'bind_3': ['bind', 'from_publication'],
    'bind_4': ['bind', 'one_vs_sm'],
    'bind_5': ['bind', 'one_vs_mn'],
    'bind_6': ['bind', 'one_vs_sn'],
    'sav_1': ['sav', 'mixed'],
    'sav_2': ['sav', 'human'],
    'sav_3': ['sav', 'only_savs'],  
    'secondary_structure': ['secondary_structure', 'sampled'],
    'conservation': ['secondary_structure', 'sampled']
}

# Available protocols
global protocols
protocols = ['residue_to_class', 'sequence_to_class', 'sequence_to_value', 'residue_to_value']

# Path to the configurations bank
global configs_bank
configs_bank = (Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'configsbank').resolve()

# Path to the splits
global splits
splits = (Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'FLIP' / 'splits').resolve()