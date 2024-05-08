from revista import readUrl, scrap, getDataFromTable, saveToCSV

def guardardatos():
    print('Guardando datos...')
    lista_revistas = []
    for i in range(1, 585):
        url = 'https://www.scimagojr.com/journalrank.php?page=' + str(i) + '&total_size=29165'
        print(url)
        pagina=scrap(url)
        lista_revistas.append(getDataFromTable(pagina))
    lista_final = []
    for sublist in lista_revistas:
        lista_final.extend(sublist)
    saveToCSV(lista_final, 'datos/revistas')
    print('Datos guardados en datos/revistas.csv')
    #saveToJSON(lista_final, 'datos/revistas')

def main():
    guardardatos()

if __name__ == '__main__':
    main()
