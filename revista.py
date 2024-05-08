from bs4 import BeautifulSoup
import requests

class Revista:
    def __init__(self, titulo:str,url:str, catalogo:str, sjr:str, q:str, h_index:str, total_citas:str, AreasyCategorias:str, publisher:str, ISSN:str, widget_code:str):
        self.titulo = titulo
        self.url = url
        self.catalogo = catalogo
        self.sjr = float(sjr)
        self.q = q
        self.h_index = int(h_index)
        self.total_citas = int(total_citas)
        self.AreasyCategorias = AreasyCategorias
        self.publisher = publisher
        self.ISSN = ISSN
        self.widget_code = widget_code


    def __str__(self):
        return f'{self.titulo} | {self.url} | {self.catalogo} | {self.sjr} | {self.q} | {self.total_citas} | {self.AreasyCategorias} | {self.publisher} | {self.ISSN} | {self.widget_code}'


def readUrl():
    with open ('urls.txt') as f:
        lineas = f.readlines()
    return lineas

def scrap(url):
    pagina = requests.get(url)
    soup=BeautifulSoup(pagina.content, 'html.parser')
    results=soup.find(class_="table_wrap")
    return results

def getDataFromTable(table):
    #[1][3 - aqui tambien esta Q][4][9]
    lista_revistas = []
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        titulo = columns[1].get_text().strip().replace(',','')

        if titulo.find('\u0113'):
            titulo = titulo.replace('\u0113', 'e')
    
        url = "https://www.scimagojr.com/"+columns[1].find('a')['href']

        pagina = requests.get(url)
        soup=BeautifulSoup(pagina.content, 'html.parser')
        table = soup.find_all('div', class_='journalgrid')

        # SUBJECT AREA AND CATEGORY
        # areas_and_categories = soup.find_all('ul', class_='treecategory')
        # for area_and_category in areas_and_categories:
        #         area_link = area_and_category.find_previous('a')
        #         area_name = area_link.get_text()
        #         list_area = []
        #         list_area.append(area_name)
        #         print(list_area)

        #         categories = area_and_category.find_all('a')
        #         for category in categories:
        #             category_name = category.get_text()
        #             list_category = []
        #             list_category.append(category_name)
        #             print(list_category)
        
        AreasyCategorias = ""
        areas_and_categories = soup.find_all('ul', class_='treecategory')
        for area_and_category in areas_and_categories:
            # Encontrar el enlace de la área
            area_link = area_and_category.find_previous('a')
            area_name = area_link.get_text().replace(',','')+ ""
            AreasyCategorias += area_name + ": "

            # Encontrar todas las categorías dentro de la lista
            categories = area_and_category.find_all('a')
            for category in categories:
                category_name = category.get_text().replace(',','') + " "
                AreasyCategorias += category_name+ "+ "
                if category == categories[-1]:                   
                    AreasyCategorias = AreasyCategorias[:-2] + "| " 
                    if area_and_category == areas_and_categories[-1]:
                        AreasyCategorias = AreasyCategorias[:-2]     

        # # PUBLISHER 
        # divs= table[0].find_all('div')
        # publisher = divs[2].get_text()
        # anchor = divs[2].find('a')
        # for a in anchor:
        #     publisher = a.get_text().replace(',','')
        

        # PUBLISHER
        for t in table:
            publisher = t.find_all('p')
            for a in publisher[2].find_all('a'):
                publisher = a.get_text().replace(',','')

        # ISSN 
        for t in table:
            titu = t.find_all('p')
            for a in titu[5]:
                ISSN = a.get_text().replace(',','')

        # WIDGET 
        for t in table:
            widget_input = soup.find('input', id='embed_code')
            if widget_input:
                widget_code = widget_input.get('value')
            else:
                print("No se encontró el widget.")


        catalogo = columns[2].get_text()

        sjr = columns[3].get_text().split(' ')[0]
        if sjr == '':
            sjr = '0'

        try :
            q = columns[3].get_text().split(' ')[1]
        except IndexError:
            q = 'N/A'

        #sjq_and_Q = columns[3].get_text()
        h_index = columns[4].get_text()
        total_citas = columns[8].get_text()
        r = Revista(titulo,url,catalogo,sjr,q,h_index,total_citas,AreasyCategorias,publisher,ISSN,widget_code)
        lista_revistas.append(r)
        print(len(lista_revistas))

    return lista_revistas

def saveToCSV(lista_revistas, savename):
    with open(savename + ".csv", 'w', encoding='utf-8') as f:
        f.write('Titulo,url,Catalogo,SJR,Q,h_index,Total Citas,Areas y Categorias,Publisher,ISSN,Widget\n')
        for revista in lista_revistas:
            f.write(f'{revista.titulo},{revista.url},{revista.catalogo},{revista.sjr},{revista.q},{revista.h_index},{revista.total_citas},{revista.AreasyCategorias},{revista.publisher},{revista.ISSN},{revista.widget_code}\n')


# def saveToJSON(lista_revistas, savename):
#     with open(savename + ".json", 'w') as f:
#         f.write('[') 
#         for revista in lista_revistas:
#             f.write('{\n') 
#             f.write(f'"Titulo": "{revista.titulo}",\n') 
#             f.write(f'"URL": "{revista.url}",\n') 
#             f.write(f'"Catalogo": "{revista.catalogo}",\n') 
#             f.write(f'"SJR": "{revista.sjr}",\n') 
#             f.write(f'"Q": "{revista.q}",\n')
#             f.write(f'"h_index": "{revista.h_index}",\n')
#             f.write(f'"Total Citas": "{revista.total_citas}",\n') 
#             f.write(f'"Area y Categoria": "{revista.AreasyCategorias}",\n') 
#             f.write(f'"Publisher": "{revista.publisher}",\n') 
#             f.write(f'"ISSN": "{revista.ISSN}",\n') 
#             f.write(f'"Widget": "{revista.widget_code}"\n') 
#             if revista != lista_revistas[-1]:
#                 f.write('},\n') 
#             else:
#                 f.write('}\n') 
#         f.write(']')
    

def main():
    firstURL = readUrl()[0]
    print(firstURL)
    pagina=scrap(firstURL)
    lista_revistas = getDataFromTable(pagina)
    for revista in lista_revistas:
        print(revista)
    saveToCSV(lista_revistas, 'datos/revistas2')
    #saveToJSON(lista_revistas, 'datos/revistas')

if __name__ == '__main__':
    main()