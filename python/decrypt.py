import gnupg

gpg = gnupg.GPG(gnupghome='/tmp/mygpg')

with open('nobody.gpg', 'rb') as f:
    decrypted = gpg.decrypt_file(
        f,
        passphrase='mot_de_passe_secret',
        output='nobody_dechiffre.mkv',
    )
