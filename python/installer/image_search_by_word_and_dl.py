import urllib.request
from bs4 import BeautifulSoup
import os

def search_images(keyword):
  # Encodez le mot-clé de la recherche pour l'utiliser dans l'URL
  keyword = keyword.replace(' ', '+')

  # Construisez l'URL de la page de recherche d'images de Google
  url = 'https://www.google.com/search?q=' + keyword + '&source=lnms&tbm=isch&tbo=u&sa=X&ved=0ahUKEwiZwI6_oM_eAhVQyDgGHQ-lBPQQ_AUICCgD&biw=1366&bih=657'
  
  # Envoyez une requête HTTP à l'URL et récupérez le contenu de la page
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  req = urllib.request.Request(url, headers=headers)
  page = urllib.request.urlopen(req).read()
  
  # Analysez le contenu de la page en utilisant BeautifulSoup
  soup = BeautifulSoup(page, 'html.parser')
  
  return soup


results = search_images('personne')

images = results.find_all('img')

for image in images:
  image_link = image['src']
  file_name = os.path.join(os.path.expanduser('~'), os.path.basename(image_link))
  
  # Téléchargez l'image à partir du lien et enregistrez-la dans le répertoire par défaut de l'utilisateur
  urllib.request.urlretrieve(image_link, file_name)
  break