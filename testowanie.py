import numpy as np
import random 
producenci=np.array([[35,21,33],[29,44,26],[1000,22,23]])
klienci=np.array([[21,33,32],[33,32,23],[25,22,22]])
cena=np.array([[10,4,5],[1,7,4],[1000,2,5]])
dystans=[[5,22,11],[100,55,30],[22,10,15]]
ograniczenia=[23,21,33]
produkcja=[45,40,1000]
macierz_test=np.array([[3,5,6],[17,10,2],[11,17,7]])

def function(producents, distribuation, price, distance):
        m = len(producents[0])
        n = len(distribuation[0])
        value = 0
        matrix = [[0] * m for i in range(n)]
        for i in range(n):
            for j in range(m):
                if distribuation[i][j] >= 0.1 * producents[j][0]:
                    matrix[i][j] = distribuation[i][j] * price[j][0]
                else:
                    matrix[i][j] = distribuation[i][j] * price[j][0] + 0.45 * distance[i][j]
                value += matrix[i][j]
                value = round(value, 5)
        return value
    
def function_efficency(value):
        value_eff = 1 / (1 + value)
        value_eff = round(value_eff, 5)
                
        return value_eff
    

def correct_position(new_bee,ograniczenia,produkcja,producenci,cena,dystans):
        
        counter=0
        kolumny = np.sum(new_bee, axis=0)
        wiersze = np.sum(new_bee, axis=1)
        
        while not(np.all(ograniczenia == wiersze) and np.all(kolumny <= produkcja)):
            a=np.shape(new_bee)[0]
            b=np.shape(new_bee)[1]
            for i in range(a):
                for j in range(b):
                    k=random.randint(0,b-1)
                    roz=np.abs(ograniczenia[i]-wiersze[i])
                    value=random.randint(0,roz)
                    if ograniczenia[i] >= wiersze[i]:
                        if np.sum(new_bee,axis=0)[k]+value <= produkcja[k]:
                            new_bee[i, k] = new_bee[i, k] + value
                            kolumny = np.sum(new_bee, axis=0)
                            wiersze=np.sum(new_bee,axis=1)
                            break
                    if ograniczenia[i]< wiersze[i]:
                        if new_bee[i,k]-value > 0:
                            new_bee[i, k] = new_bee[i, k] - value
                            kolumny = np.sum(new_bee, axis=0)
                            wiersze=np.sum(new_bee,axis=1)
                            break
            counter += 1
            kolumny = np.sum(new_bee, axis=0)
            wiersze=np.sum(new_bee,axis=1)
            if counter >= 10:
                new_bee,correct_value,correct_eff = generate_matrix_production(producenci,ograniczenia,produkcja,1,a,b,cena,dystans)
                new_bee=np.squeeze(new_bee)
                return new_bee
        return new_bee
    
    
def generate_matrix_production(producents, customers, vector_producents, n, number_customers, number_producents, price, distance):


        matrixes = []
        vector = []
        vector_eff = []

        while len(matrixes) < n:
            matrix = np.zeros((number_customers, number_producents), dtype=int)

            for j in range(number_customers):
                value = customers[j]
                for i in range(number_producents):
                    if i == number_producents - 1:
                        a = vector_producents[i] - np.sum(matrix[:j, i])
                        if value <= a:
                            matrix[j, i] = value
                        else:
                            break  # Przerwanie pętli w przypadku braku dopuszczalnej macierzy
                    else:
                        x = random.randint(0, min(value, vector_producents[i] - np.sum(matrix[:j, i])))
                        matrix[j, i] = x
                        value -= x
                else:
                    continue
                break

            else:
                # Ta część kodu zostanie wykonana, jeśli pętla zakończy się naturalnie (bez przerwania)
                matrixes.append(matrix)
        for i in range(len(matrixes)):
            vector.append(function(producents, matrixes[i], price, distance))
            vector_eff.append(function_efficency(vector[i]))

        return matrixes, vector, vector_eff    
    
    
def generate_neighbours(matrix, production, customers,producenci,cena,dystans):
    n = len(matrix)
    neighbours_matrix = np.zeros(np.shape(matrix))
    fi = np.random.randint(0, 2, size=np.shape(matrix))
    neighbours_matrix = matrix + fi
    corrected_neighbour = correct_position(neighbours_matrix, customers, production,producenci,cena,dystans)
    return corrected_neighbour

