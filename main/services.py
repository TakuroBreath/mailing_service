from django.core.cache import cache
from client.models import Client


def get_cached_clients():
    client_cache_key = 'clients_data_cache'
    cached_clients = cache.get(client_cache_key)

    if cached_clients:
        return cached_clients
    else:
        clients = Client.objects.all()

        cache.set(client_cache_key, clients)

        return clients
