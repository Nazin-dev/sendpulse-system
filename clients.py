import mysql.connector

nerus = mysql.connector.connect(
  host = "192.168.0.55",
  user = "eacadm",
  password = "N3rus@3acadm",
  database = "sqldados"
)

cursor = nerus.cursor()

cursor.execute("SELECT 'mateus'  as name, '(89)78787878' as contato, 'Rua Pedro Paixao' as endereco")

data = cursor.fetchall()

lista_clientes = list(data * 10)

clientes_dict = []

chaves = ['nome', 'telefone', 'endereco']

for c in lista_clientes:
  dicionario = dict(zip(chaves, c))
  clientes_dict.append(dicionario)
  


