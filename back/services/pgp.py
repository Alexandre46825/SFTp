import gnupg
import os
import shutil
import uuid

def generate_pgp_keypair(user_id: int, name_real: str, name_email: str, passphrase: str):
    gnupghome = f"/tmp/gpg_{user_id}_{uuid.uuid4().hex[:8]}"
    os.makedirs(gnupghome, exist_ok=True)

    gpg = gnupg.GPG(gnupghome=gnupghome)

    input_data = gpg.gen_key_input(
        key_type='RSA',
        key_length=4096,
        name_real=name_real,
        name_email=name_email,
        passphrase=passphrase,
    )

    key = gpg.gen_key(input_data)

    public_key = gpg.export_keys(key.fingerprint)
    private_key = gpg.export_keys(
        key.fingerprint,
        secret=True,
        passphrase=passphrase
    )

    shutil.rmtree(gnupghome, ignore_errors=True)

    return public_key, private_key


def encrypt_file_pgp(file_bytes: bytes, recipient_public_key: str, recipient_email: str, tmp_id: str) -> bytes:
    unique_id = f"{tmp_id}_{uuid.uuid4().hex[:8]}"
    gnupghome = f"/tmp/gpg_op_{unique_id}"
    os.makedirs(gnupghome, exist_ok=True)
    gpg = gnupg.GPG(gnupghome=gnupghome)

    import_result = gpg.import_keys(recipient_public_key)
    if import_result.count == 0:
        shutil.rmtree(gnupghome, ignore_errors=True)
        raise ValueError("Échec de l'import de la clé publique du destinataire")

    encrypted = gpg.encrypt(
        file_bytes,
        recipients=[recipient_email],
        always_trust=True
    )

    shutil.rmtree(gnupghome, ignore_errors=True)

    if not encrypted.ok:
        raise ValueError(f"Échec du chiffrement PGP: {encrypted.status}")

    return encrypted.data