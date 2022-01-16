import lightrdf
import nltk
from nltk.tokenize import word_tokenize

# 2
FILE_PATH = "./CSO.3.3.owl"
WORD = "facial_action"
CRITERION = "superTopicOf"

parser = lightrdf.Parser()

print ("In loc de spatii scrieti _")
WORD = input("Dati un cuvant: ")
with open (FILE_PATH, "rb") as r_file:
    for triple in parser.parse(r_file, format="owl", base_iri=None):
        if WORD in triple[0] and CRITERION in triple[1]:
            print (triple)

# 3
r_file = open("computer-science.txt", "r")
w_file = open("output.txt", "w")
lines = r_file.readlines()

for line in lines:
    if not line:
        continue
    line = list(line.split("."))
    for sentence in line:
        text = list(sentence.split(" "))
        pos_tags = nltk.pos_tag(text)

        nn_1_found, vb_found, nn_2_found = False, False, False

        for pos_tag in pos_tags:
            if pos_tag[1] == 'NN':
                nn_1_found = True
            elif nn_1_found and pos_tag[1] == 'VB':
                vb_found = True
            if nn_1_found and vb_found and pos_tag[1] == 'NN':
                nn_2_found = True
                break

        if nn_2_found:
            w_file.write(sentence + ".\n")

r_file.close()
w_file.close()

# 4
r_file = open("output.txt", "r")
w_file = open("output2.txt", "w")
lines = r_file.readlines()
sentences = set()
nouns = set()

for line in lines:
    pos_tags = nltk.pos_tag(list(line.split(" ")))
    for pos_tag in pos_tags:
        if pos_tag[1] == 'NN' and pos_tag[0] not in nouns:
            nouns.add(pos_tag[0])
            with open (FILE_PATH, "rb") as r_file:
                for triple in parser.parse(r_file, format="owl", base_iri=None):
                    if pos_tag[0] in triple[2] and line not in sentences:
                        sentences.add(line)
                        w_file.write(line + " ---> " + pos_tag[0] + " ---> " + triple[2] + "\n")
                        continue