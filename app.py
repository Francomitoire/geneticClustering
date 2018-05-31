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
        cantidadIteraciones = int(request.form.get('cantIteraciones'))
        tamanoIndividuo = int(request.form.get('cantClases'))
        dimx = int(request.form.get('dimension1')) - 1
        dimy = int(request.form.get('dimension2')) - 1
        # lib = int(request.form.get('tipoimp'))
        if request.form.get("op1"):
            opcion1 = True

        solution = genetic.mainApp(cantidadIteraciones,tamanoIndividuo,dimx,dimy,opcion1)
    return render_template('clasificar.html', solution=solution)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
