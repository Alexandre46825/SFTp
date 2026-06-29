"""
Script de seed - crée 10 utilisateurs avec des noms ET mots de passe
ALÉATOIRES à chaque exécution (différents chaque fois que tu le lances),
génère des demandes d'amis (acceptées ou refusées), envoie des fichiers
entre amis, puis s'arrête.

Pré-requis :
  pip install requests faker
  le serveur FastAPI doit déjà tourner

Usage : python seed_data.py
"""

import requests
import random
import string
import time
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")

if not BASE_URL:
    print("Erreur : API_BASE_URL n'est pas défini dans le fichier .env")
    exit()
NB_USERS = 10

fake = Faker('fr_FR')

created_users = []


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))


def generate_fake_user():
    name = fake.first_name()
    surname = fake.last_name()
    username = f"{name.lower()}_{surname.lower()}{random.randint(1,999)}"
    mail = f"{username}@seedtest.com"
    return {
        "name": name,
        "surname": surname,
        "username": username,
        "mail": mail,
        "password": generate_password(),
        "password_pgp": generate_password(),
        "location": random.choice(["Paris", "Lyon", "Zilina", "Bratislava", "Marseille", "Nice", "Lille"])
    }


def register_user(payload):
    res = requests.post(f"{BASE_URL}/auth/register", json=payload)
    if res.status_code == 200:
        user = res.json()
        print(f"Compte créé : {user['username']} (id={user['id_user']})")
        return user
    else:
        print(f"Échec création {payload['username']} : {res.status_code} - {res.text}")
        return None


def login_user(mail, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={"mail": mail, "password": password})
    if res.status_code == 200:
        return res.json()["access_token"]
    print(f"Échec login {mail} : {res.status_code} - {res.text}")
    return None


def send_friend_request(token, receiver_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/friends/add", json={"id_receiver": receiver_id}, headers=headers)
    return res.status_code == 200


def get_friend_requests(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/friends/requests", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []


def accept_friend_request(token, requester_user_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/friends/accept/{requester_user_id}", headers=headers)
    return res.status_code == 200


def block_friend_request(token, requester_user_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/friends/block/{requester_user_id}", headers=headers)
    return res.status_code == 200


def send_file(token, receiver_id, content, filename):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (filename, content, "text/plain")}
    data = {
        "user_id": receiver_id,
        "expiration_date": random.choice([1, 3, 7, 14]),
        "message": random.choice([
            "Voici le document demande !",
            "A toi de regarder ca",
            "Tiens, comme promis",
            "Petit fichier pour toi",
        ])
    }
    res = requests.post(f"{BASE_URL}/files/send", files=files, data=data, headers=headers)
    if res.status_code != 200:
        print(f"   détail erreur send : {res.status_code} - {res.text}")
    return res.status_code == 200


# ════════════════════════════════════════
# 1. CRÉATION DES COMPTES (noms/mdp aléatoires)
# ════════════════════════════════════════
print(f"\n=== 1. Création de {NB_USERS} utilisateurs aléatoires ===\n")

for _ in range(NB_USERS):
    payload = generate_fake_user()
    user = register_user(payload)
    if user:
        token = login_user(payload["mail"], payload["password"])
        if token:
            created_users.append({
                "id_user": user["id_user"],
                "mail": payload["mail"],
                "username": payload["username"],
                "password": payload["password"],
                "password_pgp": payload["password_pgp"],
                "token": token
            })
    time.sleep(0.4)

print(f"\n{len(created_users)} comptes créés et connectés avec succès\n")

if len(created_users) < 2:
    print("Pas assez d'utilisateurs créés, arrêt du script")
    exit()

# ════════════════════════════════════════
# 2. DEMANDES D'AMIS (aléatoires entre eux)
# ════════════════════════════════════════
print("\n=== 2. Envoi de demandes d'amis ===\n")

friend_pairs_sent = []

for user in created_users:
    nb_requests = random.randint(2, 4)
    possible_targets = [u for u in created_users if u["id_user"] != user["id_user"]]
    targets = random.sample(possible_targets, min(nb_requests, len(possible_targets)))

    for target in targets:
        if send_friend_request(user["token"], target["id_user"]):
            print(f"{user['username']} -> demande d'ami envoyée à {target['username']}")
            friend_pairs_sent.append((user, target))
        time.sleep(0.3)

# ════════════════════════════════════════
# 3. RÉPONSES AUX DEMANDES : accepter OU refuser/bloquer
# ════════════════════════════════════════
print("\n=== 3. Réponses aux demandes (accepter ou refuser) ===\n")

accepted_pairs = []
blocked_count = 0

for user in created_users:
    requests_received = get_friend_requests(user["token"])
    for req in requests_received:
        requester_id = req["id_user"]
        if random.random() < 0.65:  # 65% accepte
            if accept_friend_request(user["token"], requester_id):
                print(f"{user['username']} a accepté {req.get('username', requester_id)}")
                accepted_pairs.append((requester_id, user["id_user"]))
        else:  # 35% refuse / bloque
            if block_friend_request(user["token"], requester_id):
                print(f"{user['username']} a refusé {req.get('username', requester_id)}")
                blocked_count += 1
        time.sleep(0.3)

# ════════════════════════════════════════
# 4. ENVOI DE FICHIERS ENTRE AMIS ACCEPTÉS
# ════════════════════════════════════════
print("\n=== 4. Envoi de fichiers entre amis ===\n")

fake_file_contents = [
    b"Ceci est un rapport de projet confidentiel.",
    b"Liste des taches a faire pour le sprint.",
    b"Notes de reunion du jour.",
    b"Photo de vacances (simulee en texte).",
    b"Document important - ne pas perdre.",
]

users_by_id = {u["id_user"]: u for u in created_users}
files_sent_count = 0

for sender_id, receiver_id in accepted_pairs:
    sender = users_by_id.get(sender_id)
    if not sender:
        continue

    nb_files = random.randint(1, 2)
    for i in range(nb_files):
        content = random.choice(fake_file_contents)
        filename = f"document_{random.randint(100,999)}.txt"
        if send_file(sender["token"], receiver_id, content, filename):
            receiver_username = users_by_id.get(receiver_id, {}).get("username", receiver_id)
            print(f"{sender['username']} -> fichier envoyé à {receiver_username}")
            files_sent_count += 1
        time.sleep(0.4)

# ════════════════════════════════════════
# RÉCAPITULATIF FINAL
# ════════════════════════════════════════
print("\n" + "="*50)
print("RÉCAPITULATIF DU SEED")
print("="*50)
print(f"Utilisateurs créés        : {len(created_users)}")
print(f"Demandes d'amis envoyées  : {len(friend_pairs_sent)}")
print(f"Amitiés acceptées         : {len(accepted_pairs)}")
print(f"Demandes refusées/bloquées: {blocked_count}")
print(f"Fichiers envoyés          : {files_sent_count}")
print("\nComptes créés (mail / password / password_pgp) :")
for u in created_users:
    print(f"  - {u['mail']} / {u['password']} / pgp:{u['password_pgp']}")
print("\nScript terminé. Va vérifier /admin/overview et /admin/users sur Swagger !")