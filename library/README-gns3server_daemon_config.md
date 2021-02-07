[![Licence](https://img.shields.io/github/license/pamioc/ansible-gns3vm.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Debian 10](https://img.shields.io/badge/debian-10-da1e4e.svg)](https://www.debian.org)
[![Python 3.7](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org)
[![Ansible 2.10](https://img.shields.io/badge/ansible-2.10%2B-black.svg)](https://www.ansible.com)
[![GNS3 2.2.17](https://img.shields.io/badge/gns3server-2.2.17-00bfff.svg)](https://www.gns3.com)

# gns3server_daemon_config

Module ansible de génération du fichier de configuration du démon gns3server dans le cadre de l'installation d'un serveur GNS3 VM.  
Si le fichier de configuration est déjà présent, la configuration est modifiée uniquement si l'option `force` est activée.

#### Systèmes supportés

- Linux Debian 10.  
  Ce module n'a pas été testé sur d'autres distributions Linux mais il devrait fonctionner également. 

#### Versions de GNS3 supportées

- GNS3 v2.2.17 est supportée par ce module.  
  Ce module n'a pas été testé avec les versions antérieures de GNS3 mais il devrait fonctionner depuis la version 2.2.4.  

## Prérequis

**Manageur Ansible :**
- Ansible v2.10

**Cible :**
- Python 3
- gns3server

## Options

| Nom | Description | Type | Par défaut | Requis |
|:-:|:-:|:-:|:-:|:-:|
| `config-file` | Nom du fichier de configuration du démon gns3server. | Chaîne | `/etc/gns3/gns3_server.conf` | Non |
| `force` | Force la modification du fichier de configuration du démon gns3server si il existe déjà. | Booléen | `False` | Non |
| `debug` | Activation du mode debug du module. | Booléen | `False` | Non |
| `data-root` | Emplacement de stockage des répertoires :<br>projects, images, configs, appliances et symbols. | Chaîne | `/opt/gns3` | Non |
| `interface` | Nom de l'interface réseau d'écoute du démon gns3server. | Chaîne |  | Oui |
| `port` | Numéro du port d'écoute du démon gns3server. | Entier | `3080` | Non |
| `auth` | Option permettant d'activer l'authentification HTTP. | Booléen | `False` | Non |
| `user` | Nom d'utilisateur pour l'authentification HTTP. | Chaîne | `gns3` | Non |
| `password` | Mot de passe pour l'authentification HTTP. | Chaîne | `gns3` | Non |
| `enable_kvm` | (Qemu) Accès avec permissions lecture/écriture au périphérique KVM (/dev/kvm). | Booléen | `True` | Non |
| `require_kvm` | (Qemu) Exiger l'installation de KVM pour pouvoir démarrer les VM. | Booléen | `True` | Non |
| `enable_hardware_acceleration` | Activer l'accélération matérielle. | Booléen | `True` | Non |
| `require_hardware_acceleration` | Nécessite une accélération matérielle pour démarrer les VM. | Booléen | `False` | Non |

## Utilisation

Exemple de la définition d'une tâche de configuration par défaut seulement si le fichier de configuration n'existe pas :
- Utilisation du fichier de configuration : `/etc/gns3/gns3_server.conf`.
- Détection de l'adresse IP sur l'interface réseau `eth0`.
```yaml
- name: "Configuration par défaut en utilisant l'interface eth0"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    interface: "eth0"
```

Exemple de la définition d'une tâche de configuration par défaut ou modification de la configuration actuelle :
- Utilisation du fichier de configuration : `/etc/gns3/gns3_server.conf`.
- Détection de l'adresse IP sur l'interface réseau `eth0`
```yaml
- name: "Configuration en utilisant l'interface d'écoute eth0"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    force: true
    interface: "eth0"
```

Exemple de la définition d'une tâche de configuration par défaut :
- Utilisation du fichier de configuration : `/etc/gns3/gns3_server.conf`.
- Détection de l'adresse IP sur l'interface réseau `eth0`
- Activation et définition de l'authentification HTTP.
```yaml
- name: "Configuration par défaut utilisant eth0 et définition de l'authentification HTTP"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    interface: "eth0"
    auth: true
    user: admin
    password: MotDePasse
```

Exemple de la définition d'une tâche de configuration par défaut ou modification de la configuration actuelle :
- Utilisation du fichier de configuration : `/etc/gns3/gns3_server.conf`.
- Détection de l'adresse IP sur l'interface réseau `eth0`
- Désactivation du pré-requis KVM (Démarrage de VM Qemu impossible).
- Activation du mode debug du module.
```yaml
- name: "Configuration en utilisant l'interface d'écoute eth0, désactivation du pré-requis KVM (Démarrage de VM Qemu normalement impossible) et activation du mode debug du module"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    force: true
    debug: true
    interface: "eth0"
    require_kvm: false
```

## Valeurs de retour

**Les valeurs sont retournées uniquement si l'option `debug` est activée.**

Exemple de paramètres transmis au module :
```json
parametres: {
 "force": true,
 "debug": true,
 "interface": "eth0",
 "require_kvm": false
}
```

Exemple de paramètres de la configuration actuelle si il en existe une :
```json
config_actuelle: {
  "Server": {
    "host": "0.0.0.0",
    "port": 3080,
    "auth": false,
    "user": "gns3",
    "password": "gns3"
  },
  "IOU": {
    "license_check": true
  },
  "Qemu": {
    "enable_kvm": false,
    "require_kvm": false
  }
}
```

Exemple de paramètres de la configuration qui seront appliqués :
```json
config_daemon: {
  "Server": {
    "host": "192.168.10.21",
    "port": 3080,
    "auth": true,
    "user": "gns3",
    "password": "gns3"
  },
  "IOU": {
    "license_check": true
  },
  "Qemu": {
    "enable_kvm": true,
    "require_kvm": true
  }
}
```

## Auteur

Pascal MIRALLES
