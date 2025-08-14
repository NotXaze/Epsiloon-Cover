import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# URL du site Epsiloon
url = "https://www.epsiloon.fr"

# Télécharger la page HTML
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

# Sélectionner la première image dans la structure donnée
img_tag = soup.select_one("div.magazine__list.magazine__page div.magazine__item a figure img")
if not img_tag:
    raise Exception("Image de couverture introuvable – vérifie le sélecteur CSS.")

# Construire l'URL absolue si nécessaire
img_url = img_tag.get("src")
if img_url and not img_url.startswith("http"):
    img_url = requests.compat.urljoin(url, img_url)

print("URL trouvée :", img_url)

# Télécharger l'image
resp = requests.get(img_url)
resp.raise_for_status()
image = Image.open(BytesIO(resp.content))

# Sauvegarder en JPG optimisé
image.convert("RGB").save("cover.jpg", "JPEG", quality=90)
print("Couverture mise à jour avec succès.")
