#!C:\Python36/python.exe
# -*- coding: utf-8 -*-

from flask import *
import os
from Clusters import ultimaTormenta


app = Flask(__name__)
app.secret_key = 'IA'

UPLOAD_FOLDER = 'static/archivos'
ALLOWED_EXTENSIONS = set(['txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:

            return render_template('index.html')

        f = request.files['file']
        if f.filename == '':
            flash('No selecciono ningun archivo')
            return render_template('index.html')

        if f and allowed_file(f.filename):
            filename = "newdataset.txt"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('DataSet Cargado Correctamente')
            return render_template('clasificar.html')
        else:
            flash('Tipo de archivo incorrecto')
            return render_template('index.html')
    return render_template('index.html')



@app.route('/clasificar', methods=['GET', 'POST'])
def clasificar():
    global solution
    if request.method == 'POST':
        cantidadIteraciones = int(request.form.get('cantIteraciones'))
        tamanoIndividuo = int(request.form.get('cantClases'))
        solution = ultimaTormenta.mainApp(cantidadIteraciones,tamanoIndividuo)
    return render_template('clasificar.html', solution=solution)

# def analizar():
#     if request.method == 'POST':
#         cantidadGeneraciones = int(request.form.get('cantGen'))
#         cantidadIndividuos = int(request.form.get('cantInd'))
#         cantClusters = int(request.form.get('cantClus'))
#         metodoSeleccion = str(request.form.get('metSeleccion'))
#         porcentajeSeleccion = int(request.form.get('porcSeleccion'))
#         porcentajeElitista = int(request.form.get('porcElitista'))
#         cantRanuras = int(request.form.get('cantRanuras'))
#         porcentajeCruza = int(request.form.get('porcCruza'))
#         puntoCruza = int(request.form.get('puntCruza'))
#         probMutacion = float(request.form.get('probabMutacion'))
#         arreglo = funcionGeneralParaGraficar(int(2),cantidadGeneraciones,cantidadIndividuos,cantClusters,porcentajeSeleccion,metodoSeleccion,porcentajeElitista,cantRanuras,porcentajeCruza,puntoCruza,probMutacion)
#     return render_template('inicial.html', arreglo = arreglo)
#     #return render_template('inicial.html', arreglo = array[1])

if __name__ == "__main__":
    app.run(debug = True, port = 5000)
