

import requests


resp = requests.get('https://www.iaai.com/VehicleDetail/38785520~US')

print(resp.text)