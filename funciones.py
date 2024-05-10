# Duate Ruiz Jorge Luis
# Martínez Haro Kevin Xandé
# Proyecto Final DS4 - 09/05/2024

import csv
import unicodedata


def carga_csv(nombre_archivo:str)->list:
    '''
    Carga archivo csv y regresa una lista 
    '''
    lista = []
    with open(nombre_archivo,'r',encoding="utf-8") as archivo:
        lista = list(csv.DictReader(archivo))
    return lista

def crea_diccionario_revistas(lista_revistas:list)->dict:
    d = {}
    for revista in lista_revistas:
        key = revista["Titulo"]
        d[key] = revista
    return d

def crea_diccionario_alfabetico(lista_revistas:list)->dict:
    d = {}
    for revista in lista_revistas:
        key = revista["Titulo"][0].upper()
        if key in d:
            d[key].append(revista)
        else:
            d[key] = [revista]
        for key in d:
            d[key] = sorted(d[key], key=lambda x: x["Titulo"])
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}
    return d

def main():
    lista = carga_csv("datos/revistas.csv")
    d = crea_diccionario_revistas(lista)
    print(d)
    d = crea_diccionario_alfabetico(lista)
    print(d)

if __name__ == "__main__":
    main()


    



        
