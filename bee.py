import numpy as np
import random

# do wytworzenia macierzy kosztu transportu macierz = [[random.uniform(0.0, 10.0) for i in range(producents)] for i in range(customers)]
# do wytworzenia ilosci produktow lista_produktow = [random.randint(max_demand, 100) for i in range(n)]
# do wytworzenia cen produktow cena_produktow = [round(random.uniform(0.0, 100.0), 2) for i in range(n)]
# do wytworzenia zapotrzebowania klienta zapotrzebowanie = [random.randint(0, max_demand) for i in range(n)]

# pierw stworz liste zapotrzebowan, zsumuj zapotrzebowanie wszystkich klientow, a nastepnie stworz liste produktow producentow gdzie dolny zakres
# to zsumowane zaptorzebowanie klientow

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
    def __init__(self, producents, customers, distance, price):
        self.producents = producents
        self.customers = customers
        self.distance = distance
        self.price = price
        self.product = self.generate_solution(producents, customers, distance, price)
    

        
    def generate_solution(self, producents, customers, distance, price):
        number_producents = len(producents[0])
        number_customers = len(customers[0])
        product = [[0] * number_customers for _ in range(number_producents)]

        for i in range(number_producents):
            for j in range(number_customers):
                if (customers[i][j] > 0):
                    product[i][j] = round(price[i][j] * customers[i][j] + distance[i][j] * 0.45, 2)
                    
                else:
                    product[i][j] = 0
              
        return product


        

producentA = Producents(1, [random.randint(50, 100) for i in range(4)], [round(random.uniform(0.0, 100.0), 2) for i in range(4)])
producentB = Producents(2, [random.randint(50, 100) for i in range(4)], [round(random.uniform(0.0, 100.0), 2) for i in range(4)])
producentC = Producents(3, [random.randint(50, 100) for i in range(4)], [round(random.uniform(0.0, 100.0), 2) for i in range(4)])
producentD = Producents(4, [random.randint(50, 100) for i in range(4)], [round(random.uniform(0.0, 100.0), 2) for i in range(4)])

customerA = Customers(1, [random.randint(0, 50) for i in range(4)])
customerB = Customers(2, [random.randint(0, 50) for i in range(4)])
customerC = Customers(3, [random.randint(0, 50) for i in range(4)])
customerD = Customers(4, [random.randint(0, 50) for i in range(4)])

matrix_producent = [producentA.quantity, producentB.quantity, producentC.quantity, producentD.quantity]
matrix_customer = [customerA.demand, customerB.demand, customerC.demand, customerD.demand]
matrix_price = [producentA.price, producentB.price, producentC.price, producentD.price]
distance = [[round(random.uniform(0.0, 10.0), 2) for i in range(4)] for j in range(4)]

bee1 = Bee(matrix_producent, matrix_customer, distance, matrix_price)
product = bee1.generate_solution(bee1.producents, bee1.customers, bee1.distance, bee1.price)
for row in product:
    print(row)
    

#przykladowy producent 
#producent1 = Producents(1, [random.randint(0, 100) for i in range(5)], [round(random.uniform(0.0, 100.0), 2) for i in range(5)])
# wynik 1 [52, 60, 72, 49, 73] [30.95, 28.44, 36.31, 82.93, 61.77]
#gdzie odpowiednio mamy id producenta, liste ilosci produktow produkowanych oraz liste cen dla danego produktu


