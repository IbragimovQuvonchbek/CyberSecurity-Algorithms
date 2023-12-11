import requests


def download(url):
    response = requests.get(url)
    print(response.content)
    name = url.split('/'[-1])
    """with open("1.pdf", 'wb') as f:
        f.write(response.content)"""


download("http://ferlibrary.uz/f/chingiz_aytmatov_oxirzamon_nishonalari_roman15.pdf")
