# Test of Simullator class

import sys
sys.path.append("./src")
from Simulator import *
from numpy import random


def generate_infos(size, nb_product):
	infos = []
	pick  = [e for e in range(nb_product)]
	for node in range(size):
		#random.randint(0,10)/10 to have human readable probabilities
		#random.randint(0,nb_product) fix the secondary product to display (can it be itself ? if not : random.choice(pick.copy().remove(node)))
		pick_tmp = pick.copy()
		pick_tmp.remove(node)
		tmp = [[random.choice(pick_tmp),random.randint(0,10)/10,random.choice(pick_tmp),random.randint(0,10)/10] for _ in range(nb_product)]
		infos.append(tmp)
	return infos

def generate_mu(size):
	mu = []
	for node in range(size):
		mu.append(random.randint(0,10)/10)
	return mu

def main():
	nb_classes = 3
	nb_product = 5
	expected_alphas = [[0.1,0.2,0.7],[0.3,0.4,0.3],[0.5,0.1,0.4]]
	simu = Simulator(generate_infos(nb_classes,nb_product), generate_mu(nb_classes), expected_alphas, nb_classes)
	for i in range(len(simu.graphs)):
		print(simu.graphs[i])
		print('current : ',simu.current[i])
		print("after click ", simu.click(i))	


if __name__ == "__main__":
	main()
