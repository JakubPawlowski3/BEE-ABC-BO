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
    def __init__(self, matrix_producents, matrix_customers, number_products, number_customers, restricition, producents, price, distance):
        self.matrix_producents = matrix_producents
        self.matrix_customers = matrix_customers
        self.number_products = number_products
        self.number_customers = number_customers
        self.restricition = restricition #Wektor klientow posiadajacych zapotrzebowanie na produkt X
        self.producents = producents  #Wektor producentow produkujacych produkt X
        self.price = price
        self.distance = distance

    def function(self, matrix_producents, matrix_customers):
        m = self.number_products
        n = self.number_customers
        value = 0.0
        matrix = [[0] * m for i in range(n)]
        for i in range(n):
            for j in range(m):
                if np.any(matrix_customers[i][j] >= 0.1 * matrix_producents[j][0]):
                    matrix[i][j] = matrix_customers[i][j] * self.price[j][0]
                else:
                    matrix[i][j] = matrix_customers[i][j] * self.price[j][0] + 0.45 * self.distance[i][j]
                value += np.any(matrix[i][j])
                value = round(value, 5)
        return value
    
    def function_efficency(self, value):
        value_eff = 1 / (1 + value)
        value_eff = np.round(value_eff, 5)
                
        return value_eff

    def generate_matrix_production(self, n, matrix_producents):


        matrixes = []
        vector = []
        vector_eff = []

        while len(matrixes) < n:
            matrix = np.zeros((self.number_products, self.number_customers), dtype=int)

            for j in range(self.number_products):
                value = self.restricition[j]
                for i in range(self.number_customers):
                    if i == self.number_customers - 1:
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
            vector.append(self.function(matrix_producents, matrixes[i]))
            vector_eff.append(self.function_efficency(vector[i]))

        return matrixes, vector, vector_eff

    def correct_position(self, neighbour, q):
        
        counter=0
        kolumny = np.sum(neighbour, axis=0)
        wiersze = np.sum(neighbour, axis=1)
        
        while not(np.all(self.restricition == wiersze) and np.all(kolumny <= self.producents)):
            a=np.shape(neighbour)[0]
            b=np.shape(neighbour)[1]
            for i in range(a):
                for j in range(b):
                    k=random.randint(0,b-1)
                    roz=np.abs(self.restricition[i]-wiersze[i])
                    value=random.randint(0,roz)
                    if self.restricition[i] >= wiersze[i]:
                        if np.sum(neighbour,axis=0)[k]+value <= self.producents[k]:
                            neighbour[i, k] = neighbour[i, k] + value
                            kolumny = np.sum(neighbour, axis=0)
                            wiersze=np.sum(neighbour,axis=1)
                            break
                    if self.restricition[i]< wiersze[i]:
                        if neighbour[i,k]-value > 0:
                            neighbour[i, k] = neighbour[i, k] - value
                            kolumny = np.sum(neighbour, axis=0)
                            wiersze=np.sum(neighbour,axis=1)
                            break
            counter += 1
            kolumny = np.sum(neighbour, axis=0)
            wiersze=np.sum(neighbour,axis=1)
            if counter >= 10:
                neighbour,correct_value,correct_eff = self.generate_matrix_production(q, neighbour)
                neighbour=np.squeeze(neighbour)
                return neighbour
        return neighbour


    def generate_neighbours(self, matrix, q):
        n = len(matrix)
        neighbours_matrix = [[0]*n for i in range(n)]
        fi = np.random.randint(0, 2, size=(n,n))
        neighbours_matrix = matrix + fi
        corrected_neighbour = self.correct_position(neighbours_matrix, q)
        return corrected_neighbour

    def employee_bees(self, matrixes, vector, eff, q):
        counter_list = [0 for i in range(len(matrixes))]
        list_neighbours = [0 for i in range(len(matrixes))]
        for i in range(len(matrixes)):
            neighbour_matrix = self.generate_neighbours(matrixes[i], q)
            new_value = self.function(self.matrix_producents, neighbour_matrix)
            if np.any(new_value < vector[i]):
                list_neighbours[i] = neighbour_matrix
                vector[i] = new_value
                eff[i] = self.function_efficency(new_value)
            else:
                list_neighbours[i] = matrixes[i]
                counter_list[i] += 1
        matrixes = list_neighbours
        return matrixes, vector, eff, counter_list

    def onlooker_bees(self, matrixes, vector, eff, counter_list, ob, q):
        counter = 0
        counter_help = 0
        matrixes1 = np.array(matrixes[0])
        list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(eff))]
        list_value = [0 for i in range(len(eff))]
        list_efficency = [0 for i in range(len(eff))]
        list_probability = [0 for i in range(len(eff))]
        for z in range(len(eff)):
            list_probability[z] = eff[z] / np.sum(eff)
        while counter < ob:
            for i in range(ob):
                for j in range(len(matrixes)):
                    r = random.uniform(0, 1)
                    if np.any(r < list_probability[j]):
                        if np.array_equal(list_position[i], np.zeros(np.shape(matrixes1))):
                            list_position[i] = self.generate_neighbours(matrixes[j], q)
                            list_value[i] = self.function(self.matrix_producents, list_position[i])
                            list_efficency[i] = self.function_efficency(list_value[i])
                            if np.any(vector[j] > list_value[i]):
                                matrixes[j] = list_position[i]
                                vector[j] = list_value[i]
                                eff[j] = list_efficency[i]
                                counter_list[j] = 0
                            counter += 1
                            break
        return matrixes, vector, eff, counter_list 

    def scout_bees(self, matrixes,vector, eff, counter_list, limit, q):
        matrixes1 = np.array(matrixes[0])
        list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(matrixes))]
        for i in range(len(matrixes)):
            if counter_list[i] > limit:
                matrix, vec, eff1 = generate_matrix_production(self.matrix_producents,self.restricition, self.producents, 1)
                matrix = np.squeeze(np.array(matrix))
                matrixes[i] = matrix
                vector[i] = vec
                eff[i] = eff1
                counter_list[i] = 0
            
        return matrixes, np.squeeze(vector), np.squeeze(eff), counter_list

    def ABC(self, n, ob, limit, limit_iter, q):
        population, vec, vec_eff = self.generate_matrix_production(q, self.matrix_producents)
        vector_best = []
        counter = 0
        while counter < limit_iter:
            print(f" Mati to szef zapamiętaj to po raz  {counter}")
            population, vec, vec_eff, counter_list = self.employee_bees(population, vec, vec_eff, q)
            population, vec, vec_eff, counter_list = self.onlooker_bees(population, vec, vec_eff, counter_list, ob, q)
            population, vec, vec_eff, counter_list = self.scout_bees(population, vec, vec_eff, counter_list, limit, q)
            vector_best.append(np.min(vec))
            counter += 1

        fitness_index = np.argmin(vec)
        fitness_value = vec[fitness_index]
        population_best = population[fitness_index]

        return population_best, vector_best, fitness_value


producenci=np.array([[35,21,33],[29,44,26],[1000,22,23]])
klienci=np.array([[21,33,32],[33,32,23],[25,22,22]])
cena=np.array([[10,4,5],[1,7,4],[1000,2,5]])
dystans=[[5,22,11],[100,55,30],[22,10,15]]
ograniczenia=[23,21,33]
produkcja=[45,40,1000]
macierz_test=np.array([[3,5,6],[17,10,2],[11,17,7]])

number_products = 3
number_customers = 3
restricition = np.transpose(matrix_customer[0])
producents = np.transpose(matrix_producent[0])
bee = Bee(producenci, klienci, number_products, number_customers, ograniczenia, produkcja, cena, dystans)


popultaion_best,vector_best,fitness_value= bee.ABC(100, 20, 10, 100, 100)

print("Jakub Pawłowski obliczył, że najlepsze jest dopasowanie: ", "\n")
print(popultaion_best, "\n")
print("najlepsza wartość funkcji celu jest równa:  ", "\n")
print(fitness_value)

y=bee.function(producenci,popultaion_best)