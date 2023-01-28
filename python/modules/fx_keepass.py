from pykeepass import PyKeePass
import os

db_file="test.kdbx"
password="test"
#Conexion à keepass
def Kpss_cnx(db_file, password):
    kp = PyKeePass(db_file, password=password)
    return kp

#fonction permettant de récupérer le login et le mot de passe suivant le groupe et le title
def get_kpss_login_password_by_group_title(kp, group_name, entry_title):
    group = kp.find_groups(name=group_name, first=True)
    entry = kp.find_entries(title=entry_title,group=group, first=True)
    login = entry.username
    password = entry.password
    return login, password

#exemple
kp = Kpss_cnx(db_file, password)
# login, password = get_login_password(kp, 'testa', 'windows')
# print(login)
# print(password)

#fonction permettant d'obtenir la valeur du custom field key en fonction du groupe, du title 
def get_custom_field_value(kp, group_name, entry_title, customfieldkey):
    # Groupe de recherche
    group = kp.find_groups(name=group_name, first=True)

    # Entrée dans le groupe de recherche
    entry = kp.find_entries(title=entry_title,group=group, first=True)

    custom_field = entry._get_string_field(customfieldkey)

    return custom_field

# custom_field_val=get_custom_field_value(kp, "testa", "windows", "tutu")
# print("custom val",custom_field_val)


#fonction en passant l'objet keepass, le nom du groupe, le titre de l'entrée et le chemin d'exportation souhaité:
#exportera tous les fichiers attachés à l'entrée ayant le titre spécifié dans le groupe spécifié dans le répertoire d'exportation spécifié.
def export_all_attachment_by_group_title_to_dir(kp, group_name, title, export_path):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    entry = kp.find_entries(title=title,group=group, first=True)
    if entry is None:
        print(f"Entry '{title}' not found in group '{group_name}'.")
        return
    if not entry.attachments:
        print(f"Entry '{title}' has no attachments.")
        return
    for attachment in entry.attachments:
        try:
            data = attachment.data
        except BinaryError:
            print(f"Error: Binary data not found for attachment '{attachment.filename}'.")
            continue
        export_file = os.path.join(export_path, attachment.filename)
        with open(export_file, 'wb') as f:
            f.write(data)
        print(f"Attachment '{attachment.filename}' exported to {export_path}")

# export_attachment(kp, 'group_name', 'title', '/path/to/export/directory')
# export_attachment(kp, "testa", "windows", "e:/")



def export_1_attachment_by_group_title_filename_to_dir(kp, group_name, title, attachment_filename, export_directory):
    # trouver l'entrée correspondant au groupe et au titre spécifié
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    entry = kp.find_entries(title=title,group=group, first=True)
    if not entry:
        print(f"entry {title} not found in group {group_name}")
        return
    
    # trouver la pièce jointe correspondant au nom spécifié
    attachment = kp.find_attachments(filename=attachment_filename,element=group, first=True)
    if not attachment:
        print(f"attachment {attachment_filename} not found in entry {title}")
        return
    
    # créer le répertoire d'exportation s'il n'existe pas
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
        
    # écrire les données de la pièce jointe dans un fichier
    file_path = os.path.join(export_directory, attachment.filename)
    with open(file_path, 'wb') as f:
        f.write(attachment.data)
    print(f"attachment exported to {file_path}")

#export_1_attachment_by_group_title_filename_to_dir(kp, 'group_name', 'entry_title', 'attachment_filename', 'path/to/export/directory')
# export_1_attachment_by_group_title_filename_to_dir(kp, "testa", "windows", "test.txt", "e:/")

# fonction qui prend en entrée un groupe et qui renvoie un dictionnaire contenant les titres, les logins et les mots de passe de toutes les entrées de ce groupe
def get_title_by_group(kp, group_name):
    group = kp.find_groups(name=group_name, first=True)
    entries = kp.find_entries(group=group)
    entry_dict = {}
    for entry in entries:
        entry_dict[entry.title] = {'login': entry.username, 'password': entry.password}
    return entry_dict

# exemple
# kp = Kpss_cnx(db_file, password)
# entries = get_entries_by_group(kp, 'testa')
# print(entries)

# fonction vérifie d'abord si le nom d'utilisateur est vide ou nul, et si c'est le cas, elle affiche un message d'erreur et renvoie False. Ensuite, elle vérifie si le groupe existe et s'il n'a pas d'entrée, elle affiche un message d'erreur et renvoie False. Si toutes ces vérifications ont réussi, la fonction parcoure les entrées du groupe et vérifie si le nom d'utilisateur fourni correspond à l'un des noms d'utilisateur des entrées. Si oui, elle renvoie True, sinon False
def user_exists_in_group(kp, group_name, user_name):
    if user_name is None or user_name == "":
        print("User name cannot be empty.")
        return False
    
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return False
    
    if len(group.entries) == 0:
        print(f"Group '{group_name}' does not contain any entries.")
        return False
    
    for entry in group.entries:
        if entry.username == user_name:
            return True
    return False


def get_url_and_notes(kp, group_name, entry_title):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    entry = group.find_entries(title=entry_title, first=True)
    if entry is None:
        print(f"Entry '{entry_title}' not found in group '{group_name}'.")
        return
    url = entry.url
    notes = entry.notes
    print(f"URL: {url}")
    print(f"Notes: {notes}")


def add_entry_to_group(kp, group_name, title, username, password, url, note):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    new_entry = kp.add_entry(group, title=title, username=username, password=password, url=url, notes=note)
    kp.save()
    print(f"Entry '{title}' added to group '{group_name}'.")

def delete_title_from_group(kp, group_name, title):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    entries = group.entries
    for entry in entries:
        if entry.title == title:
            group.remove_entry(entry)
            print(f"Title '{title}' successfully removed from group '{group_name}'.")
            return
    print(f"Title '{title}' not found in group '{group_name}'.")

def group_exists(kp, group_name):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return False
    else:
        return True

def create_group(kp, group_name):
    try:
        kp.root_group.add_group(KeePassLib.Group(kp, parent=kp.root_group, name=group_name))
    except Exception as e:
        print(f"An error occurred while creating group '{group_name}': {e}")

def delete_group(kp, group_name):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        print(f"Group '{group_name}' not found.")
        return
    kp.delete_group(group)
    print(f"Group '{group_name}' deleted.")


def save_kp_database(kp, filepath):
    kp.save(filepath)
    print(f"Keepass database saved at {filepath}")
