# AutoEval

This repository contains the AutoEval module, which allows to auto evaluate FLIP datasets using [bio-trainer](https://github.com/sacdallago/biotrainer) to train the models and [bio-embeddings](https://github.com/sacdallago/bio_embeddings) to embed the proteins.

Together with the scripts, this repository also contains a bank of optimal or base configurations (in the `configsbank` folder) for each of the available datasets in FLIP. These configuration files are general versions for each dataset and they are modified by the script. The expected to be usually changed parameters (embedder_name and model_choice) can be changed using input parameters. A different configuration file can be used using the input parameters, as explained below.

## How to run AutoEval

AutoEval can be executed:

- via Command Line:

```bash
python run-autoeval.py split_abbreviation protocol /path/to/working_directory [--embedder embedder_name] [--model model_name] [--config config_name]
```

Example:
```bash
python run-autoeval.py scl_1 residue_to_class ./scl_1 --embedder prottrans_t5_xl_u50 --model CNN
```

- via Docker:

```bash
?
```

The available input parameters are:

| Parameter | Usage |
| --- | --- |
| `split` | Name of the split. It should be indicated using the abbreviations in the table below. |
| `protocol` | Protocol to use from [the available ones in bio-trainer](https://github.com/sacdallago/biotrainer/blob/main/README.md). |
| `working_dir` | Path to the folder to save the required files and results. |
| `-e` / `--embedder` | To indicate the embedder to use if different from the one in the config file. It should be one from [the ones available in bio-embeddings](https://docs.bioembeddings.com/v0.2.3/api/bio_embeddings.embed.html). |
| `-m` / `--model` | To indicate the model to use if different fro the one in the config file. It houls be one form [the ones available in bio-trainer](https://github.com/sacdallago/biotrainer/tree/main/biotrainer/models) |
| `-c` / `--config` | Config file different from the provided one in configsbank for the indicated `split`. |

## Recommended configurations per dataset

| Dataset | Recommended pLM Embeddings | Recommended Model | Available in Configsbank |
| --- | :---: | :---: | :---: |
| `AAV` | ? | ? | ❌ |
| `GB1` | ? | ? | ❌ |
| `Meltome` | ? | ? | ❌ |
| `SCL` | ProtT5 | Light attention | ❌ |
| `Bind` | ? | ? | ❌ |
| `SAV` | ? | ? | ❌ |
| `Secondary Structure` | ? | ? | ❌ |
| `Conservation` | ? | ? | ❌ |

## Available splits

| Dataset | Split | Abbreviation | Split | Abbreviation | 
| --- | --- | --- | --- | --- |
| `AAV` | `des_mut` | aav_1 | `mut_des` | aav_2 |
|  | `one_vs_many` | aav_3 | `two_vs_many` | aav_4 |
|  | `seven_vs_many` | aav_5 | `low_vs_high` | aav_6 |
|  | `sampled` | aav_7 |  |  |
| `Meltome` | `mixed_split` | meltome_1 | `human` | meltome_2 |
|  | `human_cell` | meltome_3 |  |  |
| `GB1` | `one_vs_rest` | gb_1 | `two_vs_rest` | gb_2 |
|  | `three_vs_rest` | gb_3 | `low_vs_high` | gb_4 |
|  | `sampled` | gb_5 |  |  |
| `SCL` | `mixed_soft` | scl_1 | `mixed_hard` | scl_2 |
|  | `human_soft` | scl_3 | `human_hard` | scl_4 |
|  | `balanced` | scl_5 | `mixed_vs_human_2` | scl_6 |
| `Bind` | `one_vs_many` | bind_1 | `two_vs_many` | bind_2 |
|  | `from_publication` | bind_3 | `one_vs_sm` | bind_4 |
|  | `one_vs_mn` | bind_5 | `one_vs_sn` | bind_6 |
| `SAV` | `mixed` | sav_1 | `human` | sav_2 |
|  | `only_savs` | sav_3 |  |  |
| `Secondary Structure` | `sampled` | secondary_structure |  |  |
| `Conservation` | `sampled` | conservation |  |  |