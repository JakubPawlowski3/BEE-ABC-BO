import numpy as np
import random
from users import *
from obj import *

products = ["A", "B", "C", "D"]
bee1 = Bee(matrix_producent, matrix_customer, distance, matrix_price, 4)
product = bee1.generate_solution(bee1.producents, bee1.customers, bee1.distance, bee1.price, 4)
for row in matrix_producent:
    print(row)
print("\n")
for row in matrix_customer:
    print(row)
print("\n")
for i in range(len(product)):
    print(f"Macierz produktu {products[i]}")
    for j in range(len(product[i])):
        
        print(product[i][j])
    
    print("\n")




