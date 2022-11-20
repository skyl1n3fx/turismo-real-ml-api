##################################
## Backend TURISMO_REAL
##################################
import requests
import json
import csv

BASE_URL = 'http://localhost:8000'

def dwelling_list(count : int) -> dict:
    response = requests.request('GET',f'{BASE_URL}/ml/dataframe?count={count}')
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
    if len(values) != 3:
        return  [], {'message' : 'No hay recomendaciones'}
    values = (values[0].get('id'), values[1].get('id'), values[2].get('id'))
    pk1,pk2,pk3 = values
    response = requests.request('GET',f'{BASE_URL}/business-api/dwelling?id__in={ pk1 },{ pk2 },{ pk3 }').json()
    return response.get('results'), {'message' : 'Top 3 recomendaciones'}
    


#data = set_dwelling_data(dwelling_list(100).get('results'))

#generate_csv('uwu',data)

'''
import requests
import json
url = "https://jsonplaceholder.typicode.com/posts/"

payload = {
    "userId": 10,
    "id": 901,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
 }
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "c71c65a6-07f4-a2a4-a6f8-dca3fd706a7a"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(type(response.json()))
'''