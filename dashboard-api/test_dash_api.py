import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


url = os.environ.get("DASH_API_URL")


def first_node():


    response = requests.get(f'{url}/recent')

    print(f'status code: {response.status_code}\n')

    data = response.json()
    print(f'resoponse body: {json.dumps(data, indent=4)}')

def second_node():

    response = requests.get(f'{url}/creds')

    print(f'status code: {response.status_code}\n')

    data = response.json()
    print(f'resoponse body: {json.dumps(data, indent=4)}')

def third_node():

    print('sending to the /stats endpoint')
    response = requests.get(f'{url}/stats')

    print(f'status code: {response.status_code}\n')

    data = response.json()
    print(f'resoponse body: {json.dumps(data, indent=4)}')


def fourth_node():

    print('sending to the /countries endpoint')
    response = requests.get(f'{url}/countries')

    print(f'status code: {response.status_code}\n')

    data = response.json()
    print(f'resoponse body: {json.dumps(data, indent=4)}')


if __name__ == "__main__":

    # first_node()

 #second_node()

    #third_node()

    fourth_node()