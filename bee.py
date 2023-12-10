import numpy as np
import random
from users import *
from obj import *


bee1 = Bee(matrix_producent, matrix_customer, distance, matrix_price, 3)
cost, product = bee1.generate_solution(bee1.producents, bee1.customers, bee1.distance, bee1.price, 3)
for row in matrix_producent:
    print(row)
print("\n")
for i in range(len(product)):
    for j in range(len(product[i])):

        print(product[i][j])
    print("\n")




