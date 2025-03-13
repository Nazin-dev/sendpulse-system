from send.scripts.redis_client import redis_client
from send.scripts import clients, api

def run_campaigns():
    """
    Busca todas as campanhas ativas e, para cada uma, envia a mensagem da campanha para os clientes
    que ainda não foram removidos (filtrados pelo ID da campanha).
    """
    campaign_keys = redis_client.keys("campaign:*")
    
    for key in campaign_keys:
        data = redis_client.hgetall(key)
        campaign = {k.decode(): v.decode() for k, v in data.items()}
        
        # Extrai o campaign_id a partir da chave (que tem o formato "campaign:<id>")
        campaign_id = key.decode().split(":")[1]
        
        if campaign.get("status") != "active":
            continue
        
        try:
            dias = int(campaign.get("dias", 0))
        except ValueError:
            dias = 0
        
        message = campaign.get("message", "")
        
        # Passa o campaign_id para filtrar os clientes excluídos para essa campanha
        clientes_list = clients.get_clientes(dias, campaign_id)
        
        phone_numbers = []
        for cliente in clientes_list:
            telefone = cliente['telefone'].strip()
            if not telefone.startswith('+55'):
                telefone = '+55' + telefone
            phone_numbers.append(telefone)
        
        if phone_numbers:
            api.send_sms(phone_numbers, message)