def employee_bees(matrixes, vector, eff, production, restriction, producents, price, distance):
        counter_list = [0 for i in range(len(matrixes))]
        list_neighbours = [0 for i in range(len(matrixes))]
        for i in range(len(matrixes)):
            neighbour_matrix = generate_neighbours(matrixes[i], production, restriction,producents,price,distance)
            new_value = function(producents, neighbour_matrix, price, distance)
            if new_value < vector[i]:
                list_neighbours[i] = neighbour_matrix
                vector[i] = new_value
                eff[i] = function_efficency(new_value)
            else:
                list_neighbours[i] = matrixes[i]
                counter_list[i] += 1
        matrixes = list_neighbours
        return matrixes, vector, eff, counter_list
    
def onlooker_bees(matrixes, vector, eff, counter_list, ob, production, customers, producents, price, distance):
        counter = 0
        counter_help = 0
        matrixes1 = np.array(matrixes[0])
        list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(eff))]
        list_value = [0 for i in range(len(eff))]
        list_efficency = [0 for i in range(len(eff))]
        list_probability = [0 for i in range(len(eff))]
        for i in range(len(eff)):
            list_probability[i] = eff[i] / np.sum(eff)
        while counter < ob:
            for i in range(ob):
                for j in range(len(matrixes)):
                    r = random.uniform(0, 1)
                    if r < list_probability[j]:
                        if np.array_equal(list_position[i], np.zeros(np.shape(matrixes1))):
                            list_position[i] = generate_neighbours(matrixes[j], production, customers,producents,price,distance)
                            list_value[i] = function(producents, list_position[i], price, distance)
                            list_efficency[i] = function_efficency(list_value[i])
                            if vector[j] > list_value[i]:
                                matrixes[j] = list_position[i]
                                vector[j] = list_value[i]
                                eff[j] = list_efficency[i]
                                counter_list[j] = 0
                            counter += 1
                            break
        return matrixes, vector, eff, counter_list    

def scout_bees(matrixes,vector, eff, counter_list, limit, producents, customers, vector_producents, number_products, number_customers, price, distance):
        matrixes1 = np.array(matrixes[0])
        list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(matrixes))]
        for i in range(len(matrixes)):
            if counter_list[i] > limit:
                matrix, vec, eff1 = generate_matrix_production(producents, customers, vector_producents, 1, number_products, number_customers, price, distance)
                matrix = np.squeeze(np.array(matrix))
                matrixes[i] = matrix
                vector[i] = vec
                eff[i] = eff1
                counter_list[i] = 0
            
        return matrixes, np.squeeze(vector), np.squeeze(eff), counter_list
    

def ABC(producents, customers, vector_producents, n, ob, number_customers, number_producents, price, distance, limit, limit_iter):
        population, vec, vec_eff = generate_matrix_production(producents, customers, vector_producents, n, number_customers, number_producents,price,distance)
        vector_best = []
        counter = 0
        while counter < limit_iter:
            print(f" Mati to szef zapamiętaj to po raz  {counter}")
            population, vec, vec_eff, counter_list= employee_bees(population, vec, vec_eff, vector_producents,customers, producents, price, distance)
            population, vec, vec_eff, counter_list = onlooker_bees(population, vec, vec_eff, counter_list, ob, vector_producents, customers, producents, price, distance)
            population, vec, vec_eff, counter_list = scout_bees(population,vec,vec_eff,counter_list,limit, producents, customers, vector_producents, number_producents, number_customers, price, distance)
            vector_best.append(min(vec))
            counter += 1

        fitness_index = np.argmin(vec)
        fitness_value = vec[fitness_index]
        population_best = population[fitness_index]

        return population_best, vector_best, fitness_value


popultaion_best,vector_best,fitness_value=ABC(producenci,ograniczenia,produkcja,100,20,3,3,cena,dystans,10,100)

print("Jakub Pawłowski obliczył, że najlepsze jest dopasowanie: ", "\n")
print(popultaion_best, "\n")
print("najlepsza wartość funkcji celu jest równa:  ", "\n")
print(fitness_value)

y=function(producenci,popultaion_best,cena,dystans)

