from pyzabbix import ZabbixAPI, ZabbixAPIException
from datetime import datetime, timedelta
import time


def recebe_host(host):
    global host_dispo
    host_dispo = host
   

    print(f"Esse é para tratar fora do frontEnd {host}")

def disponibilidade():


    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        #print(f"Conectado dispo_host, {zapi.api_version()}")

    except Exception as erro:
     print(erro)


    # #data desejada
    # #inicio="06/07/2022 00:00:00"
    # inicio=(datetime.strptime(data,'%d/%m/%Y %H:%M')).strftime("%d/%m/%Y %H:%M")

    # #fim="19/12/2018 00:00:00"
    # fim=(datetime.strptime(final,'%d/%m/%Y %H:%M')).strftime('%d/%m/%Y %H:%M')

    # #horario timestamp
    # data_inicio=time.mktime(datetime.strptime(inicio, "%d/%m/%Y %H:%M").timetuple())
    # data_fim=time.mktime(datetime.strptime(fim, "%d/%m/%Y %H:%M").timetuple())



    
    avail_data = []

    hosts = zapi.host.get(output=["hostid","name"],selectGroups="extend", selectTags="extend", hostids=host_dispo, selectInterfaces="extend")
    print(f"Aqui é a chamada da função disponibilidade. {hosts}")

    return avail_data
    ...
