# -*- coding: utf-8 -*-
"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from genetic_algorithm.ga_numeric import genetic_algorithm
from RosembrockExample import Rosembrock
import matplotlib.pyplot as plt


NumIndividuals = 100
MinX1 = -2
MaxX1 = 2
MinX2 = -1
MaxX2 = 3
IndividualSize = 16
MutationRate = 0.02

problem = Rosembrock(MinX1, MaxX1, MinX2, MaxX2, IndividualSize)

#individual="0100000000000000";
#decimal = problem.bin_to_dec(individual[:int(IndividualSize/2)]);
#print(decimal)
#real =problem.x1Real(decimal)
#print(real)

MaxGeneration = 100
Target = 0.00001
Elitism = True


ClassHandle  = genetic_algorithm(problem,MutationRate,Elitism)
fit,generation = ClassHandle.search(NumIndividuals, MaxGeneration, Target)

interaction=[i for i in range(generation)]
plt.plot(interaction,fit)
plt.show()  