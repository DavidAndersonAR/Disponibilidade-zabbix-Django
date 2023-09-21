from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pyzabbix import ZabbixAPI


# Create your views here.


def index(request):

    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        print(f'Login bem-sucedido! {zapi.api_version()}')
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
        print(f'Login bem-sucedido! {zapi.api_version()}')
    except Exception as e:
        print("Erro ao fazer login:", e)

    # conectar ao zabbix
    
    grupos = zapi.hostgroup.get(output=["name", "groupid"])

    contexto = {
        "grupos" : grupos
    }
    return render(request, "hosts.html", contexto)


def obter_hosts_por_grupo(request, grupo):
    try:
        zapi = ZabbixAPI("http://10.71.1.69/zabbix")
        zapi.login("Admin", "26143024")
        print(f'Login da descoberta de hosts por grupo! {zapi.api_version()}')
    except Exception as e:
        print("Erro ao fazer login:", e)

    print(grupo)
    # Obter hosts do grupo

    hosts = zapi.host.get(output=["hostid", "name"], groupids=grupo)
    print(hosts)
    

    # Extrair nomes dos hosts
    #nomes_hosts = [host['host'] for host in hosts]

    return JsonResponse({'hosts': hosts})

