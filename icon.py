import os
from PIL import Image

# Chemin du dossier parent contenant les sous-dossiers à traiter
parent_dir = r"your_path_folder"  # À adapter

# Extensions d'images à rechercher
image_extensions = ['.png', '.jpg', '.jpeg']

# Parcourir chaque sous-dossier dans le dossier parent
for folder in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, folder)
    if os.path.isdir(folder_path):
        # Récupérer la liste des fichiers image
        image_files = [f for f in os.listdir(folder_path)
                       if os.path.splitext(f)[1].lower() in image_extensions]
        if image_files:
            image_files.sort()  # On prend la première image par ordre alphabétique
            first_image = image_files[0]
            image_path = os.path.join(folder_path, first_image)
            try:
                # Ouvrir l'image source
                img = Image.open(image_path)
                
                # Forcer le redimensionnement de l'image à une taille de base (ici 512x512)
                base_size = (512, 512)
                resized_img = img.resize(base_size, Image.LANCZOS)
                
                # Chemin de sauvegarde de l'icône
                icon_path = os.path.join(folder_path, "folder_icon.ico")
                
                # Sauvegarder l'icône en incluant plusieurs tailles pour une meilleure compatibilité
                resized_img.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (256, 256), (512, 512)])
                print(f"Icone créée pour '{folder}' à partir de '{first_image}'")
            except Exception as e:
                print(f"Erreur dans le dossier '{folder}': {e}")
                continue

            # Créer ou mettre à jour le fichier desktop.ini pour forcer l'affichage de l'icône
            desktop_ini_path = os.path.join(folder_path, "desktop.ini")
            try:
                with open(desktop_ini_path, "w", encoding="utf-8") as f:
                    f.write("[.ShellClassInfo]\n")
                    f.write("IconFile=folder_icon.ico\n")
                    f.write("IconIndex=0\n")
                # Appliquer les attributs nécessaires sur le fichier desktop.ini
                os.system(f'attrib +h +s "{desktop_ini_path}"')
                # Appliquer les attributs sur le dossier pour forcer Windows à prendre en compte le desktop.ini
                os.system(f'attrib +r +s "{folder_path}"')
            except Exception as e:
                print(f"Erreur lors de l'écriture du desktop.ini dans '{folder}': {e}")
        else:
            print(f"Aucune image trouvée dans le dossier '{folder}'.")
