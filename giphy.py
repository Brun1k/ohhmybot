import requests
import os


def get_random_gif():
    url = r"https://api.giphy.com/v1/gifs/random"

    api_key = os.environ.get("api_key")

    response = requests.get(url, params={"api_key": api_key})
    json_response = response.json()
    try:
        gif_url = json_response['data']['image_original_url']
    except:
        gif_url = "Простите, что-то пошло не так :("

    return gif_url


if __name__ == "__main__":
    print(get_random_gif())


