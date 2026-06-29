import gnupg

gpg = gnupg.GPG(gnupghome='/tmp/mygpg')  # répertoire keyring temporaire

input_data = gpg.gen_key_input(
    key_type='RSA',
    key_length=4096,
    name_real='Alice Dupont',
    name_email='alice@exemple.fr',
    passphrase='mot_de_passe_secret',
)

key = gpg.gen_key(input_data)
print("Fingerprint :", key.fingerprint)

# Clé publique (partageable)
public_key = gpg.export_keys(key.fingerprint)
print(public_key)
# -----BEGIN PGP PUBLIC KEY BLOCK-----
# ...

# Clé privée (à garder secrète)
private_key = gpg.export_keys(
    key.fingerprint,
    secret=True,
    passphrase='mot_de_passe_secret'
)
print(private_key)
# -----BEGIN PGP PRIVATE KEY BLOCK-----
# ...
