import requests
import config

# Получаем ид сотрудника для ерпа
async def get_id_erp(tel_id):
    url = config.URL_AUTH + str(tel_id)
    response = requests.get(url=url).json()
    if response['status'] != 'ok':
        return False
    url = config.GET_GROUP + str(response['data'][0]['id'])
    response1 = requests.get(url=url).json()
    return [response['data'][0]['title'], response1['data'][0]['value']]
