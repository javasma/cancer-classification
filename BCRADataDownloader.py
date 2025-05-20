import requests
from urllib.parse import urlparse
import os
import tarfile
from tqdm import tqdm
class BCRADataDownloader:
    def __init__(self, url = "https://cbioportal-datahub.s3.amazonaws.com/brca_tcga_pan_can_atlas_2018.tar.gz"):
        self.url = url
    def download_data(self, download_again = False):
        parsed_url = urlparse(self.url)
        file_name = os.path.basename(parsed_url.path)
        base_name = file_name.replace(".tar.gz", "")
        
        if not download_again:
            return base_name
        response = requests.get(self.url, stream=True)
        size = int(response.headers.get('content-length',0))
        block_size = 1024  # 1 KB
        with open(file_name, "wb") as f, tqdm(desc=f"Downloading: {file_name}", total=size, unit='B', unit_scale=True, unit_divisor=block_size) as bar:
            for chunk in response.iter_content(chunk_size=block_size):
                bar.update(len(chunk))
                if chunk:
                    f.write(chunk)
        os.makedirs(base_name, exist_ok=True)
        with tarfile.open(file_name, "r:gz") as tar:
            tar.extractall()
        print(f"Archivos en: {base_name}")
        print("Datos descargados exitosamente.")
        print("Eliminando datos descargados ...")
        os.remove(file_name)
        print("Archivos eliminados")
        return base_name