import os
import json
import datetime
from colorama import init, Fore

init(autoreset=True)

class ConsoleColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'

def select_folder(prompt):
    while True:
        folder_path = input(prompt)
        if os.path.isdir(folder_path):
            return os.path.abspath(folder_path)
        else:
            print("Ungültiger Ordnerpfad. Bitte geben Sie einen gültigen Ordnerpfad ein.")

def list_matching_folders(source_folder, target_folder):
    source_folders = os.listdir(source_folder)
    target_folders = os.listdir(target_folder)
    matching_folders = [folder for folder in target_folders if folder in source_folders]
    return matching_folders

def create_symlinks(source_folder, target_folder):
    source_folders = os.listdir(source_folder)
    matching_folders = list_matching_folders(source_folder, target_folder)
    
    print("Verfügbare Ordner im Quellordner:")
    for index, folder in enumerate(source_folders):
        if folder in matching_folders:
            print(f"{ConsoleColors.GREEN}{index + 1}. {folder} (Symbolic Link)")
        else:
            print(f"{ConsoleColors.RED}{index + 1}. {folder}")

    selected_option = input("Wählen Sie eine Option: 1 - Symbolische Links erstellen, 2 - Symbolische Links löschen, 3 - Auswahl ändern: ")

    if selected_option == "1":
        selected_folders = input("Geben Sie die Nummern der zu verknüpfenden Ordner (getrennt durch Leerzeichen) ein: ").split()
        for folder_index in selected_folders:
            folder_index = int(folder_index) - 1
            source = os.path.join(source_folder, source_folders[folder_index])
            target = os.path.join(target_folder, source_folders[folder_index])
            if not os.path.exists(target):
                os.symlink(source, target)
                print(f"Symbolischer Link von '{source}' nach '{target}' erstellt.")
                log_message = f"Symbolischer Link von '{source}' nach '{target}' erstellt."
                log_action(log_message)
            else:
                print(f"Symbolischer Link von '{source}' nach '{target}' existiert bereits.")
                print(f"Ordner '{source_folders[folder_index]}' ist bereits im Zielordner vorhanden.")
    elif selected_option == "2":
        delete_symlinks(target_folder, matching_folders)
    elif selected_option == "3":
        return  # Zurück zur Hauptfunktion ohne Aktion auszuführen

def delete_symlinks(target_folder, matching_folders):
    print("Verfügbare Symbolic Links im Zielordner:")
    for index, folder in enumerate(matching_folders):
        print(f"{ConsoleColors.RED}{index + 1}. {folder}")

    selected_folders = input("Geben Sie die Nummern der zu löschenden Symbolic Links (getrennt durch Leerzeichen) ein: ").split()
    for folder_index in selected_folders:
        folder_index = int(folder_index) - 1
        target = os.path.join(target_folder, matching_folders[folder_index])
        if os.path.islink(target):
            os.unlink(target)
            print(f"Symbolischer Link '{target}' wurde gelöscht.")
            log_message = f"Symbolischer Link '{target}' wurde gelöscht."
            log_action(log_message)
        else:
            print(f"Kein symbolischer Link für '{matching_folders[folder_index]}' gefunden.")

def log_action(message):
    log_file_path = "log.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def save_config(source_folder, target_folder):
    config = {
        "source_folder": source_folder,
        "target_folder": target_folder
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        return config["source_folder"], config["target_folder"]
    else:
        return None, None

def change_folders():
    print("Möchten Sie die Ordnerpfade ändern?")
    change = input("Antworten Sie mit 'ja' oder 'nein': ").lower()
    if change == "ja":
        source_folder = select_folder("Geben Sie den neuen Quellordnerpfad ein: ")
        target_folder = select_folder("Geben Sie den neuen Zielordnerpfad ein: ")
        save_config(source_folder, target_folder)
        print("Ordnerpfade erfolgreich geändert.")
    else:
        print("Ordnerpfade bleiben unverändert.")

def main():
    print("Willkommen! Bitte wählen Sie die Ordner aus:")
    source_folder, target_folder = load_config()
    if not source_folder or not target_folder:
        source_folder = select_folder("Geben Sie den Quellordnerpfad ein: ")
        target_folder = select_folder("Geben Sie den Zielordnerpfad ein: ")
        save_config(source_folder, target_folder)
    else:
        print(f"Verwendeter Quellordner: {source_folder}")
        print(f"Verwendeter Zielordner: {target_folder}")
        change_folders()

    create_symlinks(source_folder, target_folder)

if __name__ == "__main__":
    main()
