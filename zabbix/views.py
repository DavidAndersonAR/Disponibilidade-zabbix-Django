from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pyzabbix import ZabbixAPI
from zabbix.func import recebe_host, disponibilidade, data_final, data_inicial, horario_disponibilidade
from datetime import datetime





# Create your views here.


def index(request):

    try:
        zapi = ZabbixAPI("http://seu servidor do zabbix/zabbix")
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
        zapi = ZabbixAPI("http://seu servidor do zabbix/zabbix")
        zapi.login("Admin", "zabbix")
        
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
        zapi = ZabbixAPI("http://seu servidor do zabbix/zabbix")
        zapi.login("Admin", "zabbix")
     
    except Exception as e:
        print("Erro ao fazer login:", e)


    # Obter hosts do grupo

    hosts = zapi.host.get(output=["hostid", "name"], groupids=grupo)
 
    

    # Extrair nomes dos hosts
    #nomes_hosts = [host['host'] for host in hosts]

    return JsonResponse({'hosts': hosts})


def disponibilidade_selecionada(request):
    try:
        zapi = ZabbixAPI("http://seu servidor do zabbix/zabbix")
        zapi.login("Admin", "zabbix")
        
    except Exception as e:
        print("Erro ao fazer login:", e)

    grupos = zapi.hostgroup.get(output=["name", "groupid"])
    avail_data = disponibilidade()
    horario_data = horario_disponibilidade()
    contexto = {
        "avail_data" : avail_data,  
        "grupos" : grupos,
        "horario_data" : horario_data,
    }
    print(avail_data)
   
    return render(request, "hosts.html", contexto)
    



# def obter_dados_grafico_zabbix():
#     # Conectar-se à API Zabbix
#     try:
#         zapi = ZabbixAPI("http://seu servidor do zabbix/zabbix")
#         zapi.login("Admin", "26143024")
        
#     except Exception as e:
#         print("Erro ao fazer login:", e)

#     # Obtendo o timestamp atual e o timestamp de duas horas atrás
#     agora = int(time.time())  
#     duas_horas_atras = agora - (2 * 3600)  

#     # ID do host para o qual você deseja obter o gráfico
#     host_id = 15485

#     # ID do item do gráfico desejado
#     item_id = 211027

#     # Obter dados do gráfico
#     grafico_dados = zapi.history.get(itemids=item_id, time_from=duas_horas_atras, time_till=agora, output='extend')

  

#     return grafico_dados


# from django.shortcuts import render
# from django.http import HttpResponse
# import requests

# def obter_imagem_grafico_zabbix(request):
#     # Suponha que graph_id seja o ID do gráfico que você deseja obter
#     graph_id = 22188  # Substitua pelo ID real do gráfico

#     # Construa a URL da API Zabbix para obter a imagem do gráfico
#     url_api_zabbix = 'http://seu servidor do zabbix/zabbix'
#     parametros = {
#         'graphid': graph_id,
#         'width': 800,  # Largura desejada da imagem
#         'height': 400,  # Altura desejada da imagem
#         # Adicione outros parâmetros conforme necessário
#     }

#     # Faça uma requisição para obter a imagem do gráfico
#     resposta = requests.get(url_api_zabbix, params=parametros)
#     print(resposta)

#     # Verifique se a requisição foi bem-sucedida
#     if resposta.status_code == 200:
#         # Retorne a imagem como resposta
#         return HttpResponse(resposta.content, content_type='image/png')
#     else:
#         return HttpResponse('Erro ao obter a imagem do gráfico', status=resposta.status_code)

# # No seu template Django
# def visualizar_imagem_grafico(request):
#     return render(request, 'visualizar_imagem_grafico.html')




# def obter_dados_grafico_zabbix(graph_id):
#     url_api_zabbix = 'http://seu servidor do zabbix/zabbix/api_jsonrpc.php'
    
#     # Configure o cabeçalho com o token de autenticação
#     headers = {
#         'Content-Type': 'application/json-rpc',
#     }

#     # Configure os parâmetros para obter os dados do gráfico
#     parametros = {
#         'jsonrpc': '2.0',
#         'method': 'graph.get',
#         'params': {
#             'output': 'extend',
#             'graphids': graph_id,
#         },
#         'auth': '59f940b162f83db0846574da192a476303b7dea4e5dc095d746f7b46b96a9a3f',  # Substitua pelo seu token de autenticação
#         'id': 1,
#     }

#     # Faça uma requisição para a API do Zabbix para obter os dados do gráfico
#     resposta = requests.post(url_api_zabbix, headers=headers, json=parametros)

#     # Verifique se a requisição foi bem-sucedida
#     if resposta.status_code == 200:
#         return resposta.json()
#     else:
#         print('Erro ao obter os dados do gráfico:', resposta.status_code)
#         return None



# def exibir_grafico_zabbix(request, graph_id):
#     # Obtém os dados do gráfico do Zabbix
#     dados_grafico = obter_dados_grafico_zabbix(graph_id)

#     if dados_grafico:
#         # Se os dados foram obtidos com sucesso, retorne como JSON
#         return JsonResponse(dados_grafico, safe=False)
#     else:
#         # Se houve um erro, retorne uma resposta de erro
#         return JsonResponse({'erro': 'Erro ao obter os dados do gráfico'}, status=500)

# # ... outras views ...
