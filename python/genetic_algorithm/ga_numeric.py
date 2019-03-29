"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""
import numpy as np
from bisect import bisect_left


class genetic_algorithm(object):
    '''
    classdocs
    '''

    def __init__(self, problem, mutation_rate, elitism=False):
        '''
        Constructor
        '''
        self.__mutationRate = mutation_rate
        self.__elitism = elitism
        self.problem = problem
        self.best_fit = 0
        self.best_individual = []

    def __mutation(self, individual):
        if self.__mutationTest():
            randomPosition = int(np.random.uniform(0, self.problem.individual_size - 1))
#             print('Mutation at position: %d' %randomPosition)
            # get a random value for changing in the individual position selected before
            randomValue = np.random.uniform(self.problem.getMinGeneSymbol(), 
                                            self.problem.getMaxGeneSymbol())

            individual[randomPosition] = round(randomValue)
            
        return individual

    def __mutationTest(self):
        return np.random.rand() > self.__mutationRate
        
    def __bestFitness(self):
        pop_fit = self.problem.fitness(self.population)
#         print(pop_fit)
        best_fit = max(pop_fit)
        best_individual = pop_fit.index(best_fit)

        return best_fit, best_individual

    def __crossover3(self, individual_x, individual_y):
        n = self.problem.individual_size
        c = np.random.uniform(1, n)
        d = np.random.uniform(c, n)
#         print("crossing point 1: %d" %c)
#         print("crossing point 2: %d" %d)

        def create_individual(ind_x, ind_y):
            return [*ind_x[:c], *ind_y[c:d], *ind_x[d:]]

        return (
            create_individual(individual_x, individual_y),
            create_individual(individual_y, individual_x),
        )

    def __crossover(self, individual_x, individual_y):
        c = int(np.random.uniform(0, self.problem.individual_size-1))
#         print("crossing point: %d" %c)

        return (
            [*individual_x[:c], *individual_y[c:]],
            [*individual_y[:c], *individual_x[c:]]
        )
    
    def __get_cum_sum_for_pop(self):
        self.population = sorted(self.population, key=self.problem.getFitness, reverse=True)
        
        pop_fit = self.problem.fitness(self.population)
#         print(pop_fit)

        pop_fit_sum = np.sum(pop_fit)
        prob_fit = [1.0*individual/pop_fit_sum for individual in pop_fit]
#         print(prob_fit)

        # Get the cumulative sum of the probabilities.
        return np.cumsum(prob_fit)

    def __selection(self, cumSumP):
        # Get our random numbers - one for each column.
        randomNumber = np.random.rand()
        
        i = bisect_left(cumSumP, randomNumber)
        selected = self.population[i]
        
        # Display it. Uncomment for log.
#         print("Selected individual [%d] = %s" %(i,selected))
        return selected

    def __newPopulation(self, population_size):
        new_population = []
        offset_population_index = 0

        if self.__elitism:
            new_population.append(self.population[self.best_individual])
            offset_population_index = 1
            
        cumSumP = self.__get_cum_sum_for_pop()

        for i in range(offset_population_index, population_size, 2):
            # Selection
            x = self.__selection(cumSumP)
            y = self.__selection(cumSumP)

            # Crossover
            new_individual_x, new_individual_y = self.__crossover(x, y)

            # Mutation
            new_individual_x = self.__mutation(new_individual_x)
            new_individual_y = self.__mutation(new_individual_y)

#             print('New individual x: %s'%new_individual_x)
#             print('New individual y: %s'%new_individual_y)

            new_population.append(new_individual_x)
            new_population.append(new_individual_y)
        
        return new_population

    def search(self, population_size, max_generation, target):
        generation = 1
        fit_historical = []
        last_best_fit = 0

        self.population = self.problem.initPopulation(population_size)

        self.best_fit, self.best_individual = self.__bestFitness()

#         print("Generation: %d" %generation)
#         print("Population: %s" %self.population)
#         print("Best fit: Individual [%d] = %g" %(self.best_individual,self.best_fit))

        fit_historical.append(self.best_fit)

#         while (np.abs(self.best_fit-last_best_fit) > target) and (generation < max_generation):
        while ((1 - self.best_fit) > target) and (generation < max_generation):
            #         while (generation < max_generation):
            generation += 1

            self.population = self.__newPopulation(population_size)

            self.best_fit, self.best_individual = self.__bestFitness()
            last_best_fit = self.best_fit

#             print("\r\nGeneration: %d" %generation)
#             print("Population: %s" %self.population)
#             print("Best fit: Individual[%d] = %g" %(self.best_individual,self.best_fit))

            fit_historical.append(self.best_fit)

        print("Solution found: %s\r\n" % self.population[self.best_individual])
        print(f"Generations taken: {generation}")
        print(f"Best fit: {self.best_fit}")

        self.problem.printSolution(self.population[self.best_individual])

        return fit_historical, generation
