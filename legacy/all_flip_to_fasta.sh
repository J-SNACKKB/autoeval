# AAV
echo "Converting AAV..."
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file mut_des.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file des_mut.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file one_vs_many.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file two_vs_many.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file seven_vs_many.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file low_vs_high.csv --output_location ./all_fasta/aav
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/aav/splits/ --split_file sampled.csv --output_location ./all_fasta/aav

# Meltome
echo "Converting Meltome..."
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/meltome/splits/ --split_file human_cell.csv --output_location ./all_fasta/meltome
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/meltome/splits/ --split_file human.csv --output_location ./all_fasta/meltome
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/meltome/splits/ --split_file mixed_split.csv --output_location ./all_fasta/meltome

# GB1
echo "Converting GB1..."
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/gb1/splits/ --split_file one_vs_rest.csv --output_location ./all_fasta/gb1
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/gb1/splits/ --split_file two_vs_rest.csv --output_location ./all_fasta/gb1
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/gb1/splits/ --split_file three_vs_rest.csv --output_location ./all_fasta/gb1
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/gb1/splits/ --split_file low_vs_high.csv --output_location ./all_fasta/gb1
python flip_csv_to_fasta.py --protocol sequence_to_value --task_location ../autoeval/FLIP/splits/gb1/splits/ --split_file sampled.csv --output_location ./all_fasta/gb1

#SLC
echo "Converting SCL..."
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file mixed_soft.csv --output_location ./all_fasta/scl
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file mixed_hard.csv --output_location ./all_fasta/scl
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file human_soft.csv --output_location ./all_fasta/scl
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file human_hard.csv --output_location ./all_fasta/scl
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file balanced.csv --output_location ./all_fasta/scl
python flip_csv_to_fasta.py --protocol residues_to_class --task_location ../autoeval/FLIP/splits/scl/splits/ --split_file mixed_vs_human_2.csv --output_location ./all_fasta/scl

# Bind
echo "Converting Bind..."
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file one_vs_many.fasta --output_location ./all_fasta/bind
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file two_vs_many.fasta --output_location ./all_fasta/bind
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file from_publication.fasta --output_location ./all_fasta/bind
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file one_vs_mn.fasta --output_location ./all_fasta/Bind
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file one_vs_sm.fasta --output_location ./all_fasta/bind
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/bind/splits/ --split_file one_vs_sn.fasta --output_location ./all_fasta/bind

# SAV
echo "Converting SAV..."
python flip_csv_to_fasta.py --protocol sequence_to_class --task_location ../autoeval/FLIP/splits/sav/splits/ --split_file mixed.csv --output_location ./all_fasta/sav
python flip_csv_to_fasta.py --protocol sequence_to_class --task_location ../autoeval/FLIP/splits/sav/splits/ --split_file human.csv --output_location ./all_fasta/sav
python flip_csv_to_fasta.py --protocol sequence_to_class --task_location ../autoeval/FLIP/splits/sav/splits/ --split_file only_savs.csv --output_location ./all_fasta/sav

# Secondary structure
echo "Converting Secondary structure..."
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/secondary_structure/splits/ --split_file sampled.fasta --output_location ./all_fasta/secondary_structure

# Conservation
echo "Converting Conservation..."
python flip_csv_to_fasta.py --protocol residue_to_class --task_location ../autoeval/FLIP/splits/conservation/splits/ --split_file sampled.fasta --output_location ./all_fasta/conservation