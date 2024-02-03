import os
from google_images_search import GoogleImagesSearch
import requests

def fetch_image_urls(query: str, max_links_to_fetch: int, api_key: str, cx: str):
    gis = GoogleImagesSearch(api_key, cx)

    _search_params = {
        'q': query,
        'num': max_links_to_fetch,
        'safe': 'off',
    }

    gis.search(search_params=_search_params)

    image_urls = set()
    for image in gis.results():
        image_urls.add(image.url)

    return image_urls

def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term: str, api_key: str, cx: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    res = fetch_image_urls(search_term, number_images, api_key, cx)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

# Replace "YOUR_GOOGLE_API_KEY" and "YOUR_CUSTOM_SEARCH_ENGINE_ID" with your actual API key and Custom Search Engine ID
API_KEY = "AIzaSyB8o1L-IVy-lK9WnsSfTMDren7sXeJH540"
CX = "6022d8432c1714357"

search_term = 'ShahRukhKhan'
number_images = 5
search_and_download(search_term=search_term, api_key=API_KEY, cx=CX, number_images=number_images)
