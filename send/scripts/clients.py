import mysql.connector
from send.scripts.redis_client import redis_client

def get_connection():
    return mysql.connector.connect(
        host="192.168.0.55",
        port=3306,
        user="eacadm",
        password="N3rus@3acadm",
        database="sqldados"
    )

def get_excluded_codes(campaign_id):
    """
    Retorna um conjunto com os códigos de clientes excluídos para a campanha especificada,
    armazenados na chave "excluded_clients:<campaign_id>" no Redis.
    """
    codes = redis_client.smembers(f"excluded_clients:{campaign_id}")
    return {code.decode().strip() for code in codes}

def get_clientes(dias, campaign_id=None):
    """
    Retorna a lista de clientes filtrados pelo intervalo de dias,
    excluindo os clientes que foram removidos para a campanha informada (se campaign_id for fornecido).
    Se campaign_id for None, retorna todos os clientes.
    """
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
        WHERE duedate = DATE_ADD(CURDATE(), INTERVAL %s DAY)
          AND itxa.status NOT IN (1, 5)
          AND custp.freeFld1 NOT IN (8631, 8633, 8629, 8630);
    '''
    mycursor.execute(sql, (dias,))
    nomes_colunas = mycursor.column_names
    data = mycursor.fetchall()
    clientes = []

    if campaign_id is not None:
        excluded_codes = get_excluded_codes(campaign_id)
    else:
        excluded_codes = set()

    for c in data:
        dicionario = dict(zip(nomes_colunas, c))
        if len(dicionario['telefone'].replace(' ', '')) >= 11:
            codigo_cliente = str(dicionario['codigo_cliente']).strip()
            if codigo_cliente not in excluded_codes:
                clientes.append(dicionario)
    
    mydb.close()
    return clientes

def remove_from_clientes(codigo_cliente, campaign_id):
    """
    Registra que o código do cliente foi removido para a campanha especificada,
    adicionando-o no conjunto armazenado em Redis.
    """
    code = str(codigo_cliente).strip()
    redis_client.sadd(f"excluded_clients:{campaign_id}", code)

print("✅ Executado com Sucesso: clients.py")
