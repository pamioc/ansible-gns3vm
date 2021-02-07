[![Licence](https://img.shields.io/github/license/pamioc/ansible-gns3vm.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Debian 10](https://img.shields.io/badge/debian-10-da1e4e.svg)](https://www.debian.org)
[![Python 3.7](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org)
[![Ansible 2.10](https://img.shields.io/badge/ansible-2.10%2B-black.svg)](https://www.ansible.com)

# docker_daemon_config

Module ansible de génération du fichier de configuration du démon docker dans le cadre de l'installation d'un serveur GNS3 VM.  
Si le fichier de configuration est déjà présent, la configuration est modifiée uniquement si l'option `force` est activée.

#### Systèmes supportés

- Linux Debian 10.  
  Ce module n'a pas été testé sur d'autres distributions Linux mais il devrait fonctionner également. 

#### Versions de Docker supportées

- Toutes les versions de docker sont supportées par ce module.

## Prérequis

**Manageur Ansible :**
- Ansible v2.10

**Cible :**
- Python 3
- Docker

## Options

| Nom | Description | Type | Par défaut | Requis |
|:-:|:-:|:-:|:-:|:-:|
| `config-file` | Nom du fichier de configuration du démon docker. | Chaîne | `/etc/docker/daemon.json` | Non |
| `force` | Intègre le(s) paramètre(s) au fichier de configuration<br>du démon docker si il(s) existe(nt) déjà. | Booléen | `False` | Non |
| `debug` | Activation du mode debug du module. | Booléen | `False` | Non |
| `data-root` | Emplacement de stockage des données docker. | Chaîne | `/var/lib/docker` | Non |
| `dns` | Liste de serveurs DNS à utiliser séparés par des virgules. | Chaîne |  | Non |
| `dns-search` | Liste de domaines de recherche DNS à utiliser séparés<br>par des virgules. | Chaîne |  | Non |

## Utilisation

Exemple de la définition d'une tâche de configuration d'un emplacement de stockage sans écraser la configuration actuelle en mode debug du module :
```yaml
- name: "Définition d'un emplacement de stockage en mode debug"
  docker_daemon_config:
    data-root: "/srv/docker"
    debug: true
```

Exemple de la définition d'une tâche de configuration d'un emplacement de stockage en modifiant la configuration actuelle si elle existe :
```yaml
- name: "Définition d'un emplacement de stockage forcé"
  docker_daemon_config:
    data-root: "/srv/docker"
    config-file: "/etc/docker/daemon.json"
    force: true
```

Exemple de la définition d'une tâche de configuration d'un emplacement de stockage et les paramètres DNS en modifiant la configuration actuelle si elle existe :
```yaml
- name: "Définition d'un emplacement de stockage et les paramètres DNS forcé"
  docker_daemon_config:
    data-root: "/srv/docker"
    force: true
    dns: "8.8.8.8,8.8.8.4"
    dns-search: "domain.local,reseau.lan"
```

## Valeurs de retour

**Les valeurs sont retournées uniquement si l'option `debug` est activée.**

Exemple de paramètres transmis au module :
```json
parametres: {
  "config-file": "/etc/docker/daemon.json",
  "data-root": "/srv/docker",
  "debug": true,
  "dns": "8.8.8.8,8.8.4.4",
  "dns-search": "domain.local,reseau.lan",
  "force": true
}
```

Exemple de paramètres de la configuration actuelle si il en existe une :
```json
config_actuelle: {
  "data-root": "/var/lib/docker"
}
```

Exemple de paramètres de la configuration qui seront appliqués :
```json
config_daemon: {
  "data-root": "/srv/docker",
  "dns": [
    "8.8.8.8",
    "8.8.8.4"
  ],
  "dns-search": [
    "domain.local",
	"reseau.lan"
  ]
}
```

## Auteur

Pascal MIRALLES
