import pandas as pd
import numpy as np



producenci=np.array([[35,21,33],[29,44,26],[1000,22,23]])
klienci=np.array([[21,33,32],[33,32,23],[25,22,22]])
cena=np.array([[10,4,5],[1,7,4],[1000,2,5]])
dystans = [[5, 22, 11], [100, 55, 30], [22, 10, 15]]

data = {
    'producenci': producenci.flatten(),
    'klienci': klienci.flatten(),
    'cena': cena.flatten(),
    'dystans': dystans.flatten()
}

df = pd.DataFrame(data)
df.to_csv('Dataframe')
value = pd.read_csv('Dataframe')