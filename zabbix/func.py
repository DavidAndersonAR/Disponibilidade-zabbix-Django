from pyzabbix import ZabbixAPI, ZabbixAPIException
from datetime import datetime, timedelta
import time



def data_inicial(valor):
    global datainit
    datainit = valor
   
def data_final(valor):
    global datafim
    datafim = valor
   
def recebe_host(host):
    global host_dispo
    host_dispo = host
    
def disponibilidade():


    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
      

    except Exception as erro:
     print(erro)


    #data desejada
    #inicio="06/07/2022 00:00:00"
    inicio=(datetime.strptime(datainit,'%d/%m/%Y %H:%M')).strftime("%d/%m/%Y %H:%M")

    #fim="19/12/2018 00:00:00"
    fim=(datetime.strptime(datafim,'%d/%m/%Y %H:%M')).strftime('%d/%m/%Y %H:%M')

    #horario timestamp
    data_inicio=time.mktime(datetime.strptime(inicio, "%d/%m/%Y %H:%M").timetuple())
    data_fim=time.mktime(datetime.strptime(fim, "%d/%m/%Y %H:%M").timetuple())

    avail_data = []

    hosts = zapi.host.get(output=["hostid","name"],selectGroups="extend", selectTags="extend", hostids=host_dispo, selectInterfaces="extend")
    for host in hosts:
        host_name = host["name"]
        host_id = host["hostid"]
        interface_teste = zapi.hostinterface.get(hostids=host_id, filter={"type" : 2})
        #IP = interface_teste[0]["ip"]
        item = zapi.item.get(search={"key_": "icmpping"}, output="itemid", hostids=host_id)

        #DISPONIBILIDADE
        if len(item) > 0:
            item_id= item[0]["itemid"]
            history = zapi.history.get(itemids=item_id, time_from=int(data_inicio), time_till=int(data_fim))
            values = [int(historico["value"]) for historico in history]  # Lista dos valores histórico
            quantidade_history = len(history)
            
            contador = 0
            dispo = 000

            for y in range(0, quantidade_history):
                if history[y]["value"] == "1":
                    contador = contador + 1

            if quantidade_history > 0:
                dispo = (contador / float(quantidade_history)) * 100
                primeiros_digitos = '{:.2f}'.format(dispo).replace('.', ',')

                IP = host['interfaces']
                for ipid in IP:
                    ip = ipid['ip']
                    if 'tags' in host:
                        for tag in host['tags']:
                            if tag['tag'] == 'Ambiente':
                                ambiente = tag['value']
                            elif tag['tag'] == 'SubLocal':
                                localidade = tag['value']   


                                avail_data.append({
                                    'id' : host_id,
                                    'sonda': "ENEL_BR_RJ",
                                    'localidade': localidade,
                                    'NOME': host_name,
                                    'ambiente': ambiente,
                                    'SENSOR': 'Ping',
                                    'percent_availability': primeiros_digitos,
                                    'valor' : values,
                                    'hora_inicial' : datainit,
                                    'hora_final' : datafim
                                })
                                print(f"{host_name}, {host_id}, {primeiros_digitos}, {datainit}, {datafim}")
                          

    return avail_data
                                    
   
