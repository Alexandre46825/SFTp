# SFTp

Secure file transfer between connected people

BDD : MySQL

Languages:
- HTML
- CSS
- JS
- SQL


## Project setup on Linux

### Commands:

#### Docker installation steps:

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

## Front-End Overview

The front-end of this project is built with **Vue 3 (Composition API)** and follows a modular architecture based on components, views, and Pinia stores.

We use:
- **Vue Router** for navigation between pages (dashboard, files, friends, admin, etc.)
- **Pinia** for centralized state management (auth, files, friends, admin data)
- **Axios** to communicate with the REST API
- **TailwindCSS** for styling, including full **dark mode support**

The application is designed as a **Single Page Application (SPA)** with a strong separation between UI, state, and API layers. Data is dynamically updated through store actions to ensure a reactive user experience without page reloads.

### Admin account

```
admin@uniza.sk
```
password:

```
admin
```

### User account

```
alexandre@uniza.sk
```
password:

```
alexandre
```

