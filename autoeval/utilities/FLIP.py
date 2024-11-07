from biotrainer.protocols import Protocol

FLIP_DATASETS = {
    "aav": {
        "splits": [
            "des_mut",
            "mut_des",
            "one_vs_many",
            "two_vs_many",
            "seven_vs_many",
            "low_vs_high",
            "sampled"
        ]
        ,
        "protocol": Protocol.sequence_to_value
    },
    "meltome": {
        "splits": [
            "mixed_split",
            "human",
            "human_cell"
        ]
        ,
        "protocol": Protocol.sequence_to_value
    },
    "gb1": {
        "splits": [
            "one_vs_rest",
            "two_vs_rest",
            "three_vs_rest",
            "low_vs_high",
            "sampled"
        ]
        ,
        "protocol": Protocol.sequence_to_value
    },
    "scl": {
        "splits": [
            "mixed_soft",
            "mixed_hard",
            "human_soft",
            "human_hard",
            "balanced",
            "mixed_vs_human_2"
        ]
        ,
        "protocol": Protocol.residues_to_class
    },
    "bind": {
        "splits": [
            "one_vs_many",
            "two_vs_many",
            "from_publication",
            "one_vs_sm",
            "one_vs_mn",
            "one_vs_sn"
        ]
        ,
        "protocol": Protocol.residue_to_class
    },
    "sav": {
        "splits": [
            "mixed",
            "human",
            "only_savs"
        ]
        ,
        "protocol": Protocol.sequence_to_class
    },
    "secondary_structure": {
        "splits": [
            "sampled"
        ]
        ,
        "protocol": Protocol.residue_to_class
    },
    "conservation": {
        "splits": [
            "sampled"
        ]
        ,
        "protocol": Protocol.residue_to_class
    }
}
