# AutoEval

This repository contains the AutoEval module, which allows to auto evaluate FLIP datasets using [bio-trainer](https://github.com/sacdallago/biotrainer) to train the models and [bio-embeddings](https://github.com/sacdallago/bio_embeddings) to embed the proteins.

Together with the scripts, this repository also contains a bank of optimal or base configurations (in the `configsbank` folder) for each of the available datasets in FLIP. These configuration files are general versions for each dataset and they are modified by the script. The expected to be usually changed parameters (embedder_name and model_choice) can be changed using input parameters. A different configuration file can be used using the input parameters, as explained below.

## How to run AutoEval

AutoEval can be executed:

- via Poetry:
```bash
# Make sure you have poetry installed
curl -sSL https://install.python-poetry.org/ | python3 - --version 1.1.13

# Install dependencies and AutoEval via poetry
poetry install

# Run
poetry run python3 run-autoeval.py split_abbreviation protocol /path/to/working_directory [--embedder embedder_name] [--model model_name] [--config config_name]
```

Example:
```bash
poetry run python3 scl_1 residue_to_class ./scl_1 --embedder prottrans_t5_xl_u50 --model CNN
```

- via Command Line:

```bash
python run-autoeval.py split_abbreviation protocol /path/to/working_directory [--embedder embedder_name] [--embeddingsfile embeddings_path] \
    [--model model_name] [--config config_name] \
    [--minsize min_size] [--maxsize max_size]
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
| `-f` / `--embeddingsfile` | To indicate the path to the file containing precomputed embeddings. |
| `-m` / `--model` | To indicate the model to use if different fro the one in the config file. It houls be one form [the ones available in bio-trainer](https://github.com/sacdallago/biotrainer/tree/main/biotrainer/models) |
| `-c` / `--config` | Config file different from the provided one in configsbank for the indicated `split`. |
| `-mins` / `--minsize` | Use proteins with more than minsize residues. |
| `-maxs` / `--maxsize` | Use proteins with less than maxsize residues. |

## Recommended configurations per dataset

| Dataset | Type of task | Recommended pLM Embeddings | Recommended model | Reference | Available in Configsbank |
| --- | :---: | :---: | :---: | :---: | :---: |
| `AAV` | ? | ? | ? | ? | ❌ |
| `GB1` | ? | ? | ? | ? | ❌ |
| `Meltome` | ? | ? | ? | ? | ❌ |
| `SCL` | sequence_to_class | ProtT5 (ProtT5-XL-UniRef50) | Light attention | [[Stärk 2021](https://doi.org/10.1093/bioadv/vbab035)] | ⚠️ |
| `Bind` | residue_to_class | ProtT5 (ProtT5-XL-UniRef50) | CNN | [[Littmann 2021](https://doi.org/10.1038/s41598-021-03431-4)] | ✅ |
| `SAV` | residue_to_class | ProtT5 (ProtT5-XL-U50) | CNN | [[Marquet 2021](https://doi.org/10.1007/s00439-021-02411-y)] | ✅ |
| `Secondary Structure` | residue_to_class | ProtT5 (ProtT5-XL-U50) | CNN | - | ⚠️ |
| `Conservation` | residue_to_class | ProtT5 (ProtT5-XL-U50) | CNN | [[Marquet 2021](https://doi.org/10.1007/s00439-021-02411-y)] | ✅ |

Availability semaphore:
- ✅: Available in configsbank in the closest possible way to the better configuration in the reference.
- ⚠️: The best configuration is not possible due to, e.g., a lack of features (temporarily) in biotrainer. The best possible alternative is the one available.
- ❌: Not available in configsbank. Somecases can be used anyhow under user's responsability.


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