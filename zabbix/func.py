from pyzabbix import ZabbixAPI, ZabbixAPIException
from datetime import datetime
import time
import pytz



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
                                print(avail_data)
                          

    return avail_data
                                    
   
def horario_disponibilidade():
    
    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")

    except Exception as erro:
     print(erro)

    #data desejada
    inicio=(datetime.strptime(datainit,'%d/%m/%Y %H:%M')).strftime("%d/%m/%Y %H:%M")
    #fim="19/12/2018 00:00:00"
    fim=(datetime.strptime(datafim,'%d/%m/%Y %H:%M')).strftime('%d/%m/%Y %H:%M')

    #horario timestamp
    data_inicio=time.mktime(datetime.strptime(inicio, "%d/%m/%Y %H:%M").timetuple())
    data_fim=time.mktime(datetime.strptime(fim, "%d/%m/%Y %H:%M").timetuple())

    data_status = []
    datas_formatadas = []

    hosts = zapi.host.get(output=["hostid","name"],selectGroups="extend", selectTags="extend", hostids=host_dispo, selectInterfaces="extend")
    for host in hosts:
        host_name = host["name"]
        host_id = host["hostid"]
        item = zapi.item.get(search={"key_": "icmpping"}, output="itemid", hostids=host_id)

        #DISPONIBILIDADE
        if len(item) > 0:
            item_id= item[0]["itemid"]
            history = zapi.history.get(itemids=item_id, time_from=int(data_inicio), time_till=int(data_fim))
            for horario in history:
                data = horario["clock"]
                status = horario["value"]
                if status == "1":
                    status = "OK"
                else:
                    status = "DOWN"
                timestamp = int(data)

                # Fuso horário desejado (neste exemplo, usei o fuso horário de São Paulo)
                fuso_horario = pytz.timezone('America/Sao_Paulo')

                # Convertendo o timestamp para data e hora no fuso horário desejado
                data_hora = datetime.fromtimestamp(timestamp, tz=fuso_horario)

                horario_dispo = data_hora.strftime('%Y-%m-%d %H:%M:%S')
                # values_data = [(historico["clock"]) for historico in history]

                data_status.append({
                    "horario" : horario_dispo,
                    "status" : status
                })

            values_data = [(historico["clock"]) for historico in history]   
            for timestamp in values_data:
                    try:
                        timestamp_int = int(timestamp)
                        data_hora = datetime.fromtimestamp(timestamp_int, tz=fuso_horario)
                        datas_formatadas.append(data_hora.strftime('%Y-%m-%d %H:%M:%S'))
                    except ValueError:
                        print(f'Valor inválido para timestamp: {timestamp}')

            #print(datas_formatadas)  # Exibe as datas formatadas
            data_status.append({
                "horaio_grafico" : datas_formatadas
            })

            print(data_status)
           

    return data_status

    