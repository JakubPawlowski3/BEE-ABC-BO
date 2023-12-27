import numpy as np
import random

def wypelnienie(ograniczenia, produkcja, n, wymiar1, wymiar2):
    macierze = []

    while len(macierze) < n:
        matrix = np.zeros((wymiar1, wymiar2), dtype=int)

        for j in range(wymiar1):
            value = ograniczenia[j]
            for i in range(wymiar2):
                if i == wymiar2 - 1:
                    a = produkcja[i] - np.sum(matrix[:j, i])
                    if value <= a:
                        matrix[j, i] = value
                    else:
                        break  # Przerwanie pętli w przypadku braku dopuszczalnej macierzy
                else:
                    x = random.randint(0, min(value, produkcja[i] - np.sum(matrix[:j, i])))
                    matrix[j, i] = x
                    value -= x
            else:
                continue
            break

        else:
            # Ta część kodu zostanie wykonana, jeśli pętla zakończy się naturalnie (bez przerwania)
            macierze.append(matrix)

    return macierze

n = 5  # Liczba macierzy do wygenerowania
ograniczenia = [20, 30, 40,12]
produkcja = [26, 35, 32,35]
wyniki = wypelnienie(ograniczenia, produkcja, n, 4, 4)

for i, result in enumerate(wyniki):
    print(f"Macierz {i + 1}:")
    print(result)
    print()


