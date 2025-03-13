from send.scripts.redis_client import redis_client
from send.scripts import clients, api

def run_campaigns():
    """
    Busca todas as campanhas ativas e, para cada uma, envia a mensagem da campanha para os clientes
    que ainda não foram removidos.
    """
    campaign_keys = redis_client.keys("campaign:*")
    
    for key in campaign_keys:
        data = redis_client.hgetall(key)
        campaign = {k.decode(): v.decode() for k, v in data.items()}
        
        if campaign.get("status") != "active":
            continue
        
        try:
            dias = int(campaign.get("dias", 0))
        except ValueError:
            dias = 0
        
        message = campaign.get("message", "")
        clientes_list = clients.get_clientes(dias)
        
        phone_numbers = []
        for cliente in clientes_list:
            telefone = cliente['telefone'].strip()
            if not telefone.startswith('+55'):
                telefone = '+55' + telefone
            phone_numbers.append(telefone)
        
        if phone_numbers:
            api.send_sms(phone_numbers, message)
