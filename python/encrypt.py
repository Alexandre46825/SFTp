import gnupg

gpg = gnupg.GPG(gnupghome='/tmp/mygpg')

# Chiffrer un fichier
with open('nobody.mkv', 'rb') as f:
    encrypted = gpg.encrypt_file(
        f,
        recipients=['alice@exemple.fr'],  # destinataire(s)
        always_trust=True,
        output='nobody.gpg',        # fichier de sortie
    )
