import mysql.connector

# Conjunto global de códigos de clientes “excluídos” apenas em memória
excluded_codes = set()

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
        # Filtra números de telefone “incompletos”
        if len(dicionario['telefone'].replace(' ', '')) >= 11:
            # Verifica se esse codigo não está no conjunto de excluidos
            if dicionario['codigo_cliente'] not in excluded_codes:
                clientes.append(dicionario)

    mydb.close()
    return clientes

def remove_from_clientes(codigo_cliente):
    """
    Marca o código do cliente como 'excluído' em memória.
    """
    excluded_codes.add(codigo_cliente)

print("✅ Executado com Sucesso: clients.py")
