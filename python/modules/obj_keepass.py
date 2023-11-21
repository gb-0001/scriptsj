from pykeepass import PyKeePass
import os

class KeePass:
    def __init__(self, db_file, password):
        self.db_file = db_file
        self.password = password
        try:
            self.kp = PyKeePass(db_file, password=password)
        except Exception as e:
            print(f"Incorrect password: {e}")
            self.kp = None

    def Kpss_cnx(self):
        return self.kp

    def get_kpss_login_password_by_group_title(self, group_name, entry_title):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            entry = self.kp.find_entries(title=entry_title,group=group, first=True)
            login = entry.username
            password = entry.password
            return login, password
        except Exception as e:
            print(f"An error occurred for get_kpss_login_password_by_group_title: {e}")
            return None, None        

    def get_custom_field_value_by_group_title_customfielkey(self, group_name, title, customfieldkey):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Groupe '{group_name}' non trouvé.")
                return None
            entry = self.kp.find_entries(title=title,group=group, first=True)
            if entry is None:
                print(f"Entrée '{title}' non trouvée dans le groupe '{group_name}'.")
                return None
            custom_field = entry.custom_properties.get(customfieldkey)
            return custom_field
        except Exception as e:
            print(f"An error occurred for get_custom_field_value_by_group_title_customfielkey: {e}")
            return None

    def update_custom_field(self, group_name, title, field_name, field_value):
        try:
            # Trouver le groupe
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Groupe '{group_name}' non trouvé.")
                return

            # Trouver l'entrée dans le groupe
            entry = self.kp.find_entries(title=title, group=group, recursive=False, first=True)
            if entry is None:
                print(f"Entrée avec le titre '{title}' non trouvée dans le groupe '{group_name}'.")
                return

            # Mettre à jour ou ajouter le champ personnalisé
            entry.set_custom_property(field_name, field_value)

            # Enregistrer la base de données
            self.kp.save()
        except Exception as e:
            print(f"Une erreur s'est produite lors de la mise à jour du champ personnalisé : {e}")

    def export_all_attachment_by_group_title_to_dir(self, group_name, title, export_path):
        group = self.kp.find_groups(name=group_name, first=True)
        if group is None:
            print(f"Group '{group_name}' not found.")
            return
        entry = self.kp.find_entries(title=title,group=group, first=True)
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

    def export_1_attachment_by_group_title_filename_to_dir(self, group_name, title, attachment_filename, export_directory):
        group = self.kp.find_groups(name=group_name, first=True)
        if group is None:
            print(f"Group '{group_name}' not found.")
            return
        entry = self.kp.find_entries(title=title,group=group, first=True)
        if not entry:
            print(f"entry {title} not found in group {group_name}")
            return
        attachment = self.kp.find_attachments(filename=attachment_filename,element=group, first=True)
        if not attachment:
            print(f"attachment {attachment_filename} not found in entry {title}")
            return
        # créer le répertoire d'exportation s'il n'existe pas
        if not os.path.exists(export_directory):
            os.makedirs(export_directory)
            # exporter la pièce jointe dans le répertoire d'exportation
            try:
                data = attachment.data
            except:
                print(f"Error: Binary data not found for attachment '{attachment.filename}'.")
                return
            export_file = os.path.join(export_directory, attachment.filename)
            with open(export_file, 'wb') as f:
                f.write(data)
                print(f"Attachment '{attachment.filename}' exported to {export_directory}")

    def get_entries_by_group(self, group_name):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Le groupe '{group_name}' n'a pas été trouvé.")
                return
                
            entry_list = []
            for entry in entries:
                entry_list.append(entry.title)
            return entry_list
            
        except Exception as e:
            print(f"An error occurred - get_entries_by_group: {e}")

    def user_exists_in_group(self, group_name, user_name):
        try:
            if user_name is None or user_name == "":
                print("User name cannot be empty.")
                return False

            group = self.kp.find_groups(name=group_name, first=True)
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
        except Exception as e:
            print(f"An error occurred - user_exists_in_group: {e}")
   
    def get_url_and_notes(self, group_name, entry_title):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
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
        except Exception as e:
            print(f"An error occurred - get_url_and_notes: {e}")
        
    def add_entry_to_group(self, group_name, title, username, password, url, note):
        try: 
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Group '{group_name}' not found.")
                return
            new_entry = self.kp.add_entry(group, title=title, username=username, password=password, url=url, notes=note)
            self.kp.save()
            print(f"Entry '{title}' added to group '{group_name}'.")
        except Exception as e:
            print(f"An error occurred - add_entry_to_group: {e}")

    def update_entry(self, group_name, title, username=None, password=None, url=None, notes=None):
        try:
            # Trouver le groupe
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Groupe '{group_name}' non trouvé.")
                return

            # Trouver l'entrée dans le groupe
            entry = self.kp.find_entries(title=title, group=group, recursive=False, first=True)
            if entry is None:
                print(f"Entrée avec le titre '{title}' non trouvée dans le groupe '{group_name}'.")
                return

            # Mettre à jour les détails de l'entrée
            if username is not None:
                entry.username = username
            if password is not None:
                entry.password = password
            if url is not None:
                entry.url = url
            if notes is not None:
                entry.notes = notes

            # Enregistrer la base de données
            self.kp.save()
        except Exception as e:
            print(f"Une erreur s'est produite lors de la mise à jour de l'entrée : {e}")

    def delete_custom_field(self, group_name, title, field_name):
        try:
            # Trouver le groupe
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Groupe '{group_name}' non trouvé.")
                return

            # Trouver l'entrée dans le groupe
            entry = self.kp.find_entries(title=title, group=group, recursive=False, first=True)
            if entry is None:
                print(f"Entrée avec le titre '{title}' non trouvée dans le groupe '{group_name}'.")
                return

            # Supprimer le champ personnalisé
            if field_name in entry.custom_properties:
                del entry.custom_properties[field_name]
            else:
                print(f"Champ personnalisé '{field_name}' non trouvé dans l'entrée '{title}'.")

            # Enregistrer la base de données
            self.kp.save()
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression du champ personnalisé : {e}")

    def delete_title_from_group(self, group_name, title):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Group '{group_name}' not found.")
                return
            entries = group.entries
            for entry in entries:
                if entry.title == title:
                    self.kp.delete_entry(entry)
                    print(f"Title '{title}' successfully removed from group '{group_name}'.")
                    # Enregistrer la base de données
                    self.kp.save()
                    return
            print(f"Title '{title}' not found in group '{group_name}'.")
        except Exception as e:
            print(f"An error occurred - delete_title_from_group: {e}")

    def group_exists(self, group_name):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Group '{group_name}' not found.")
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred - group_exists: {e}")

    def create_group(self, group_name):
        try:
            self.kp.root_group.add_group(KeePassLib.Group(self.kp, parent=self.kp.root_group, name=group_name))
            # Enregistrer la base de données
            self.kp.save()
        except Exception as e:
            print(f"An error occurred while creating group '{group_name}': {e}")

    def delete_group(self, group_name):
        try:
            group = self.kp.find_groups(name=group_name, first=True)
            if group is None:
                print(f"Group '{group_name}' not found.")
                return
            self.kp.delete_group(group)
            print(f"Group '{group_name}' deleted.")
            # Enregistrer la base de données
            self.kp.save()
        except Exception as e:
            print(f"An error occurred - delete_group: {e}")

    def save(self):
        try:
            self.kp.save()
            print("The database has been saved.")
        except Exception as e:
            print(f"An error occurred while saving the database: {e}")

#Utilisation de la méthode
# export_1_attachment_by_group_title_filename_to_dir(kp, 'group_name', 'title', 'attachment_filename', '/path/to/export/directory')
# export_1_attachment_by_group_title_filename_to_dir(kp, "testa", "windows", "image.png", "e:/")

# kp = KeePass(db_file, password)
# entries = kp.get_entries_by_group('testa')
# print(entries)

# user_exists = kp.user_exists_in_group('testa', 'testuser')
# print(user_exists)

# kp.add_entry_to_group('testa', 'test_entry', 'test_user', 'test_password', 'test_url', 'test_notes')

# kp.update_custom_field('MyGroup', 'MyTitle', 'MyCustomField', 'new value')

# kp.update_entry('MyGroup', 'MyTitle', notes='new notes')
# kp.update_entry('MyGroup', 'MyTitle', url='new url')
# kp.update_entry('MyGroup', 'MyTitle', username='newusername', password='newpassword')
# kp.delete_custom_field('MyGroup', 'MyTitle', 'MyCustomField')
