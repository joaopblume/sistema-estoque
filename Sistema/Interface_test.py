from PyQt5 import uic, QtWidgets
import mysql.connector

# conectando com localhost mysql
banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='cadastro_produtos'
)

def excluir():
    linha = storage.tableWidget.currentRow() 
    id = storage.tableWidget.item(linha, 0).text()

    cursor = banco.cursor()
    comando = f'DELETE FROM produtos WHERE id = {id}'
    cursor.execute(comando)
    banco.commit()
    
    storage.tableWidget.removeRow(linha)

def quantity():
    sell.show()

    linha = storage.tableWidget.currentRow()
    total = int(storage.tableWidget.item(linha, 5).text())
    sell.spinBox.setRange(1 , int(total))

    sell.pushButton.clicked.connect(confirmar)

    return total
    

def confirmar():

    linha = storage.tableWidget.currentRow() 
    id = storage.tableWidget.item(linha, 0).text()

    valor = int(sell.spinBox.value())
    resultado = quantity() - valor
    if resultado == 0:
        excluir()
    else:
        cursor = banco.cursor()
        comando = f'UPDATE produtos SET quantidade = {resultado} WHERE id = {id}'
        cursor.execute(comando)
        banco.commit()
        storage.tableWidget.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(resultado)))
    
    sell.close()
    return resultado


def registrar():
# captando os dados inseridos nas labels
    nome = new.lineEdit.text()
    tipo = new.comboBox.currentText()
    preco = new.lineEdit_2.text()
    codigo = new.lineEdit_3.text()
    quantidade = new.lineEdit_4.text()


# passando os dados captados para uma tabela na db
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

    storage.tableWidget.verticalHeader().setVisible(False)

# pegando todos os produtos já cadastrados no banco de dados
    cursor = banco.cursor()
    comando = 'SELECT * FROM produtos'
    cursor.execute(comando)
    dados_lidos = cursor.fetchall()

# definindo tamanho das linhas e colunas da tabela
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

# botão excluir e vender
    storage.pushButton.clicked.connect(excluir)
    storage.pushButton_2.clicked.connect(quantity)



app = QtWidgets.QApplication([])

# import das interfaces
index = uic.loadUi('index.ui')
new = uic.loadUi('novo_instrumento.ui')
storage = uic.loadUi('estoque.ui')
sell = uic.loadUi('vender.ui')

# definindo funções para os botões de index.ui
index.pushButton.clicked.connect(novo_instrumento)
index.pushButton_2.clicked.connect(estoque)

index.show()
app.exec()
