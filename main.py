import random


random.seed(1)


N = 7
K = 3

nucleotide_types = ["A", "C", "G", "T"]
oligonucleotides = []
nucleotide = "".join(random.choices(nucleotide_types, k=N))


def gen_oligonucleotides():
	for i in range(len(nucleotide)):	
		if len(nucleotide) - i >= 3:
			oligonucleotides.append(nucleotide[i:i+3])
	
	original_nucleotide = oligonucleotides.pop(0)
	oligonucleotides.sort()
	oligonucleotides.insert(0, original_nucleotide)


if __name__ == "__main__":
	gen_oligonucleotides()
	print(nucleotide, oligonucleotides)