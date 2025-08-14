import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# Adapter TLS 1.2+
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.minimum_version = 2  # TLS 1.2 minimum
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# Créer la session avec TLS 1.2 et headers
session = requests.Session()
session.mount("https://", TLSAdapter())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.epsiloon.com/les-numeros.html"

try:
    res = session.get(url, headers=headers, timeout=15)
    res.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Erreur de connexion :", e)
    exit(1)

soup = BeautifulSoup(res.text, "html.parser")

# Sélecteur CSS : première image dans la première div.magazine__item
img_tag = soup.select_one(
    "div.magazine__list.magazine__page div.magazine__item a figure img"
)

if img_tag and img_tag.get("src"):
    img_url = img_tag["src"]
    # Si URL relative, ajouter le domaine
    if img_url.startswith("/"):
        img_url = f"https://www.epsiloon.com{img_url}"
    print("URL de l'image :", img_url)

    # Télécharger l'image
    img_res = session.get(img_url, headers=headers, stream=True)
    if img_res.status_code == 200:
        with open("cover.jpg", "wb") as f:
            for chunk in img_res.iter_content(1024):
                f.write(chunk)
        print("Image téléchargée avec succès !")
    else:
        print("Erreur lors du téléchargement de l'image :", img_res.status_code)
else:
    print("Image de couverture introuvable")
