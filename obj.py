import random

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
        

        self.generate_solution(producents, customers, distance, price, number_products)
    

        
    def generate_solution(self, producents, customers, distance, price, number_products):
        number_producents = len(producents[0])
        number_customers = len(customers[0])
        cost = [[0] * number_customers for _ in range(number_producents)]
        product = [[0] * number_customers for _ in range(number_producents)]

        list_product_matrix = [] 
        for k in range(number_products):
            for i in range(number_producents):
                for j in range(number_customers):
                    if (customers[i][j] > 0):
                        product[i][j] = customers[i][j]


                    else:
                        cost[i][j] = 0
            list_product_matrix.append(product)
        

        return cost, list_product_matrix


