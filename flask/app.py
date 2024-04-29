from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_mysqldb import cursors

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'lista_compras'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Nome da classe como string porque tava dando merda

mysql = MySQL(app)

#repository pattern

class ItemRepository:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_items(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM itens")
        lista_de_compras = cursor.fetchall()
        cursor.close()
        return lista_de_compras

    def add_item(self, descricao):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO itens (descricao) VALUES (%s)", [descricao])
        self.mysql.connection.commit()
        cursor.close()

    def remove_item(self, id_item):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM itens WHERE id = %s", (id_item,))
        self.mysql.connection.commit()
        cursor.close()

    def get_item_by_id(self, id_item):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM itens WHERE id = %s", (id_item,))
        item = cursor.fetchone()
        cursor.close()
        return item

    def update_item(self, id_item, descricao):
        cursor = self.mysql.connection.cursor()
        cursor.execute("UPDATE itens SET descricao = %s WHERE id = %s", (descricao, id_item))
        self.mysql.connection.commit()
        cursor.close()

item_repository = ItemRepository(mysql)

# Rotinha para exibir a lista de compras
@app.route('/')
def index():
    lista_de_compras = item_repository.get_all_items()
    return render_template('index.html', lista_de_compras=lista_de_compras)

# Rotinha para adicionar um novo item
@app.route('/adicionar', methods=['POST'])
def adicionar():
    descricao = request.form.get('item')
    if descricao:
        item_repository.add_item(descricao)
    return redirect(url_for('index'))

# Rotinha para remover um item
@app.route('/remover/<int:id_item>', methods=['POST'])
def remover(id_item):
    item_repository.remove_item(id_item)
    return redirect(url_for('index'))

@app.route('/editar/<int:id_item>')
def editar(id_item):
    item = item_repository.get_item_by_id(id_item)
    return render_template('editar.html', item=item)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    id_item = request.form.get('id')
    descricao = request.form.get('descricao')
    item_repository.update_item(id_item, descricao)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


''' CODIGO DO  MYSQL  :
CREATE DATABASE lista_compras;
USE lista_compras;
CREATE TABLE itens (
   id INT AUTO_INCREMENT PRIMARY KEY,
   descricao VARCHAR(255) NOT NULL
);

SELECT *
FROM itens;'''

# TMJ  BIBICIO 