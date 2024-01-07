import random
import numpy as np
from users import *

class Customer():
    def __init__(self, demand):
        self.demand = demand
class Producent():
    def __init__(self, quantity, price):
        self.price = price
        self.quantity = quantity

class Bee():
    def __init__(self, product, matrix_producents, matrix_customers, number_products, number_customers, number_bees, number_observator, restricition, producents, price, distance):
        self.product = product
        self.matrix_producents = matrix_producents
        self.matrix_customers = matrix_customers
        self.number_products = number_products
        self.number_customers = number_customers
        self.number_bees = number_bees
        self.number_observator = number_observator
        self.restricition = restricition #Wektor klientow posiadajacych zapotrzebowanie na produkt X
        self.producents = producents  #Wektor producentow produkujacych produkt X
        self.price = price
        self.distance = distance

    def function(self, distribuation):
            k = self.product - 1
            m = len(self.matrix_producents[0])
            n = len(distribuation[0])
            value = 0
            matrix = [[0] * m for i in range(n)]
            for i in range(n):
                for j in range(m):
                    if distribuation[i][j] >= 0.1 * self.matrix_producents[j][k]:
                        matrix[i][j] = distribuation[i][j] * self.price[j][k]
                    else:
                        matrix[i][j] = distribuation[i][j] * self.price[j][k] + 0.45 * self.distance[i][j]
                    value += matrix[i][j]
                    value = round(value, 5)
            return value
    
    def function_efficency(self, value):
            value_eff = 1 / (1 + value)
            value_eff = round(value_eff, 5)
                    
            return value_eff
        

    def correct_position(self, new_bee):
            
            counter=0
            kolumny = np.sum(new_bee, axis=0)
            wiersze = np.sum(new_bee, axis=1)
            
            while not(np.all(self.restricition == wiersze) and np.all(kolumny <= self.producents)):
                a=np.shape(new_bee)[0]
                b=np.shape(new_bee)[1]
                for i in range(a):
                    for j in range(b):
                        k=random.randint(0,b-1)
                        roz=np.abs(self.restricition[i]-wiersze[i])
                        value=random.randint(0,roz)
                        if self.restricition[i] >= wiersze[i]:
                            if np.sum(new_bee,axis=0)[k]+value <= self.producents[k]:
                                new_bee[i, k] = new_bee[i, k] + value
                                kolumny = np.sum(new_bee, axis=0)
                                wiersze=np.sum(new_bee,axis=1)
                                break
                        if self.restricition[i]< wiersze[i]:
                            if new_bee[i,k]-value > 0:
                                new_bee[i, k] = new_bee[i, k] - value
                                kolumny = np.sum(new_bee, axis=0)
                                wiersze=np.sum(new_bee,axis=1)
                                break
                counter += 1
                kolumny = np.sum(new_bee, axis=0)
                wiersze=np.sum(new_bee,axis=1)
                if counter >= 10:
                    new_bee,correct_value,correct_eff = self.generate_matrix_production(new_bee, 1)
                    new_bee=np.squeeze(new_bee)
                    return new_bee
            return new_bee
        
        
    def generate_matrix_production(self, producents, n):

            matrixes = []
            vector = []
            vector_eff = []

            while len(matrixes) < n:
                matrix = np.zeros((self.number_customers, self.number_products), dtype=int)

                for j in range(self.number_customers):
                    value = self.restricition[j]
                    for i in range(self.number_products):
                        if i == self.number_products - 1:
                            a = self.producents[i] - np.sum(matrix[:j, i])
                            if value <= a:
                                matrix[j, i] = value
                            else:
                                break  # Przerwanie pętli w przypadku braku dopuszczalnej macierzy
                        else:
                            x = random.randint(0, min(value, self.producents[i] - np.sum(matrix[:j, i])))
                            matrix[j, i] = x
                            value -= x
                    else:
                        continue
                    break

                else:
                    # Ta część kodu zostanie wykonana, jeśli pętla zakończy się naturalnie (bez przerwania)
                    matrixes.append(matrix)
            for i in range(len(matrixes)):
                vector.append(self.function(matrixes[i]))
                vector_eff.append(self.function_efficency(vector[i]))

            return matrixes, vector, vector_eff    
        
        
    def generate_neighbours(self, matrix):
        n = len(matrix)
        neighbours_matrix = np.zeros(np.shape(matrix))
        fi = np.random.randint(0, 2, size=np.shape(matrix))
        neighbours_matrix = matrix + fi
        corrected_neighbour = self.correct_position(neighbours_matrix)
        return corrected_neighbour

    def employee_bees(self, matrixes, vector, eff):
            counter_list = [0 for i in range(len(matrixes))]
            list_neighbours = [0 for i in range(len(matrixes))]
            for i in range(len(matrixes)):
                neighbour_matrix = self.generate_neighbours(matrixes[i])
                new_value = self.function(neighbour_matrix)
                if new_value < vector[i]:
                    list_neighbours[i] = neighbour_matrix
                    vector[i] = new_value
                    eff[i] = self.function_efficency(new_value)
                else:
                    list_neighbours[i] = matrixes[i]
                    counter_list[i] += 1
            matrixes = list_neighbours
            return matrixes, vector, eff, counter_list
        
    def onlooker_bees(self, matrixes, vector, eff, counter_list, ob):
            counter = 0
            counter_help = 0
            matrixes1 = np.array(matrixes[0])
            if ob < len(eff):
                list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(eff))]
                list_value = [0 for i in range(len(eff))]
                list_efficency = [0 for i in range(len(eff))]
            else:
                list_position = [np.zeros(np.shape(matrixes1)) for i in range(ob)]
                list_value = [0 for i in range(ob)]
                list_efficency = [0 for i in range(ob)]
            
            list_probability = [0 for i in range(len(eff))]
            for i in range(len(eff)):
                list_probability[i] = eff[i] / np.sum(eff)
            while counter < ob:
                for i in range(ob):
                    for j in range(len(matrixes)):
                        r = random.uniform(0, 1)
                        if r < list_probability[j]:
                            if np.array_equal(list_position[i], np.zeros(np.shape(matrixes1))):
                                list_position[i] = self.generate_neighbours(matrixes[j])
                                list_value[i] = self.function(list_position[i])
                                list_efficency[i] = self.function_efficency(list_value[i])
                                if vector[j] > list_value[i]:
                                    matrixes[j] = list_position[i]
                                    vector[j] = list_value[i]
                                    eff[j] = list_efficency[i]
                                    counter_list[j] = 0
                                counter += 1
                                break
            return matrixes, vector, eff, counter_list    

    def scout_bees(self, matrixes,vector, eff, counter_list, limit):
            matrixes1 = np.array(matrixes[0])
            list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(matrixes))]
            for i in range(len(matrixes)):
                if counter_list[i] > limit:
                    matrix, vec, eff1 = self.generate_matrix_production(self.matrix_producents, 1)
                    matrix = np.squeeze(np.array(matrix))
                    matrixes[i] = matrix
                    vector[i] = vec
                    eff[i] = eff1
                    counter_list[i] = 0
                
            return matrixes, np.squeeze(vector), np.squeeze(eff), counter_list
        

    def ABC(self, limit, limit_iter):
            population, vec, vec_eff = self.generate_matrix_production(self.matrix_producents, self.number_bees)
            vector_best = []
            counter = 0
            while counter < limit_iter:
                print(f" Mati to szef zapamiętaj to po raz  {counter}")
                population, vec, vec_eff, counter_list= self.employee_bees(population, vec, vec_eff)
                population, vec, vec_eff, counter_list = self.onlooker_bees(population, vec, vec_eff, counter_list, self.number_observator)
                population, vec, vec_eff, counter_list = self.scout_bees(population, vec, vec_eff, counter_list, limit)
                vector_best.append(min(vec))
                counter += 1

            fitness_index = np.argmin(vec)
            fitness_value = vec[fitness_index]
            population_best = population[fitness_index]

            return population_best, vector_best, fitness_value


