############################################################################################################################################################
##
## PVPC-ESIOS
## Script desarrollado para consultar y procesar la informacion de Precio Voluntario para el Pequeño Consumidor en la web ESIOS de red Electrica Española
## Mas informacion sobre PVPC: https://es.wikipedia.org/wiki/Precio_voluntario_para_el_peque%C3%B1o_consumidor
##
## Desarrollado por Diego Maroto ( BilbaoMakers ) JUNIO 2021
##
## Distribuido bajo licencia GNU General Public License v3.0
##
## GITHUB: https://github.com/bilbaomakers/PVPC-ESIOS
##
############################################################################################################################################################

import requests
import json
import statistics
from datetime import datetime
import sys

# Configurar geolocalizacion del precio Mediande el GeoID: 8741 - Peninsula, 8742 - Canarias, 8743 - Baleares, 8744 - Ceuta, 8745 - Melilla
migeoid = 8741


## PREPARAR LA LLAMADA A LA API
url = 'https://api.esios.ree.es/indicators/1001'
headers = {'Accept':'application/json; application/vnd.esios-api-v2+json','Content-Type':'application/json','Host':'api.esios.ree.es','Authorization':'Token token=\"MITOKEN\"'}

## HACER LA PETICION
response = requests.get(url, headers=headers)

## Si la respuesta desde la web de ESIOS es 200 (OK)
if response.status_code == 200:

  ## Variables para uso interno
  bajomedia =  0
  proximahorabm = 0
  itemsbajomedia = int(0)
  horaejecucion = datetime.now().hour

  ## CONVERTIR A DISCCIONARIO PYTHON
  json_data = json.loads(response.text)

  ## QUEDARME CON EL LISTADO DE VALORES SOLO
  valores = json_data['indicator']['values']

  ## FILTRAR LOS VALORES POR GEOID
  valores_geoid = [x for x in valores if x['geo_id'] == migeoid ]

  ## SACAR DENTRO DEL LISTADO DE VALORES SOLO EL PRECIO
  precios = [x['value'] for x in valores_geoid ]
  ## SACAR MAX MIN Y MED DEL LISTADO DE VALORES
  valor_min = min(precios)
  valor_max = max(precios)
  valor_med = round(statistics.mean(precios),2)

  ## Recorrer los valores uno por uno para sacar la informacion que me interesa
  for t_valor in valores_geoid:
    ## Si hay parametros en la linea de comandos y concretamente es -v (solo para debug)
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
      ## Imprimir la linea por la consola
      print(t_valor)
    ## Sacar la hora del valor y convertirla a objeto datetime
    t_valor_date = datetime.fromisoformat(t_valor['datetime'])
    ## Si el precio esta por debajo de la media ...
    if t_valor['value'] < valor_med:
      ## Incremento el contador de numero de horas por debajo de la media
      itemsbajomedia += 1
      ## Si ademas es en el futuro y no he pillado aun la proxima hora bajo la media ....
      if t_valor_date.hour > horaejecucion and not proximahorabm:
        ## Me apunto en mi variable la hora 
        proximahorabm = t_valor_date
    ## Si la hora del precio es ahora
    if t_valor_date.hour == horaejecucion:
      ## Me lo apunto como valor actual
      valor_act = t_valor['value']
      ## Y pongo en la variable bajomedia true o false para saber si esta por debajo de la media
      bajomedia =  valor_act < valor_med

  ## Imprimir la info por consola en formato JSON
  print ('{\"Actual\":' + str(valor_act) + ',\"Maximo\":' + str(valor_max) + ',\"Minimo\":' + str(valor_min) + ',\"Media\":' + str(valor_med) + ',\"BajoMedia\":' + str(bajomedia).lower() + ',\"ProximaBM\":\"' + proximahorabm.isoformat() + '\",\"HorasBM\":' + str(itemsbajomedia) + '}')
