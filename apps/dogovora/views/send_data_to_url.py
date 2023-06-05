import json
import requests


def send_data_to_url_b24(froze, dogovor):
    """Функция обновляет заявку на Б24 по url"""

    # Создаём словарь для следующего создания словаря JSON
    froze_param = dict()
    froze_param['uuid'] = froze.uuid
    froze_param['name'] = froze.name
    froze_param['phone'] = froze.phone
    froze_param['owner'] = froze.owner.id
    froze_param['type_production'] = froze.type_production
    froze_param['total_amount'] = dogovor.vsego_k_oplate
    froze_param['type_pay'] = froze.type_pay
    froze_param['nomer_dogovora'] = dogovor.nomer_dogovora
    froze_param['adres_propiski'] = dogovor.adres_propiski
    froze_param['oplata_predoplata_rub'] = dogovor.oplata_predoplata_rub
    froze_param['naimenov_soputstv_izdeliy'] = dogovor.naimenov_soputstv_izdeliy
    froze_param['summa_za_soputstv_uslugi'] = dogovor.summa_za_soputstv_uslugi
    froze_param['vsego_k_oplate'] = dogovor.vsego_k_oplate
    froze_param['data_podpisaniya'] = dogovor.data_podpisaniya.strftime('%Y-%m-%d')
    froze_param['srok_ispolneniya_rabot'] = dogovor.srok_ispolneniya_rabot
    froze_param['tip_dogovora'] = dogovor.tip_dogovora
    # url = f'https://re-forma-ru.bitrix24.ru/crm/deal/details/{froze.uuid}/'
    url = f'https://sell-us.pro/clients/re-forma-ru/{froze.uuid}/get_data.php'

    # Преобразуем словарь в формат JSON
    json_data = json.dumps(froze_param)
    # Отправляем PUT-запрос с данными в формате JSON на указанный URL
    response = requests.put(url, json=json_data)
    # Возвращаем ответ сервера
    return response

