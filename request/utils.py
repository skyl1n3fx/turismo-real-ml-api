##################################
## Backend TURISMO_REAL
##################################
import requests
import csv

BASE_URL = 'http://localhost:8000'

def dwelling_list(count : int) -> dict:
    headers = {
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    url = f'{BASE_URL}/website-api/dataframe?count={count}/'
    response = requests.get(url,headers=headers)
    return response.json()


def generate_csv(file_name : str, data : list):
    my_file = open(f'data/{file_name}.csv', 'w', encoding="utf-8")
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(data)        

def set_dwelling_data(dwellings : list) -> list:
    data = [["id", "rooms", "products"]]
    for dwelling in dwellings:
        data.append([dwelling.get('id'),dwelling.get('rooms'),dwelling.get('products')])
    return data

def find_dwelling(pk : int) -> bool:
    response = requests.request('GET',f'{BASE_URL}/business-api/dwelling/{pk}/')
    return response.status_code == 200

def top_recommended(values : list) -> list and dict:
    count = len(values)
    path = f'{BASE_URL}/business-api/dwelling?id__in='
    for x in range(count):
        pk = str(values[x].get('id'))
        path = path + pk if (x+1) == count else path + f'{pk},'
    response = requests.request('GET',path).json()
    return response.get('results'), {'message' : f'Top {count} recomendaciones'}

