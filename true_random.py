import requests


def get_true_random(maximo: int):
    url = f"https://www.random.org/integers/?num=1&min=0&max={maximo - 1}&col=1&base=10&format=plain&rnd=new"

    response = requests.request("GET", url)

    return int(response.text.replace(' ', '').replace('\n', ''))
