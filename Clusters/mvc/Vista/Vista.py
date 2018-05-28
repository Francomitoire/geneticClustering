from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *


from PyQt5.QtWidgets import *


class Ui_Form(object):


#asdasdasd

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(789, 730))
        Form.setMaximumSize(QSize(789, 789))
        Form.setSizeIncrement(QSize(789, 789))
        self.actionCargaArchivo = QtWidgets.QAction(Form)
        self.actionCargaArchivo.setObjectName("actionCargaArchivo")
        self.actionGenerar_Clusters = QtWidgets.QAction(Form)
        self.actionGenerar_Clusters.setObjectName("actionGenerar_Clusters")
        self.actionTabla_de_Resultados = QtWidgets.QAction(Form)
        self.actionTabla_de_Resultados.setObjectName("actionTabla_de_Resultados")
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 30, 771, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.horizontalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(20, 20, 161, 21))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(250, 20, 161, 21))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(530, 20, 161, 21))
        self.tamPoblacion = QSpinBox(self.groupBox)
        self.tamPoblacion.setObjectName("tamPoblacion")
        self.tamPoblacion.setGeometry(QRect(140, 20, 43, 22))
        self.tamPoblacion.setMinimum(1)
        self.tamPoblacion.setMaximum(9999)
        self.cantClases = QSpinBox(self.groupBox)
        self.cantClases.setObjectName("cantClases")
        self.cantClases.setGeometry(QRect(420, 20, 43, 22))
        self.cantClases.setMinimum(1)
        self.cantClases.setValue(1)
        self.dimension1 = QSpinBox(self.groupBox)
        self.dimension1.setObjectName("dimension1")
        self.dimension1.setGeometry(QRect(650, 20, 43, 22))
        self.dimension1.setMinimum(1)
        self.dimension1.setValue(1)
        self.dimension2 = QSpinBox(self.groupBox)
        self.dimension2.setObjectName("dimension2")
        self.dimension2.setGeometry(QRect(710, 20, 43, 22))
        self.dimension2.setMinimum(2)
        self.dimension2.setMaximum(99)

        self.horizontalLayout.addWidget(self.groupBox)

        # Form.setCentralWidget(self.centralwidget)
        # self.menubar = QMenuBar(Form)
        # self.menubar.setObjectName("menubar")
        # self.menubar.setGeometry(QRect(0, 0, 789, 21))
        # Form.setMenuBar(self.menubar)
        self.menuBar = QtWidgets.QMenuBar(Form)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 789, 28))
        self.menuBar.setObjectName("menuBar")
        # MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(Form)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(62, 62))
        self.toolBar.setObjectName("toolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)



        #Form.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.actionAbrir_Archivo = QtWidgets.QAction(Form)
        self.actionAbrir_Archivo.setObjectName("actionAbrir_Archivo")

        self.actionGenerar_Clusters.setObjectName("actionGenerar_Clusters")
        self.actionGenerar_Clusters.setEnabled(True)
        self.actionTabla_de_Resultados = QtWidgets.QAction(Form)
        self.actionTabla_de_Resultados.setEnabled(True)
        self.actionTabla_de_Resultados.setObjectName("actionTabla_de_Resultados")


        self.toolBar.addAction(self.actionAbrir_Archivo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGenerar_Clusters)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTabla_de_Resultados)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

        Form.setWindowTitle(_translate("MainWindow", "Genetic Clustering"))
        self.actionAbrir_Archivo.setText(_translate("MainWindow", "Cargar Archivo"))
        self.actionGenerar_Clusters.setText(_translate("MainWindow", "Generar Clusters"))
        self.actionTabla_de_Resultados.setText(_translate("MainWindow", "Tabla de Resultados"))
        self.groupBox.setTitle(_translate("MainWindow", "Parametros de Entrada"))
        self.label.setText(_translate("MainWindow", "Tamaño de Población:"))
        self.label_2.setText(_translate("MainWindow", "Cantidad de Clases a encontrar:"))
        self.label_3.setText(_translate("MainWindow", "Dimensiones a Graficar:"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())