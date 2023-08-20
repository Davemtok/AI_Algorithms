import random
import copy
from tkinter import Label
# from Week 2.editgenealgorithm import BestFitness
import matplotlib.pyplot as plt
import math

from matplotlib import cm  # color map
from mpl_toolkits.mplot3d import Axes3D

# declare number of genes
# where n =20
N = 20
A = 10
# declare population so 50 in this case
P = 500

#Generations
G = 150

#set class individual
class individual:
    def __init__(self):
        # binary gene and finess values
        self.gene = [0] * N # [0,0,0,0,0,0,0,0,0,0]
        self.fitness = 0

# FITNESS FUNCTION
# tells us the fitness score
def oldfitnessfinder( ind ):
        fitness=0
        for i in range(N):
            # adding each gene's value to the fitness score
            fitness = fitness + ind.gene[i]
        #returns the number of ones in the gene
        return fitness
   
# def newerFitnessFinder ( ind ):
#     tot = 0
#     for i in range(0, N - 1):
#         tot += ((100 * (ind.gene[i + 1]) - (ind.gene[i] ** 2)) ** 2) + ((1 - (ind.gene[i])) ** 2)
#     return tot

def RastriginFinder ( ind ):
    tot = 0
    for i in range(0, N):
        tot += ((ind.gene[i] ** 2) - (10 * math.cos(2 * math.pi * ind.gene[i])))
    
    tot = tot + (10 * N)
    return tot


#offspring as an array
offspring=[]
totaloffspring=0
# How often elements mutate
MUTRATE = 0.5

#array of data structure type population
population = []

#mean fitness array
mean_fitness = []
#best fitness array
Bestfitness = []

#Initialise population with random candite solutions
# for x in range (0, P): # looping this * 50
#     tempgene=[]
#     for y in range (0, N):
#         # randomize 0 and 1s in the array
#         tempgene.append( random.randint(0,1))
#     newind = individual()
#     newind.gene = tempgene.copy()
#     population.append(newind)

# min and max supposed to be -100 and 100?
MIN = -100
MAX = 100

for x in range (0, P): # looping this * 50
    tempgene=[]
    for y in range (0, N):
        # randomize 0 and 1s in the array
        tempgene.append( random.uniform(MIN,MAX))
    newind = individual()
    newind.gene = tempgene.copy()
    population.append(newind)
    newind.fitness = RastriginFinder(newind)

 #?
for i in range(0,P):
    population[i].fitness = RastriginFinder(population[i])



#For each generation
for gen in range (0, G):
      
    offspring = []
    # Mutstep us how big I want the mutation to be
    # how much it ads and subtracts the gene
    # 0.06
    # MUTSTEP = 0.06
    #Best mutation size change
    MUTSTEP = 0.05
    
    #Selection
    for i in range(0,P):
        parent1 = random.randint( 0, P-1 )
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint( 0, P-1 )
        off2 = copy.deepcopy(population[parent2])
        
        #Finding the worst fitness
        if off1.fitness < off2.fitness:
            offspring.append( off1 )
            #gives the best total offspring
            # totaloffspring += off1.fitness
        else:
            offspring.append( off2 )
            # totaloffspring += off2.fitness

    #Crossover
    toff1 = individual()
    toff2 = individual()
    temp = individual()

    for i in range( 0, P, 2 ):
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i+1])
        temp = copy.deepcopy(offspring[i])
        crosspoint = random.randint(1,N)
        for j in range (crosspoint, N):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        offspring[i] = copy.deepcopy(toff1)
        offspring[i+1] = copy.deepcopy(toff2)

    #Mutation
    # for i in range( 0, P ):
    #     newind = individual();
    #     newind.gene = []
    #     for j in range( 0, N ):
    #         gene = offspring[i].gene[j]
    #         mutprob = random.random()
    #         if mutprob < MUTRATE:
    #             if( gene == 1):
    #                 gene = 0
    #             else:
    #                 gene = 1
    #         newind.gene.append(gene)
    #     newind.fitness = fitnessfinder(newind)
    #     #you must then append new individual or overwrite offspring
    #     offspring[i] = copy.deepcopy(newind)

    # Mutation2
    for i in range(  0, P ): 
        newind = individual(); 
        newind.gene = [] 
        for j in range( 0, N ): 
            gene = offspring[i].gene[j] 
            mutprob = random.random() 
            if mutprob < MUTRATE: 
                alter = random.uniform(-MUTSTEP,MUTSTEP) 
                gene = gene + alter 
                if gene > MAX: 
                    gene = MAX 
                if gene < MIN:
                    gene = MIN 
            newind.gene.append(gene)
        newind.fitness = RastriginFinder(newind)
        #append new individual or overwrite offspring
        offspring[i] = copy.deepcopy(newind)


    #Finding the worst fitness
    worstfit = population[0].fitness
    bestind = 0
    for i in range(0, P):
        if population[i].fitness < worstfit:
            worstfit = population[i].fitness
            bestind = i
    
    # finds the best fintess for the population
    worstsolution = offspring[0].fitness
    worstind = 0
    for i in range(0, P):
        if offspring[i].fitness > worstsolution:
            worstsolution = offspring[i].fitness
            worstind = i

    # appends the worst offspring with the new offspring
    offspring[worstind] = copy.deepcopy(population[bestind])
    population = copy.deepcopy(offspring)

    # calculating the mean fitness
    totalfitness=0
    for i in range(0,P):
        totalfitness+=population[i].fitness
    
    mean_fitness.append(totalfitness / P)

    # makes sure the worst fitness is always used
    worstfit = population[0].fitness
    bestind = 0
    for i in range(0, P):
        if population[i].fitness < worstfit:
            worstfit = population[i].fitness
            for i in range(0, P):
                if population[i].fitness < worstfit:
                    worstfit = population[i].fitness
                    bestind = i

    # at the end of every generation it makes sure it has the best individual 
    # elitism
    Bestfitness.append(worstfit)

# this is the best total fitness for the parents
    # print("Population", population[i].gene)
    print("Generation:" + str(gen))
    print(worstfit)
    print("Average Fitness: " + str((totalfitness / P)))
    print("")

with open('Assignment Folder/AIRastr.txt','a') as f:
    f.writelines("population:")
    f.writelines(str(P))
    f.writelines("\ngene length:")
    f.writelines(str(N))
    f.writelines("\nmut rate:")
    f.writelines(str(MUTRATE))
    f.writelines("\nmut_step:")
    f.writelines(str(MUTSTEP))
    f.writelines("\ngenerations:")
    f.writelines(str(G))
    f.writelines("\nbest performing ind:")
    f.writelines(str(worstfit))
    f.writelines("\naverage performance:")
    f.writelines(str(totalfitness/P))
    f.writelines("\n########################################\n")
    f.close()

# naming the x axis
plt.xlabel(' Generation ')
# naming the y axis
plt.ylabel(' Fitness ')

plt.plot(Bestfitness, label = "Fitness Per Generation")
plt.plot(mean_fitness, label = "Average Fitness")
plt.legend()
plt.show()




