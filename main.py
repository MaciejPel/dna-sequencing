# imports
import random

# configuration
random.seed(1)

# constants
N = 7
K = 3

# data storage and data init
nucleotide_types = ["A", "C", "G", "T"]
oligonucleotides = []
nucleotide = "".join(random.choices(nucleotide_types, k=N))
spectrum_graph = {}


# functions
def gen_oligonucleotides():
	for i in range(len(nucleotide)):	
		if len(nucleotide) - i >= K:
			oligonucleotides.append(nucleotide[i:i+K])
	
	original_nucleotide = oligonucleotides.pop(0)
	oligonucleotides.sort()
	oligonucleotides.insert(0, original_nucleotide)


def gen_graph():
	for k in range(1, K):
		spectrum_graph[k] = {}
		for i in range(len(oligonucleotides)):
			spectrum_graph[k][oligonucleotides[i]] = []
			for j in range(len(oligonucleotides)):
				if i == j:
					continue
				if oligonucleotides[i][-k:] == oligonucleotides[j][:k]:
					spectrum_graph[k][oligonucleotides[i]].append(oligonucleotides[j])


# initial main function
if __name__ == "__main__":
	gen_oligonucleotides()
	print(nucleotide, oligonucleotides)
	gen_graph()
	print(spectrum_graph)