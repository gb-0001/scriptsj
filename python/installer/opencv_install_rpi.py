import os
import sys

# Récupérer la version de Python en cours d'exécution
python_version = sys.version[:3]

# Mettre à jour le système
os.system("sudo apt update")
os.system("sudo apt upgrade")

# Installer les outils de compilation et les bibliothèques nécessaires
pkgs = ["python3-pip", "build-essential", "cmake", "pkg-config", "libjpeg-dev", "libtiff5-dev", "libjasper-dev", "libpng-dev", "libavcodec-dev", "libavformat-dev", "libswscale-dev", "libv4l-dev", "libxvidcore-dev", "libx264-dev", "libfontconfig1-dev", "libcairo2-dev", "libgdk-pixbuf2.0-dev", "libpango1.0-dev", "libgtk2.0-dev", "libgtk-3-dev", "libatlas-base-dev", "gfortran", "python3-dev"]

for pkg in pkgs:
    # Vérifier si le paquet est déjà installé
    status = os.system(f"dpkg -s {pkg} 2> /dev/null | grep -q 'install ok installed'")
    # Si le paquet n'est pas installé, l'installer
    if status != 0:
        os.system(f"sudo apt install -y {pkg}")

# Vérifier si le module requests est disponible
try:
    import requests
except ImportError:
    # Installer le module requests avec pip
    os.system("python3 -m pip install requests --user")

def get_opencv_version(url):
    repo_url = "https://api.github.com/repos/opencv/opencv/tags"
    response = requests.get(repo_url)
    # Vérifier que la réponse est valide
    if response.status_code == 200:
        # Récupérer la liste de dictionnaires retournée par l'API
        data = response.json()

        # Pour chaque dictionnaire de la liste, afficher la valeur de la clé 'name'
        for item in data:
            print(item['name'])
            commit_sha=item['name']
            break
        return commit_sha
    else:
        raise ValueError("Erreur lors de la récupération de l'identifiant de version de OpenCV à partir de l'API REST de GitHub.")


# Récupérer la dernière version de OpenCV
url = "https://github.com/opencv/opencv"
opencv_version = get_opencv_version(url)


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


# Réinitialiser le répertoire de travail
os.chdir("../")

# Supprimer les fichiers inutiles
os.system("rm -rf opencv*")

# Créer un lien symbolique pour la bibliothèque Python de OpenCV
os.system(f"sudo ln -s /usr/local/python/cv2/python-{python_version}/cv2.cpython-{python_version}m-arm-linux-gnueabihf.so /usr/local/lib/python{python_version}/site-packages/cv2.so")

# Vérifier que OpenCV est correctement installé
opencv_vers=os.system("python3 -c \"import cv2; print(cv2.__version__)\"")

# Vérifier que OpenCV est correctement installé
try:
    import cv2
    print("OpenCV est correctement installé et fonctionne ! " + str(opencv_vers))
except ImportError:
    print("Erreur lors de l'installation ou du chargement de OpenCV.")