import numpy as np
import random
from users import *
from obj import *

products = ["A", "B", "C", "D"]
bee1 = Bee(matrix_producent, matrix_customer, distance, matrix_price, 4)
new1 = np.transpose(bee1.customers)
new2 = np.transpose(bee1.producents)
product = bee1.generate_matrix_production(new1[0], new2[0], 20, 4, 4)
print("Macierz Producentow")
for row in matrix_producent:
    print(row)
print("\n")
print("Macierz klientow")
for row in matrix_customer:
    print(row)
print("\n")
# for i in range(len(product)):
#     print(f"Macierz produktu {products[i]}")
#     for j in range(len(product[i])):
        
#         print(product[i][j])
    
#     print("\n")

for i, result in enumerate(product):
    print(f"Macierz {i + 1}:")
    print(result)
    print()





