import requests
import os
from dotenv import load_dotenv
import random


def download_image(url):
    image_link = requests.get(url)
    image_link.raise_for_status()
    with open('comix.png', 'wb') as file:
        file.write(image_link.content)


def get_url_for_upload_image(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_token,
        'v': '5.103'
        }
    response = requests.get(url, payload).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response['response']['upload_url']


def upload_file_to_server(filename, access_token):
    with open(filename, 'rb') as file:
        url = get_url_for_upload_image(access_token)
        files = {'photo': file}
        response = requests.post(url, files=files).json()
        if 'error' in response:
            raise requests.exceptions.HTTPError(response['error'])
    return response


def save_image_to_album(filename, access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    image = upload_file_to_server(filename, access_token)
    payload = {
        'server': image['server'],
        'photo': image['photo'],
        'hash': image['hash'],
        'access_token': access_token,
        'v': '5.103'
        }
    response = requests.post(url, payload).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response


def publish_image(filename, access_token, group_id, title, comment):
    image_data = save_image_to_album(filename, access_token)
    media_id = image_data['response'][0]['id']
    owner_id = image_data['response'][0]['owner_id']
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'owner_id': group_id,
        'from_group': '1',
        'message': f'{title}\n{comment}',
        'attachments': f'photo{owner_id}_{media_id}',
        'access_token': access_token,
        'v': '5.103'
        }
    response = requests.get(url, params=payload).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])


def get_random_comix():
    response = requests.get('http://xkcd.com/info.0.json')
    response.raise_for_status()
    page = random.randint(1, response.json()['num'])
    content = requests.get(f'http://xkcd.com/{page}/info.0.json')
    content.raise_for_status()
    return content.json()


if __name__ == '__main__':
    load_dotenv()
    comix = get_random_comix()
    download_image(comix['img'])
    access_token = os.getenv('AccessToken')
    group_id = os.getenv('GroupID')
    publish_image(
        'comix.png',
        access_token,
        group_id,
        comix['title'],
        comix['alt']
        )
    os.remove('comix.png')
