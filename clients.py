import mysql.connector
mydb = mysql.connector.connect(
    host="192.168.0.55",
    port=3306,
    user="eacadm",
    password="N3rus@3acadm",
    database="sqldados")

mycursor = mydb.cursor()

sql = '''select 
	          itxa.contrno as contrato, 
            date_format(itxa.duedate, "%d/%m/%Y") as vencimento,
            inst.custno as codigo_cliente,
            custp.name as nome_cliente,
            concat(mid(custp.ddd, 1, 2), mid(custp.tel, 1, 9)) as telefone
        from 
	        itxa 
        left join inst on inst.contrno = itxa.contrno
        left join custp on custp.no = inst.custno
        where duedate = curdate() + 2;'''

mycursor.execute(sql)

nomes_colunas = mycursor.column_names

data = mycursor.fetchall()

clientes = []

for c in data:
  dicionario = dict(zip(nomes_colunas, c))
  if len(dicionario['telefone'].replace(' ','')) >= 11:
    clientes.append(dicionario)

print("✅ Executado com Sucesso: clients.py")