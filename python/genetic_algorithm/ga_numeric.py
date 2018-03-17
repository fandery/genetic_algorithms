"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""
import numpy as np

class genetic_algorithm(object):
    '''
    classdocs
    '''

    def __init__(self, problem, mutation_rate, elitism = None):
        '''
        Constructor
        '''
        self.__mutationRate = mutation_rate
        if(elitism == None):
            self.__elitism = False
        else:
            self.__elitism = elitism
        self.problem = problem
        self.best_fit = 0
        self.best_individual = []
    
    def __mutation(self,individual):
        
        if self.__mutationTest():
            randomPosition = int(np.random.uniform(0,self.problem.getIndividualSize()-1))
            print('Mutation at position: %d' %randomPosition)
            #get a random value for changing in the individual position selected before
            randomValue = np.random.uniform(self.problem.getMinGeneSymbol(),self.problem.getMaxGeneSymbol())
         
            if(randomValue <= 0.5):
                randomValue = int(randomValue)
            else:
                randomValue = int(randomValue+1)
            
            print('New gene value: %d' %randomValue)
            
            individual[randomPosition]=randomValue
        return individual
    
    def __mutationTest(self):
        a=[0, 1]
        p=[1-self.__mutationRate, self.__mutationRate]
        #Get the cumulative sum of the probabilities.
        cumSumP = np.cumsum(p)
        #Get our random numbers - one for each column.
        randomNumber = np.random.rand()
        #Get the values from A.
        #If the random number is less than the cumulative probability then
        #that's the number to use from A.
        for i, total in enumerate(cumSumP):
            if randomNumber < total:
                break
        test=a[i]
        if test == 1:
            print('Mutation!')
        return test
    
    def __bestFitness(self):
     
        pop_fit = self.problem.fitness(self.population)
#         print(pop_fit)
        best_fit=pop_fit[0]
        best_individual=0
        for i in range(1,len(pop_fit)):
            if(pop_fit[i] > best_fit):
                best_fit = pop_fit[i]    
                best_individual=i
         
        return best_fit,best_individual        

    
    def __crossover3(self,individual_x,individual_y):
        
        n=self.problem.getIndividualSize()
        
        c = np.random.uniform(1,n)
        d = np.random.uniform(1,n)    
        print("crossing point 1: %d" %c)
        print("crossing point 2: %d" %d)
        
        new_individual_x=[]
        new_individual_y=[]
        
        # concatenate the two fathers in the C element chosen randomly
        for gene in range(c):
            new_individual_x.append(individual_x[gene])
            new_individual_y.append(individual_y[gene])
        
        for gene in range(c,d):
            new_individual_y.append(individual_y[gene])
            new_individual_x.append(individual_x[gene])
            
        for gene in range(d,n):    
            new_individual_x.append(individual_x[gene])
            new_individual_y.append(individual_y[gene])
        
        return new_individual_x,new_individual_y
    
    def __crossover(self,individual_x,individual_y):
        
        
        n=self.problem.getIndividualSize()
        
        c = int(np.random.uniform(0,n-1))
        print("crossing point: %d" %c)
        
        new_individual_x=[]
        new_individual_y=[]
        
        # concatenate the two fathers in the C element chosen randomly
        for gene in range(c):
            new_individual_x.append(individual_x[gene])
            new_individual_y.append(individual_y[gene])
        for gene in range(c,n):    
            new_individual_x.append(individual_y[gene])
            new_individual_y.append(individual_x[gene])
        
        return new_individual_x,new_individual_y
    
    
    def __selection(self):
    
        sorted_population = sorted(self.population,key=self.problem.getFitness, reverse=True)        
        pop_fit = self.problem.fitness(sorted_population)
#         print(pop_fit)
        
        prob_fit = []
        for individual in pop_fit:
            prob_fit.append(1.0*individual/np.sum(pop_fit))
#         print(prob_fit)
        
        #Get the cumulative sum of the probabilities.
        cumSumP = np.cumsum(prob_fit)
        #Get our random numbers - one for each column.
        randomNumber = np.random.rand()
        #Get the values from A.
        #If the random number is less than the cumulative probability then
        #that's the number to use from A.
#        print('Random: %g' %randomNumber)
#        print(cumSumP)
        for i, total in enumerate(cumSumP):
            if randomNumber < total:
                break
        self.population = sorted_population
        selected = self.population[i]
        #Display it. Uncomment for log.
        print("Selected individual [%d] = %s" %(i,selected))
        return selected
        
    def __newPopulation(self,population_size):
        
        new_population = []
        offset_population_index=0
        
        if self.__elitism:
            new_population.append(self.population[self.best_individual])
            offset_population_index=1
        
        
        for i in range(offset_population_index,population_size,2):
            #Selection
            x = self.__selection()
            y = self.__selection()
            
            #Crossover
            new_individual_x,new_individual_y = self.__crossover(x,y)
            
            #Mutation
            new_individual_x = self.__mutation(new_individual_x)
            new_individual_y = self.__mutation(new_individual_y)
            
            print('New individual x: %s'%new_individual_x)
            print('New individual y: %s'%new_individual_y)
            
            new_population.append(new_individual_x)
            new_population.append(new_individual_y)
        return new_population
    
    def search(self, population_size, max_generation, target):
        
        generation = 1
        fit_historical=[]
        last_best_fit = 0 
        
        self.population = self.problem.initPopulation(population_size)
        
        self.best_fit,self.best_individual = self.__bestFitness()
                
        print("Generation: %d" %generation)
        print("Population: %s" %self.population)
        print("Best fit: Individual [%d] = %g" %(self.best_individual,self.best_fit))
        
        fit_historical.append(self.best_fit)
                
        #while (np.abs(self.best_fit-last_best_fit) > target) and (generation < max_generation):
        while (generation < max_generation):
            
            generation=generation+1
            
            self.population=self.__newPopulation(population_size)      
            
            self.best_fit,self.best_individual = self.__bestFitness()
    
            print("\r\nGeneration: %d" %generation)
            print("Population: %s" %self.population)
            print("Best fit: Individual[%d] = %g" %(self.best_individual,self.best_fit))
            
            fit_historical.append(self.best_fit)
                        
            
        print("Solution found: %s\r\n" %self.population[self.best_individual])
        
        self.problem.printSolution(self.population[self.best_individual])
            
        return fit_historical,generation    