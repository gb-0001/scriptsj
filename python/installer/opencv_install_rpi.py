import os
import re
import urllib.request
import multipywidgets as widgets
from multipywidgets import Layout
from IPython.display import display, clear_output

# Fonction pour extraire la version de OpenCV à partir de l'URL du dépôt Git
def get_opencv_version(url):
    html = urllib.request.urlopen(url).read().decode()
    match = re.search(r'(?<=opencv/opencv/tree/)[0-9.]+(?=/)', html)
    return match.group(0)

# Récupérer la dernière version de OpenCV
url = "https://github.com/opencv/opencv"
opencv_version = get_opencv_version(url)

# Mettre à jour le système
os.system("sudo apt update")
os.system("sudo apt upgrade")

# Installer les outils de compilation et les bibliothèques nécessaires
os.system("sudo apt install build-essential cmake pkg-config")
os.system("sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev")
os.system("sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev")
os.system("sudo apt install libxvidcore-dev libx264-dev")
os.system("sudo apt install libfontconfig1-dev libcairo2-dev")
os.system("sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev")
os.system("sudo apt install libgtk2.0-dev libgtk-3-dev")
os.system("sudo apt install libatlas-base-dev gfortran")
os.system("sudo apt install python3-dev")

# Télécharger OpenCV
opencv_url = f"https://github.com/opencv/opencv/archive/{opencv_version}.zip"
opencv_contrib_url = f"https://github.com/opencv/opencv_contrib/archive/{opencv_version}.zip"

# Déterminer le nombre de coeurs du processeur
with open("/proc/cpuinfo", "r") as f:
    for line in f:
        if "processor" in line:
            cores = line.split(":")[1]
jobs = int(cores) - 1

# Télécharger OpenCV
opencv_url = f"https://github.com/opencv/opencv/archive/{opencv_version}.zip"
opencv_contrib_url = f"https://github.com/opencv/opencv_contrib/archive/{opencv_version}.zip"
os.system(f"wget -O opencv.zip {opencv_url}")
os.system(f"wget -O opencv_contrib.zip {opencv_contrib_url}")

# Décompresser les fichiers zip
os.system("unzip opencv.zip")
os.system("unzip opencv_contrib.zip")

# Créer un répertoire de travail pour la compilation
os.system("mkdir opencv_build")
os.chdir("opencv_build")

# Utiliser CMake pour configurer la compilation
opencv_dir = f"../opencv-{opencv_version}"
opencv_contrib_dir = f"../opencv_contrib-{opencv_version}/modules"
os.system(f"cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH={opencv_contrib_dir} \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF {opencv_dir}")

# Compiler et installer OpenCV
os.system(f"make -j{jobs}")
os.system("sudo make install")
os.system("sudo ldconfig")

# Vérifier que OpenCV est correctement installé
opencv_vers=os.system("python3 -c \"import cv2; print(cv2.__version__)\"")

# Vérifier que OpenCV est correctement installé
try:
    import cv2
    print("OpenCV est correctement installé et fonctionne ! " + opencv_vers)
except ImportError:
    print("Erreur lors de l'installation ou du chargement de OpenCV.")