# producenci=np.array([[35,21,33],[29,44,26],[1000,22,23]])
# klienci=np.array([[21,33,32],[33,32,23],[25,22,22]])
# cena=np.array([[10,4,5],[1,7,4],[1000,2,5]])
# dystans=[[5,22,11],[100,55,30],[22,10,15]]
# ograniczenia=[23,21,33]
# produkcja=[45,40,1000]
# macierz_test = np.array([[3, 5, 6], [17, 10, 2], [11, 17, 7]])
# product = 2
# def get_restriction(customers, producents, k):
#     help_customers = np.transpose(customers)
#     help_producents = np.transpose(producents)
#     producents = help_producents[k - 1]
#     restricition = help_customers[k - 1]
#     return producents, restricition
# produkcja, ograniczenia = get_restriction(klienci, producenci, product)
# print(produkcja, ograniczenia)
# number_bees = 10
# number_observator = 20
# number_products = 3
# number_customers = 3
# bee = Bee(product, producenci, klienci, number_products, number_customers, number_bees, number_observator, ograniczenia, produkcja, cena, dystans)
# popultaion_best,vector_best,fitness_value=bee.ABC(10, 10)

# print("Jakub Pawłowski obliczył, że najlepsze jest dopasowanie: ", "\n")
# print(popultaion_best, "\n")
# print("najlepsza wartość funkcji celu jest równa:  ", "\n")
# print(fitness_value)
# print("Wektor\n")
# print(vector_best)

# y=bee.function(popultaion_best)

