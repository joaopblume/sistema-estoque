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
    print(f'Nome: {nome}')
    print(f'Tipo: {tipo}')
    print(f'Preço: R${preco}')
    print(f'Código: {codigo}')
    print(f'Quantidade: {quantidade}')

    cursor = banco.cursor()
    comando = 'INSERT INTO produtos (nome, tipo, preco, codigo, quantidade) VALUES (%s, %s, %s, %s, %s)'
    dados = (nome, tipo, str(preco), str(codigo), str(quantidade))
    cursor.execute(comando, dados)
    banco.commit()

    new.close()
    

def novo_instrumento():
    new.pushButton.clicked.connect(registrar)
    new.show()


app = QtWidgets.QApplication([])
index = uic.loadUi('index.ui')
new = uic.loadUi('novo_instrumento.ui')
index.pushButton.clicked.connect(novo_instrumento)

index.show()
app.exec()
