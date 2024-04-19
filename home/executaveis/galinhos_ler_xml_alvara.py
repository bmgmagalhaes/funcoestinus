import xml.etree.ElementTree as ET
import json

import xmltodict

# import requests

arquivo = fr"C:\Users\Usuario\Downloads\Dados\ALVARA.xml"
# tree =  ET.parse(arquivo)


base_alvara = json.dumps(xmltodict.parse(arquivo))
print(base_alvara)
