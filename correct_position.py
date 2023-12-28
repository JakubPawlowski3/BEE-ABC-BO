import random
import numpy as np

def correct_position(new_bee,ograniczenia,produkcja):
    counter=0
    wiersze=np.sum(new_bee,axis=1)
    while not np.all(ograniczenia == wiersze):
        a=np.shape(new_bee)[0]
        b=np.shape(new_bee)[1]
        for i in range(a):
            for j in range(b):
                k=random.randint(0,b-1)
                roz=np.abs(ograniczenia[i]-wiersze[i])
                value=random.randint(0,roz)
                if ograniczenia[i] >= wiersze[i]:
                    if np.sum(new_bee,axis=0)[k]+value <= produkcja[k]:
                        new_bee[i,k]=new_bee[i,k]+value
                        wiersze=np.sum(new_bee,axis=1)
                        break
                if ograniczenia[i]< wiersze[i]:
                    if new_bee[i,k]-value > 0:
                        new_bee[i,k]=new_bee[i,k]-value
                        wiersze=np.sum(new_bee,axis=1)
                        break
        counter+=1
        wiersze=np.sum(new_bee,axis=1)
        if counter >= 1000:
            print("Przekroczono maksymalną liczbę iteracji. Zwracanie macierzy zer.")
            return np.zeros((a, b), dtype=int)
    return new_bee 