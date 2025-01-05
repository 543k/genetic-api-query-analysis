from Bio.Seq import Seq
import requests
import re

#Retrieve ensembl id for MC1R gene
myGeneServer = 'https://mygene.info/v3'
endpoint = '/query?q=MC1R&fields=ensembl.gene&species=human&size=1'
myGeneR = requests.get(myGeneServer+endpoint)
myGeneR = myGeneR.json()

if 'hits' in myGeneR:
    ensemblID = myGeneR['hits'][0]['ensembl']['gene']
else:
    print("Error finding gene ensembl ID.")
    quit()

#Retrieve nucleotide sequence associated to ensembl id
jsonHeader = {'Content-Type': 'application/json'}
myEnsemblServer = 'https://rest.ensembl.org'
endpoint = '/sequence/id/'+ensemblID+'?'
myEnsemblR = requests.get(myEnsemblServer+endpoint, headers = jsonHeader)
myEnsemblR = myEnsemblR.json()

if 'seq' in myEnsemblR:
    geneSequence = myEnsemblR['seq']
else:
    print("Error retrieving gene sequence.")
    quit()

#Find longest ORF in geneSequence and convert into an amino acid sequence
#Function taken from https://stackoverflow.com/questions/31757876/python-find-longest-orf-in-dna-sequence, based on https://pythonforbiologists.com/tutorial/regex.html
longestOrf = max(re.findall(r'ATG(?:(?!TAA|TAG|TGA)...)*(?:TAA|TAG|TGA)',geneSequence), key = len)
aminoSequence = Seq(longestOrf).translate()

#Find homologies for the ensembl id, and make unique list of the species excluding homo_sapiens
endpoint = '/homology/id/human/'+ensemblID
myEnsemblR = requests.get(myEnsemblServer+endpoint, headers = jsonHeader)
myEnsemblR = myEnsemblR.json()

speciesList = []
if 'data' in myEnsemblR:
    homologies = myEnsemblR['data'][0]['homologies']
    for homolog in homologies:
        if homolog['target']['species'] != 'homo_sapiens' and homolog['target']['species'] not in speciesList:
            speciesList.append(homolog['target']['species'])
else:
    print("Error retrieving homologies.")
    quit()

#Create FASTA file and write geneSequence and aminoSequence with respective headers
fastaFile = 'MC1R.fasta'
with open(fastaFile,'w') as file:
    file.write('>MC1R|'+ensemblID+'\n')
    file.write(geneSequence+'\n')
    file.write('>MC1R|'+ensemblID+'|LongestOrf\n')
    file.write(str(aminoSequence))

#Create TXT file of species homologies from speciesList
homologyFile = 'mc1r_homology_list.txt'
with open(homologyFile,'w') as file:
    listString = '\n'.join(speciesList)
    file.write(listString)
