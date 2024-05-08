from flask import Flask, render_template, request
from funciones import carga_csv, crea_diccionario_revistas, crea_diccionario_alfabetico
from datos import guardardatos
import os


if not os.path.exists("datos/revistas.csv"):
    guardardatos()

# Por defecto, se cargan los datos de revistas2.csv ya que tiene menos datos y es más rápido, pero si se desea cargar todas las revistas, nomas se debe cambiar la variable archivo_revistas a "datos/revistas.csv"
archivo_revistas = "datos/revistas2.csv"
app = Flask(__name__)
revistas = carga_csv(archivo_revistas)
diccionario_revistas = crea_diccionario_revistas(revistas)
diccionario_alfabetico = crea_diccionario_alfabetico(revistas)

diccionario_letras = ["1", "2", "3", "4", "5", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/Explorar")
def Explorar():
    return render_template("Explorar.html", diccionario_letras=diccionario_letras)


@app.route("/Explorar/<id>")
def Explorar_id(id:str):
    palabras_clave = []
    if id in diccionario_alfabetico:
        palabras_clave = sorted({revista["Titulo"].split()[0] for revista in diccionario_alfabetico[id]})
        return render_template("Explorar_id.html", id=id, palabras_clave=palabras_clave)
    else:
        return render_template("Error.html")
    
@app.route("/Explorar/<id>/<palabra>")
def Explorar_id_palabra(id:str, palabra:str):
    revistas = []
    if id in diccionario_alfabetico:
        revistas = diccionario_alfabetico[id]
        revistas = [revista for revista in revistas if revista["Titulo"].split()[0] == palabra]
        return render_template("Explorar_id_palabra.html", id=id, palabra=palabra, revistas=revistas)
    else:
        return render_template("Error.html")

@app.route("/Revista/<id>")
def revista_id(id:str):
    revista = []
    if id in diccionario_revistas:
        revista = diccionario_revistas[id]
        return render_template("Revista_id.html", revista=revista)
    else:
        return render_template("Error.html")


@app.route("/Creditos")
def Creditos():
    return render_template("Creditos.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        Term_Buscado = request.form['search']
        Revistas_Coinciden = []
        for titulo, detalles in diccionario_revistas.items():
            if titulo.lower().find(Term_Buscado.lower()) != -1:
                Revistas_Coinciden.append(detalles)
        if Revistas_Coinciden:
            return render_template("buscar.html", revistas_busqueda=Revistas_Coinciden, Term_Busc=Term_Buscado)
        else:
            return render_template("Error.html")

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    