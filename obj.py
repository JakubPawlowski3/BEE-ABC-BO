import random


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
        cost = [[0] * number_customers for _ in range(number_producents)]
        product = [[0] * number_customers for _ in range(number_producents)]        

        for i in range(number_producents):
            for j in range(number_customers):
                if (customers[i][j] > 0):
                    cost[i][j] = round(price[i][j] * customers[i][j] + distance[i][j] * 0.45, 2)
                    product[i][j] = customers[i][j]
                    
                else:
                    cost[i][j] = 0
              
        return cost, product


        
