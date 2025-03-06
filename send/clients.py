import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="192.168.0.55",
        port=3306,
        user="eacadm",
        password="N3rus@3acadm",
        database="sqldados"
    )

def get_clientes(dias):
    mydb = get_connection()
    mycursor = mydb.cursor()

    # Utilize parâmetros para evitar SQL injection.
    sql = '''
    SELECT 
        itxa.contrno AS contrato, 
        DATE_FORMAT(itxa.duedate, "%d/%m/%Y") AS vencimento,
        inst.custno AS codigo_cliente,
        custp.name AS nome_cliente,
        CONCAT(MID(custp.ddd, 1, 2), MID(custp.tel, 1, 9)) AS telefone
    FROM 
        itxa 
    LEFT JOIN inst ON inst.contrno = itxa.contrno
    LEFT JOIN custp ON custp.no = inst.custno
    WHERE duedate = CURDATE() + %s;
    '''
    mycursor.execute(sql, (dias,))
    nomes_colunas = mycursor.column_names
    data = mycursor.fetchall()

    clientes = []
    for c in data:
        dicionario = dict(zip(nomes_colunas, c))
        if len(dicionario['telefone'].replace(' ', '')) >= 11:
            clientes.append(dicionario)

    mydb.close()
    return clientes


print("✅ Executado com Sucesso: clients.py")