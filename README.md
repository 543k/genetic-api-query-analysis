## Query Script
#### Queries RESTful APIs to uncover species with red hair. 
#### Vivek M. - 12/03/2024
### Description
A single Python script named queryScript.py that queries the  MyGene API and Ensembl API to retrieve data on the MC1R gene.

Output:

FASTA file containing red hair gene sequence, and the longest ORF amino acid sequence.

TXT file containing species with homologous red hair genes.

How to Run:

To execute the script, navigate to the directory containing the script file (ensuring the above input files are in the same directory) and run:

pip install biopython

pip install requests

chmod +X queryScript.py

python3 queryScript.py
