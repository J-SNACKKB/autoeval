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
        "recommended_evaluation_metric": "spearmans-corr-coeff",
        "protocol": Protocol.sequence_to_value
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
        "recommended_evaluation_metric": "f1_score",
        "protocol": Protocol.residue_to_class
    },
    "conservation": {
        "splits": [
            "sampled"
        ]
        ,
        "recommended_evaluation_metric": "accuracy",
        "protocol": Protocol.residue_to_class
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
        "recommended_evaluation_metric": "spearmans-corr-coeff",
        "protocol": Protocol.sequence_to_value
    },
    "meltome": {
        "splits": [
            "mixed_split",
            "human",
            "human_cell"
        ]
        ,
        "recommended_evaluation_metric": "spearmans-corr-coeff",
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
        "recommended_evaluation_metric": "accuracy",
        "protocol": Protocol.residues_to_class
    },
    "sav": {
        "splits": [
            "mixed",
            "human",
            "only_savs"
        ]
        ,
        "recommended_evaluation_metric": "f1_score",
        "protocol": Protocol.sequence_to_class
    },
    "secondary_structure": {
        "splits": [
            "sampled"
        ]
        ,
        "recommended_evaluation_metric": "accuracy",
        "protocol": Protocol.residue_to_class
    },
}
