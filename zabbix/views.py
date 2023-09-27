from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pyzabbix import ZabbixAPI
from zabbix.func import recebe_host, disponibilidade, data_final, data_inicial
from datetime import datetime




# Create your views here.


def index(request):

    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        
    except Exception as e:
        print("Erro ao fazer login:", e)

    incidents = zapi.trigger.get(
        only_true=1,
        skipDependent=1,
        monitored=1,
        active=1,
        output='extend',
        expandData='1',
        selectHosts=['host'],
        sortfield=['priority', 'lastchange'],
        sortorder='DESC'
    )
    return render(request, 'index.html', {'incidents': incidents})


def hosts_por_grupo(request):
    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        
    except Exception as e:
        print("Erro ao fazer login:", e)

    # conectar ao zabbix
    
    grupos = zapi.hostgroup.get(output=["name", "groupid"])

    #Recebe o valor do id do host que o usuario selecionou
    host = request.GET.get('hosts')
    recebe_host(host)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #Recebe as datas que foram selecionadas
    dataInicio = request.GET.get('data_inicial')
    dataFim = request.GET.get('data_final')
  
    testeinicio = dataInicio
    testefim = dataFim

    if testeinicio:
        data = datetime.strptime(dataInicio, '%Y-%m-%dT%H:%M')
        data_hora_formatada = data.strftime('%d/%m/%Y %H:%M')
        resultado = data_inicial(data_hora_formatada)
    else:
        data_hora_formatada = "20/09/2023 15:20"
    if testefim:
        dataFinal = datetime.strptime(dataFim, '%Y-%m-%dT%H:%M')
        data_hora_formatada_fim = dataFinal.strftime('%d/%m/%Y %H:%M')
        resultado_final = data_final(data_hora_formatada_fim)
    else:
        data_hora_formatada_fim = "21/09/2023 15:20"
    
    


  
    contexto = {
        "grupos" : grupos     
    }
   
    return render(request, "hosts.html", contexto)



def obter_hosts_por_grupo(request, grupo):
    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
     
    except Exception as e:
        print("Erro ao fazer login:", e)


    # Obter hosts do grupo

    hosts = zapi.host.get(output=["hostid", "name"], groupids=grupo)
 
    

    # Extrair nomes dos hosts
    #nomes_hosts = [host['host'] for host in hosts]

    return JsonResponse({'hosts': hosts})


def disponibilidade_selecionada(request):
    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        
    except Exception as e:
        print("Erro ao fazer login:", e)

    grupos = zapi.hostgroup.get(output=["name", "groupid"])
    avail_data = disponibilidade()
    contexto = {
        "avail_data" : avail_data,  
        "grupos" : grupos   
    }
   
    return render(request, "hosts.html", contexto)
    

