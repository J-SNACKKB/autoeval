# AutoEval

This repository contains AutoEval, a module for a fast and easy evaluation of FLIP benchmarking tasks. It uses [biotrainer](https://github.com/sacdallago/biotrainer) to train the task-specific models and [bio-embeddings](https://github.com/sacdallago/bio_embeddings) or custom embedders to embed proteins.

Its way of working is as simple as

```bash
python run-autoeval.py scl_mixed_soft residues_to_class ./results --embedder prottrans_t5_xl_u50
```

where

- `scl_mixed_soft` indicates the task and the split to be evaluated,
- `residues_to_class` the protocol used for the tasks,
- `./results` the output directory,
- and `--embedder prottrans_t5_xl_u50` the embedder from [bio-embeddings](https://github.com/sacdallago/bio_embeddings) to be used

The different options are summarized below.

## Installation and running

1. Make sure you have [poetry](https://python-poetry.org/) installed: 
```bash
curl -sSL https://install.python-poetry.org/ | python3 - --version 1.4.2
```

2. Install dependencies and biotrainer via `poetry`:
```bash
# In the base directory:
poetry install
# Optional: Add bio-embeddings to compute embeddings
poetry install --extras "bio-embeddings"
# You can also install all extras at once
poetry install --all-extras
```

To run AutoEval:

- with Poetry:
```bash
# Option 1:
poetry run autoeval DATASET_SPLIT PROTOCOL WORKING_DIR [...]

# Option 2:
autoeval DATASET_SPLIT PROTOCOL WORKING_DIR [...]
```

The provieded `run-autoeval.py` can also be used.

- with Docker:

```bash
# Build
docker build -t autoeval .
# Run
docker run --rm \
    -v "$(pwd)/examples/docker":/mnt \
    -v bio_embeddings_weights_cache:/root/.cache/bio_embeddings \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    biotrainer:latest /mnt/config.yml
```


## Options


| Parameter | Usage |
| --- | --- |
| `split` | Name of the split, e.g. `aav_des_mut`. The different options are listed at the end of this file. |
| `protocol` | Task-specific training protocol to use from [the available ones in biotrainer](https://github.com/sacdallago/biotrainer/blob/main/README.md): `residue_to_class`, `residues_to_class`, `sequence_to_class` and `sequence_to_value`. |
| `working_dir` | Path to the working directory.|
| `-e` / `--embedder` | Embedder to use if different from the one in the default configuration. It can be from [the ones available in bio-embeddings](https://docs.bioembeddings.com/v0.2.3/api/bio_embeddings.embed.html), e.g. `esm1b`; or a custom embedder (see details [here](https://github.com/sacdallago/biotrainer/tree/main/examples/custom_embedder)). |
| `-f` / `--embeddingsfile` | Path to the file containing precomputed embeddings if available. |
| `-m` / `--model` | Model to use if different fro them one in the default configuration. It should be one from [the ones available in biotrainer](https://github.com/sacdallago/biotrainer/tree/main/biotrainer/models), e.g. `FNN` or `CNN`. |
| `-c` / `--config` | Config file different from the provided one in configsbank for the indicated `split`. |
| `-mins` / `--minsize` | Only use proteins the given minimum length. |
| `-maxs` / `--maxsize` | Only use proteins the given maximum length. |
| `-mask` / `--mask` | If set, use the masks in the file `mask.fasta` from the split to filter the residues. It also accepts a path to a different masks file. |

## Default configurations

For every task, the original configuration is the one used by default (defined in the `configsbank` folder). A different configuration can be used by changing the input arguments of AutoEval or by copying and changing the given one. The default can be overwritten using `--config NEW_CONFIG.yml`.

| Dataset | Type of task | Recommended pLM Embeddings | Recommended model | Reference | Available in Configsbank |
| --- | :---: | :---: | :---: | :---: | :---: |
| `AAV` | sequence_to_value | - | FNN | [[Dallago 2021](https://www.biorxiv.org/content/10.1101/2021.11.09.467890v2.abstract)] | ⚠️ |
| `GB1` | sequence_to_value | - | FNN | [[Dallago 2021](https://www.biorxiv.org/content/10.1101/2021.11.09.467890v2.abstract)] | ⚠️ |
| `Meltome` | sequence_to_value | - | FNN | [[Dallago 2021](https://www.biorxiv.org/content/10.1101/2021.11.09.467890v2.abstract)] | ⚠️ |
| `SCL` | residues_to_class | ProtT5 (ProtT5-XL-UniRef50) | LightAttention | [[Stärk 2021](https://doi.org/10.1093/bioadv/vbab035)] | ✅ |
| `Bind` | residue_to_class | ProtT5 (ProtT5-XL-UniRef50) | CNN | [[Littmann 2021](https://doi.org/10.1038/s41598-021-03431-4)] | ✅ |
| `SAV` | sequence_to_class | ProtT5 (ProtT5-XL-U50) | FNN | [[Marquet 2021](https://doi.org/10.1007/s00439-021-02411-y)] | ⚠️ |
| `Secondary Structure` | residue_to_class | ProtT5 (ProtT5-XL-U50) | CNN | - | ✅ |
| `Conservation` | residue_to_class | ProtT5 (ProtT5-XL-U50) | CNN | [[Marquet 2021](https://doi.org/10.1007/s00439-021-02411-y)] | ✅ |

Availability semaphore:
- ✅: Available in configsbank in the closest possible way to the better configuration in the reference.
- ⚠️: The best configuration is not possible due to, e.g., a lack of features in biotrainer. The best possible alternative is the one available.
- ❌: Not available in configsbank. Somecases can be used anyhow under user's responsability.


## Available splits

In order to reference the split to be evaluated the pattern `dataset_split` must be followed. For example, the split `seven_vs_many` from the dataset `aav` must be referenced as `aav_seven_vs_many`.

| Dataset | Splits |
| --- | --- |
| `AAV` (`aav_*`) | `des_mut`, `mut_des`, `one_vs_many`, `two_vs_many`, `seven_vs_many`, `low_vs_high`, `sampled`   |
| `Meltome` (`meltome_*`) | `mixed_split`, `human`, `human_cell` |
| `GB1` (`gb1_*`) | `one_vs_rest`, `two_vs_rest`, `three_vs_rest`, `low_vs_high`, `sampled` |
| `SCL` (`scl_*`) | `mixed_soft`, `mixed_hard`, `human_soft`, `human_hard`, `balanced`, `mixed_vs_human_2` |
| `Bind` (`bind_*`) | `one_vs_many`, `two_vs_many`, `from_publication`,  `one_vs_sm`, `one_vs_mn`, `one_vs_sn` |
| `SAV` (`sav_*`) | `mixed`, `human`, `only_savs` |
| `Secondary Structure` (`secondary_structure_*`) | `sampled` |
| `Conservation` (`conservation_*`) | `sampled` |
