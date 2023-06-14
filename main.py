import os
import random
import Levenshtein
import pandas as pd


random.seed(0)


base_path: str = "./tests/"
debug: bool = True
nuc_types: list[str] = ["A", "C", "G", "T"]


def gen_graph(k: int, spectrum: list[str]):
	graph = {}
	for k in range(1, k):
		graph[k] = {}
		for i in range(len(spectrum)):
			graph[k][spectrum[i]] = []
			for j in range(len(spectrum)):
				if i == j:
					continue
				if spectrum[i][-k:] == spectrum[j][:k]:
					graph[k][spectrum[i]].append(spectrum[j])

	return graph


def calc_diff(s1: str, s2: str, d: int = 0):
	if s1[d:] == s2[:len(s2) - d]:
		return d

	return calc_diff(s1, s2, d + 1)


def assemble_nuc(tab: list[str]):
	s = tab[0]
	for i in range(1, len(tab)):
		addt = calc_diff(tab[i - 1], tab[i])
		s += tab[i][-addt:]

	return s


def save_to_file(dir: str, file_path: str, data: list):
	path = base_path + dir + "/"

	if not os.path.exists(path):
		os.makedirs(path)
		
	with open(path + file_path + ".txt", "w") as f:
		f.write(data[0] + "\n")
		f.write(data[1] + "\n")

		for o in data[2]:
			f.write(o + "\n")


def save_results(dir: str, result_dict: dict):
	df = pd.DataFrame.from_dict(result_dict)
	df.to_excel(base_path + "/" + dir + "/" + dir + ".xlsx", header=True, index=False)


def greedy(n: int, k: int, spectrum: list[str], init_node: str) -> list[str]:
	graph = gen_graph(k, spectrum)
	s = [init_node]
	v = s.copy()
	l = len(init_node)

	while l < n:
		f = False

		for kk in reversed(range(1, k)):
			if len(graph[kk][s[-1]]) > 0:
				for o in graph[kk][s[-1]]:
					if o not in v:
						s.append(o)
						v.append(o)
						l += k - kk
						break
				else:
					if kk == 1:
						f = True
					continue
				break

		if f:
			f = False
			v.pop(random.randrange(len(v)))

	return s


def main():
	"""
		TESTS General
	"""
	test_type = "k"
	n = 500
	err_type = 0
	err_rate = 0
	result_dict = {
		"n": [],
		"k": [],
		"er": [],
		"et": [],
		"ratio": [],
		"coverage": [],
	}
	for k in range(6, 10 + 1):
		ratios = []
		coverages = []
		for i in range(0, 10):
			init, oligos, nuc = gen_oligos(n, k)

			solution = greedy(n, k, oligos, init)
			result = Levenshtein.ratio(assemble_nuc(solution), nuc)
			ratios.append(result)
			coverages.append(len(set(solution)) / len(oligos))

			file_path = ["n" + str(n), "k" + str(k), "et" + str(err_type), "er" + str(err_rate), "i" + str(i)]
			save_to_file(test_type, "-".join(file_path), [nuc, init, oligos, result])

		result_dict["n"].append(n)
		result_dict["k"].append(k)
		result_dict["er"].append(err_rate)
		result_dict["et"].append(err_type)
		result_dict["ratio"].append(sum(ratios) / len(ratios))
		result_dict["coverage"].append(sum(coverages) / len(coverages))

	# save_results(test_type, result_dict)
	"""
		TESTS ERR
	"""
	# test_type = "er3"
	# n = 700
	# k = 6
	# err_type = 3
	# result_dict = {
	# 	"n": [],
	# 	"k": [],
	# 	"er": [],
	# 	"et": [],
	# 	"ratio": [],
	# 	"coverage": [],
	# }
	# instances = []
	# for i in range(0, 20):
	# 	instances.append(gen_oligos(n, k))

	# for err_rate in range(2, 10 + 1, 2):
	# 	ratios = []
	# 	coverages = []
	# 	for i, instance in enumerate(instances):
	# 		init, oligos, nuc = instance
	# 		oligos = add_errors(n, k, oligos, init, err_type, err_rate / 100)

	# 		try:
	# 			solution = greedy(n, k, oligos, init)
	# 		except Exception as e:
	# 			print(n,k,err_type,err_rate, nuc, init)
	# 			print(oligos)
	# 			print(gen_graph(k, oligos))
	# 			print(e)
	# 		result = Levenshtein.ratio(assemble_nuc(solution), nuc)
	# 		ratios.append(result)
	# 		coverages.append(len(set(solution)) / len(oligos))

	# 		file_path = ["n" + str(n), "k" + str(k), "et" + str(err_type), "er" + str(err_rate), "i" + str(i)]
	# 		save_to_file(test_type, "-".join(file_path), [nuc, init, oligos, result])

	# 	result_dict["n"].append(n)
	# 	result_dict["k"].append(k)
	# 	result_dict["er"].append(err_rate / 100)
	# 	result_dict["et"].append(err_type)
	# 	result_dict["ratio"].append(sum(ratios) / len(ratios))
	# 	result_dict["coverage"].append(sum(coverages) / len(coverages))

	# save_results(test_type, result_dict)


def add_errors(
	n: int, k: int, oligos: list[str], init: str, err_type: int = 0, err_rate: float = 0.05
) -> list[str]:
	ideal_length = n - k + 1
	err_amt = int(err_rate * ideal_length)

	c = 0
	if err_type == 1 or err_type == 3:
		while c < (err_amt // 2 if err_type == 3 else err_amt):
			o = "".join(random.choices(nuc_types, k=k))
			if o not in oligos:
				oligos.append(o)
				c += 1
		c = 0
	if err_type == 2 or err_type == 3:
		for _ in range(err_amt // 2 if err_type == 3 else err_amt):
			available = list(range(len(oligos)))
			available.remove(oligos.index(init))
			oligos.pop(random.choice(available))

	oligos.sort()

	return oligos


def gen_oligos(n: int, k: int) -> tuple[str, list, str]:
	nuc = "".join(random.choices(nuc_types, k=n))
	oligos = []

	for i in range(n):
		if n - i >= k:
			o = nuc[i : i + k]
			if o not in oligos:
				oligos.append(o)
	init = oligos[0]
	oligos.sort()

	return init, oligos, nuc


if __name__ == "__main__":
	main()