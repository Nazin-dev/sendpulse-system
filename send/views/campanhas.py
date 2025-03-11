from django.shortcuts import render, redirect
from send.scripts.redis_client import redis_client  

def campanhas(request):
    # Busca todas as chaves que começam com "campaign:"
    campaign_keys = redis_client.keys("campaign:*")
    campaigns_list = []
    for key in campaign_keys:
        data = redis_client.hgetall(key)
        # Converte bytes para strings
        campaign = {k.decode(): v.decode() for k, v in data.items()}
        # Extrai o ID da chave (ex: de "campaign:1", extraia "1")
        campaign_id = key.decode().split(":")[1]
        campaign["id"] = campaign_id
        campaigns_list.append(campaign)
    
    context = {
        "campaigns": campaigns_list,
    }
    return render(request, "pages/campanhas.html", context)

def delete_campaign(request, campaign_id):
    """
    Deleta a campanha do Redis e remove seu ID do conjunto de campanhas.
    """
    # Deleta a chave da campanha (assumindo que ela está salva como "campaign:<id>")
    redis_client.delete(f"campaign:{campaign_id}")
    # Remove o ID da campanha do conjunto "campaigns"
    redis_client.srem("campaigns", campaign_id)
    return redirect('campanhas')

def toggle_campaign_status(request, campaign_id):
    """
    Altera o status da campanha entre 'active' e 'paused'.
    """
    key = f"campaign:{campaign_id}"
    status = redis_client.hget(key, "status")
    if status is not None:
        status = status.decode()
    else:
        # Se não existir status, assume active
        status = "active"

    # Alterna entre active e paused
    new_status = "paused" if status == "active" else "active"
    redis_client.hset(key, "status", new_status)
    return redirect('campanhas')