from obj import *
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