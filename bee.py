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
cena = [[90, 12, 40], [12, 14, 18], [1, 8, 9]]
dystans = [[5, 12, 4], [8, 9, 11], [12, 14, 16]]

new1 = np.transpose(klienci)
new2 = np.transpose(producenci)
#product, vector, vector_eff = bee1.generate_matrix_production(matrix_producent, new1[0], new2[0], 2, 4, 4, matrix_price, distance)
product, vector, vector_eff = bee1.generate_matrix_production(producenci, new1[0], new2[0], 2, 3, 3, cena, dystans)
# for i, result in enumerate(product):
#     print(f"Macierz {i + 1}:")
#     print(result)
#     print()
# print(f"Wektor: {vector}\n")
# print(f"Wektor efektywnosci: {vector_eff}\n")
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


# neighbour, vec, eff, counter = bee1.employee_bees(product, vector, vector_eff, new2[0], new1[0], producenci, cena, dystans)
                                                
# print("FAZA EMPLOYEE BEES-BEGIN")
# for i, result in enumerate(neighbour):
#     print(f"Macierz {i + 1}:")
#     print(result)
#     print()
# print(f"Wektor: {vec}\n")
# print(f"Wektor efektywnosci: {eff}\n")
# print("FAZA EMPLOYEE BEES-END\n")
# onlooker, vec1, eff1, counter_list1 = bee1.onlooker_bees(neighbour, vec, eff, counter, 5, new2[0], new1[0], producenci, cena, dystans)

# print("FAZA ONLOOKER BEES-BEGIN")
# for i, result in enumerate(onlooker):
#     print(f"Macierz gapi {i + 1}:")
#     print(result)
#     print()
# print(f"Wektor: {vec1}\n")
# print(f"Wektor efektywnosci: {eff1}\n")
# print("FAZA ONLOOKER BEES-END\n")

# scout, vec2, eff2, counter_list2 = bee1.scout_bees(onlooker, counter_list1, vec1, eff1, -1, producenci, new1[0], new2[0], 3, 3, cena, dystans)

# print("FAZA SCOUTOW-BEGIN")
# for i, result in enumerate(scout):
#     print(f"Macierz zwiadowcow {i + 1}:")
#     print(result)
#     print()
# print(f"Wektor: {vec2}\n")
# print(f"Wektor efektywnosci: {eff2}\n")
# print(f"Lista licznika: {counter_list2}\n")
# print("FAZA SCOUTOW-END\n")
# print("Producenci")
for row in producenci:
    print(row)
print("Kleinci")
for row in klienci:
    print(row)
print("Cena")
for row in cena:
    print(row)
print("dystans")
for row in dystans:
    print(row)

print("ABC \n")
population, vector_best, fitness_value = bee1.ABC(new1[0], producenci, new1[0], new2[0], 2, 2, 3, 3, cena, dystans, 5, 1000)
print(f"Populacja: {population}\n")
print("\n")

print("\n")
print(f"Wartosc dopasowania: {fitness_value}\n")
print("\n")