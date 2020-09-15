from PyQt5 import uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='cadastro_produtos'
)

def registrar():
    nome = new.lineEdit.text()
    tipo = new.comboBox.currentText()
    preco = new.lineEdit_2.text()
    codigo = new.lineEdit_3.text()
    quantidade = new.lineEdit_4.text()
   
    cursor = banco.cursor()
    comando = 'INSERT INTO produtos (nome, tipo, preco, codigo, quantidade) VALUES (%s, %s, %s, %s, %s)'
    dados = (nome, tipo, str(preco), str(codigo), str(quantidade))
    cursor.execute(comando, dados)
    banco.commit()

    new.close()
    

def novo_instrumento():
    new.pushButton.clicked.connect(registrar)
    new.show()


def estoque():
    storage.show()

    cursor = banco.cursor()
    comando = 'SELECT * FROM produtos'
    cursor.execute(comando)
    dados_lidos = cursor.fetchall()

    storage.tableWidget.setRowCount(len(dados_lidos))
    storage.tableWidget.setColumnCount(6)

# ajustando tamanho das células
    widths = [30, 140, 90, 80, 80, 80]
    for i, width in enumerate(widths):
        storage.tableWidget.setColumnWidth(i, width)

# dando nomes às colunas
    values = ['id', 'Nome', 'Tipo', 'Preço', 'Código', 'Quantidade']
    storage.tableWidget.setHorizontalHeaderLabels(values)

# selecionando uma linha ao invés de selecionar apenas uma célula
    storage.tableWidget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

# adicionando os valores às células
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            storage.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])
index = uic.loadUi('index.ui')
new = uic.loadUi('novo_instrumento.ui')
storage = uic.loadUi('estoque.ui')
index.pushButton.clicked.connect(novo_instrumento)
index.pushButton_2.clicked.connect(estoque)

index.show()
app.exec()
