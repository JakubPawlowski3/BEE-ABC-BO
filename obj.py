import random
import numpy as np
# do wytworzenia macierzy kosztu transportu macierz = [[random.uniform(0.0, 10.0) for i in range(producents)] for i in range(customers)]
# do wytworzenia ilosci produktow lista_produktow = [random.randint(max_demand, 100) for i in range(n)]
# do wytworzenia cen produktow cena_produktow = [round(random.uniform(0.0, 100.0), 2) for i in range(n)]
# do wytworzenia zapotrzebowania klienta zapotrzebowanie = [random.randint(0, max_demand) for i in range(n)]

# pierw stworz liste zapotrzebowan, zsumuj zapotrzebowanie wszystkich klientow, a nastepnie stworz liste produktow producentow gdzie dolny zakres
# to zsumowane zaptorzebowanie klientow

#przykladowy producent 
#producent1 = Producents(1, [random.randint(0, 100) for i in range(5)], [round(random.uniform(0.0, 100.0), 2) for i in range(5)])
# wynik 1 [52, 60, 72, 49, 73] [30.95, 28.44, 36.31, 82.93, 61.77]
#gdzie odpowiednio mamy id producenta, liste ilosci produktow produkowanych oraz liste cen dla danego produktu


class Producents():
    def __init__(self, id, quantity, price):
        self.id = id
        self.quantity = quantity
        self.price = price

class Customers():
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand

class Bee():
    def __init__(self, producents, customers, distance, price, number_products):
        self.producents = producents
        self.customers = customers
        self.distance = distance
        self.price = price
        self.number_products = number_products
        
    def function(self, producents, distribuation, price, distance):
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
    
    def function_efficency(self, value):
        value_eff = 1 / (1 + value)
        value_eff = round(value_eff, 5)
                
        return value_eff

                    
        
        
    

        
    def generate_solution_equal(self, producents, customers, distance, price, number_products):
        number_producents = len(producents[0])
        number_customers = len(customers[0])
        u = 0

        list_product_matrix = [0 for i in range(number_products)] 
        for k in range(number_products):
            product = [[0] * number_customers for _ in range(number_producents)]
            sum0 = 0
            sum1 = 0
            for i in range(number_producents):
                for j in range(number_customers):
                    if (customers[i][j] > 0):
                        n = customers[j][k] // 4
                        product[i][j] = n


                    else:
                        cost[i][j] = 0
            sum0 = np.sum(product, axis=0)
            for l in range(number_products):
                m = customers[l][u] - sum0[l]
                o = producents[l][u] - m
                q = [0, 1, 2, 3]
                if (m != 0 and o > 0):

                    product[0][l] += np.abs(m)
                if (m != 0 and o < 0):
                    product[0][q[l]] += np.abs(m) 
            u += 1
                

            list_product_matrix[k] = product
        

        return list_product_matrix

    def generate_matrix_production(self, producents, customers, vector_producents, n, number_producents, number_customers, price, distance):


        matrixes = []
        vector = []
        vector_eff = []

        while len(matrixes) < n:
            matrix = np.zeros((number_producents, number_customers), dtype=int)

            for j in range(number_producents):
                value = customers[j]
                for i in range(number_customers):
                    if i == number_customers - 1:
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
            vector.append(self.function(producents, matrixes[i], price, distance))
            vector_eff.append(self.function_efficency(vector[i]))

        return matrixes, vector, vector_eff

    def generate_neigbours(self, matrix):
        n = len(mmatrix[0])
        neighbours_matrix = [[0]*n for i in range(n)]
        fi = np.random.randint(0, 2, size=(n,n))
        for i in range(len(n)):
            neighbours_matrix = matrix[i] + fi
        return neigbours_matrix
    def employee_bees(self, matrixes, vector, eff):
        for i in range(len(matrixes)):
