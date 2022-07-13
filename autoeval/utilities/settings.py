from pathlib import Path


def init():
    """
    Initialize all the settings/variables used in the program.
    """
    # Available splits
    global split_dict
    split_dict = {
        'aav_1': 'des_mut',
        'aav_2': 'mut_des',
        'aav_3': 'one_vs_many',
        'aav_4': 'two_vs_many',
        'aav_5': 'seven_vs_many',
        'aav_6': 'low_vs_high',
        'aav_7': 'sampled',
        'meltome_1' : 'mixed_split',
        'meltome_2' : 'human',
        'meltome_3' : 'human_cell',
        'gb1_1': 'one_vs_rest',
        'gb1_2': 'two_vs_rest',
        'gb1_3': 'three_vs_rest',
        'gb1_4': 'low_vs_high',
        'gb1_5': 'sampled',
        'scl_1': 'mixed_soft',
        'scl_2': 'mixed_hard',
        'scl_3': 'human_soft',
        'scl_4': 'human_hard',
        'scl_5': 'balanced',
        'scl_6': 'mixed_vs_human_2',
        'bind_1': 'one_vs_many',
        'bind_2': 'two_vs_many',
        'bind_3': 'from_publication',
        'bind_4': 'one_vs_sm',
        'bind_5': 'one_vs_mn',
        'bind_6': 'one_vs_sn',
        'sav_1': 'mixed',
        'sav_2': 'human',
        'sav_3': 'only_savs',  
        'secondary_structure': 'sampled',
        'conservation': 'sampled'
    }

    # Available protocols
    global protocols
    protocols = ['residue_to_class', 'sequence_to_class', 'sequence_to_value', 'residue_to_value']

    # Path to the configurations bank
    global configs_bank
    configs_bank = Path('') / '..' / 'configsbank'

    # Path to the splits
    global splits
    splits = Path('') / '..' / 'FLIP' / 'splits'