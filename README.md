# SFTp

Secure file transfer between connected people

BDD : MySQL

Languages:
- HTML
- CSS
- JS
- SQL
- PHP
- XML

## Mise en place du projet sur Linux

### Commande:

#### Installation Docker:

```
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt install docker.io docker-compose docker-buildx
```
#### Docker compose:

```
cd SFTp/
sudo docker compose up --build -d
```

