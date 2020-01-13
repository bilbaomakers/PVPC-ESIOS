import requests
import json
import statistics

## PREPARAR LA LLAMADA A LA API
url = 'https://api.esios.ree.es/indicators/10229'
headers = {'Accept':'application/json; application/vnd.esios-api-v2+json','Content-Type':'application/json','Host':'api.esios.ree.es','Authorization':'Token token=\"MITOKEN\"'}

## HACER LA PETICION
response = requests.get(url, headers=headers)

## Si la respuesta es 200 (OK)
if response.status_code == 200:

  bajomedia =  0

  ## CONVERTIR A DISCCIONARIO PYTHON
  json_data = json.loads(response.text)

  ## QUEDARME CON EL LISTADO DE VALORES SOLO
  valores = json_data['indicator']['values']


  ## SACAR DENTRO DEL LISTADO DE VALORES SOLO EL PRECIO
  precios = [x['value'] for x in valores]
  ## SACAR MAX MIN Y MED DEL LISTADO DE VALORES
  valor_min = min(precios)
  valor_max = max(precios)
  valor_med = statistics.median(precios)

  ## Recorrer los objetos Para sacar el valor actual
  from datetime import datetime
  for t_valor in valores:
    t_valor_date = datetime.fromisoformat(t_valor['datetime'])
    if t_valor_date.hour == datetime.now().hour:
      valor_act = t_valor['value']
      bajomedia =  valor_act < valor_med

  ## Imprimir la info por consola en formato JSON
  print ('{\"Actual\":' + str(valor_act) + ',\"Maximo\":' + str(valor_max) + ',\"Minimo\":' + str(valor_min) + ',\"Media\":' + str(valor_med) + ',\"BajoMedia\":' + str(bajomedia).lower() + '}')
