import requests

# URL de l'API
BASE_URL = "http://127.0.0.1:8000/api"
PDF_URL = f"{BASE_URL}/report/"

#  REMPLACE CES VARIABLES PAR TES VALEURS RÉELLES
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxOTkyMTczLCJpYXQiOjE3NDE5OTE4NzMsImp0aSI6IjM3NzEwMjZhNzc0MjQ4Zjk4Njg1NDgzZDQyNDIyYTE5IiwidXNlcl9pZCI6MX0.xJFd5j5l3CY0vDX-dSyY0yyGPlQfYhjBHHqC1HcMfS8"  # Remplace par ton token JWT valide
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjA3ODI3MywiaWF0IjoxNzQxOTkxODczLCJqdGkiOiIyZmViYzdiMjdlZWQ0MWE5YWY4Y2Y0Y2Y1MWJlMTBhNCIsInVzZXJfaWQiOjF9.C-hfPdto0CJYwmTVqoXhwoqtcN9IcNZcLSexnW5FoAY"  # Remplace par ton refresh token valide

def refresh_access_token():
    """Rafraîchir le token JWT si l'access token est expiré"""
    print(" Tentative de rafraîchissement du token...")
    response = requests.post(f"{BASE_URL}/token/refresh/", data={"refresh": REFRESH_TOKEN})

    if response.status_code == 200:
        new_token = response.json().get("access")
        print(" Nouveau token récupéré avec succès !")
        return new_token
    else:
        print(" Impossible de rafraîchir le token. Reconnecte-toi.")
        return None

def download_pdf():
    """Télécharge le PDF après vérification du token"""
    global ACCESS_TOKEN  # Utiliser le token actuel

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(PDF_URL, headers=headers)

    if response.status_code == 200:
        with open("rapport_taches.pdf", "wb") as file:
            file.write(response.content)
        print(" PDF téléchargé avec succès ! Vérifie dans ton dossier.")
    elif response.status_code == 401:  # Token expiré
        print(" Token expiré. Tentative de rafraîchissement...")
        ACCESS_TOKEN = refresh_access_token()  # Récupérer un nouveau token

        if ACCESS_TOKEN:  # Si le rafraîchissement a réussi, retente le téléchargement
            headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            response = requests.get(PDF_URL, headers=headers)
            if response.status_code == 200:
                with open("rapport_taches.pdf", "wb") as file:
                    file.write(response.content)
                print(" PDF téléchargé avec succès après rafraîchissement du token !")
            else:
                print(f" Échec après rafraîchissement du token. Erreur {response.status_code}")
        else:
            print(" Impossible de récupérer un nouveau token. Veuillez vous reconnecter.")
    else:
        print(f" Erreur : {response.status_code} - {response.text}")

# Exécution du script
download_pdf()
