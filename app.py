#!C:\Python36/python.exe
# -*- coding: utf-8 -*-

from flask import *
import os
from Modules import genetic

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
            flash('No seleccionó ningún archivo')
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
    global solution, opcion1
    opcion1 = False

    if request.method == 'POST':
        cantidadIndividuos = int(request.form.get('cantidadIndividuos'))
        cantidadIteraciones = int(request.form.get('cantIteraciones'))
        tamanoIndividuo = int(request.form.get('cantClases'))
        dimx = int(request.form.get('dimension1')) - 1
        dimy = int(request.form.get('dimension2')) - 1
        porcSeleccion = int(request.form.get('porcSeleccion'))
        porcCruza = int(request.form.get('porcCruza'))
        porcMutacion = int(request.form.get('porcMutacion'))
        if (cantidadIndividuos<10):
            flash('Error!! Los parametros ingresados son incorrectos, por favor lea los tips antes de ingresar')
            return render_template('clasificar.html')

        if (porcMutacion == 0 or porcCruza ==0 or porcSeleccion==0):
            flash('Error!! no puede haber porcentajes vacios! Sino no estaría aplicando un Operador fundamental del Algoritmo!!')
            return render_template(('clasificar.html'))
        if (porcMutacion+porcCruza+porcSeleccion) != 100:
            flash('Error!!Los porcentajes tienen que dar suma igual a 100')
            return render_template(('clasificar.html'))
        if (cantidadIndividuos < 10):
            flash('Error!!, el tamaño de la población mínimo es de 10 individuos!!')
            return render_template(('clasificar.html'))
        if request.form.get("op1"):
            opcion1 = True
        # solution = genetic.mainApp(cantidadIteraciones,tamanoIndividuo,dimx,dimy,opcion1)

        solution = genetic.mainApp(cantidadIndividuos,cantidadIteraciones,tamanoIndividuo,dimx,dimy,opcion1,porcSeleccion,porcCruza,porcMutacion)
    return render_template('clasificar.html', solution=solution)


if __name__ == "__main__":
    app.run(debug=True, port=5000)