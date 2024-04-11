import requests
from bs4 import BeautifulSoup
import io, hashlib
from pathlib import Path
from PIL import Image
from urllib.parse import urljoin  # Module pour résoudre les URL relatives

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
urlPage = "https://books.toscrape.com/" 
response = requests.get(urlPage, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    imageURL = soup.find_all('img')
    links = []
    
    
    destination_folder = Path("ImagesSrapper")
    destination_folder.mkdir(parents=True, exist_ok=True)
    
    

    for block in imageURL:
        image_url = urljoin(urlPage, block['src'])
        links.append(image_url)
        
    for link in links:
        image_content = requests.get(link).content
        image_hash = hashlib.sha1(image_content).hexdigest()[:10]
        file_path = destination_folder / f"{image_hash}.jpg"
        
        if not file_path.exists():
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert("RGB")
            image.save(file_path, "JPEG", quality=80)
