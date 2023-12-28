import numpy as np
import random
from users import *
from obj import *

products = ["A", "B", "C", "D"]
bee1 = Bee(matrix_producent, matrix_customer, distance, matrix_price, 4)

#new1 = np.transpose(bee1.customers)
#new2 = np.transpose(bee1.producents)

producenci = [[20, 30, 40], [50, 60, 20], [28, 32, 90]]
klienci = [[5, 6, 1], [22, 11, 11], [24, 26, 18]]
cena = [[6, 12, 3], [12, 14, 18], [5, 8, 9]]
dystans = [[5, 12, 4], [8, 9, 11], [12, 14, 16]]

new1 = np.transpose(klienci)
new2 = np.transpose(producenci)
#product, vector, vector_eff = bee1.generate_matrix_production(matrix_producent, new1[0], new2[0], 2, 4, 4, matrix_price, distance)
product, vector, vector_eff = bee1.generate_matrix_production(producenci, new1[0], new2[0], 2, 3, 3, cena, dystans)
# print("Macierz Producentow")
# for row in matrix_producent:
#     print(row)
# print("\n")
# print("Macierz klientow")
# for row in matrix_customer:
#     print(row)
# print("\n")
# for i in range(len(product)):
#     print(f"Macierz produktu {products[i]}")
#     for j in range(len(product[i])):
        
#         print(product[i][j])
    
#     print("\n")


print(f"Wektor: {vector}\n")
print(f"Wektor efektywnosci: {vector_eff}\n")

neighbour, vec, eff = bee1.employee_bees(product, vector, vector_eff, new2[0], new1[0], producenci, klienci, cena, dystans)

for i, result in enumerate(product):
    print(f"Macierz produktu {i + 1}:")
    print(result)
    print()

for i, result in enumerate(neighbour):
    print(f"Macierz {i + 1}:")
    print(result)
    print()
print(f"Wektor: {vec}\n")
print(f"Wektor efektywnosci: {eff}\n")


