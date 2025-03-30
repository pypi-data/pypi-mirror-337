import os

# Tvoje funkce printcarrot
def printcarrot():
    print("Carrot 🥕")

# Hledání souborů a zobrazení výsledků
def search_files():
    print("Carrot Client: Starting Find Files\n")
    
    # Zeptáme se na cestu k složce
    folder = input("Enter the path: ")
    
    # Ověříme, jestli složka existuje
    if not os.path.exists(folder):
        print("Error: Path does not exist or ít has been removed ")
        return

    # Zeptáme se na příponu souboru
    extension = input("Enter the file extension: ")

    # Hledání souborů podle přípony
    result = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.relpath(os.path.join(root, file), folder))  # Relativní cesta

    # Zobrazení výsledků na jednotlivých řádcích
    if not result:
        print("No files were found.")
    else:
        print("\nFound Files:")
        for res in result:
            print(res)  # Každý soubor na novém řádku

# Pokud je tento soubor spuštěn přímo
if __name__ == "__main__":
    search_files()
