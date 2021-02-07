[![Licence](https://img.shields.io/github/license/pamioc/ansible-gns3vm.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Debian 10](https://img.shields.io/badge/debian-10-da1e4e.svg)](https://www.debian.org)
[![Python 3.7](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org)
[![Ansible 2.10](https://img.shields.io/badge/ansible-2.10%2B-black.svg)](https://www.ansible.com)
![GitHub last commit](https://img.shields.io/github/last-commit/pamioc/ansible-gns3vm.svg)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/pamioc/ansible-gns3vm.svg?include_prereleases)
![GitHub downloads all releases](https://img.shields.io/github/downloads/pamioc/ansible-gns3vm/total.svg)

# Ansible GNS3 VM

Ce dépôt est destiné à l'installation d'un serveur GNS3 (GNS3 VM) et de ses compléments,
sur Linux Debian 10 (Buster) sans utiliser les paquets d'installation prévus pour Ubuntu.  
Cette méthode d'installation est une alternative à la [version téléchargeable](https://gns3.com/software/download-vm)
sous forme d'image système Ubuntu depuis le site GNS3.  
Cette installation est complétement automatisée grâce à l'exécution d'un playbook Ansible.  
Il n'est pas necéssaire que le manageur Ansible soit sur Linux Debian.

#### Compléments :

Les compléments suivants sont installés sur les cibles :
- **ubridge** : Pour la capture de paquets IP.
- **dynamips** : Emulateur de routeurs et switchs Cisco.
- **vpcs** : Simulation de PC.
- **Qemu** : Gestionnaire de machine virtuelle.
- **libvirt** : Interfaçage Cloud NAT.
- **docker** : Gestionnaire de container logiciel.
- Compatibilité **32 bits IOU** : Emulateur de routeurs et switchs Cisco.

#### Modules :

Ce dépôt intègre 3 modules personnalisés développé en python et s'exécutant sur les cibles par l'intermédiaire du playbook Ansible :
- [verif_sys](library/README-verif_sys.md "Module verif_sys") :
vérifie les pré-requis matériel pour l'hyperviseur KVM et les réseaux virtuels (TUN/TAP).
- [docker_daemon_config](library/README-docker_daemon_config.md "Module docker_daemon_config") :
Génère la configuration de docker.
- [gns3server_daemon_config](library/README-gns3server_daemon_config.md "Module gns3server_daemon_config") :
Génère la configuration de gns3-server.

#### Cibles :
Les cibles peuvent être des machines virtuelles ayant la virtualisation imbriquée activée (Nested Virtualization)
et ayant accès aux périphériques _/dev/kvm_ et _/dev/net/tun_ comme par exemple avec [Proxmox](https://pve.proxmox.com/wiki/Nested_Virtualization).  
L'avantage de cette installation est qu'elle est également possible sur des containers LXC plus économiques en ressources.

## Prérequis

**Manageur Ansible :**  
- Ansible v2.10 (n'a pas été testé avec les versions antérieures).  

**Cible :**  
- Processeur compatible avec le drapeau VMX ou SVM.
- Périphérique ***/dev/kvm*** si utilisation de machines virtuelles (Qemu).
- Périphérique ***/dev/net/tun*** pour la création de réseaux virtuels.
- Linux debian 10 (Buster) minimale.
- Python 3
- Accès SSH root par clé privée depuis le manageur Ansible.

## Installation

- Télécharger la [version compactée](https://github.com/pamioc/ansible-gns3vm/releases) et la décompresser sur le manageur Ansible.

ou

- Télécharger ce dépôt sur le manageur Ansible :  
`git clone https://github.com/pamioc/ansible-gns3vm.git`

## Configuration

Options de configuration globales :  
- `roles/commun/default/main.yml`

```yaml
---
# Variables globales
datadir: "/srv"
datadir_gns3: "{{ datadir }}/gns3"
datadir_docker: "{{ datadir }}/docker"
```

Configuration des hôtes cibles :  
- `inventories/staging`

```yaml
---
all:
  children:
    gns3server:
      hosts:
        node-cible1
        node-cible2
```

## Utilisation

- Déploiement complet d'un serveur GNS3 VM :  
`ansible-playbook -i inventories/staging main.yml`

- Déploiement d'un serveur GNS3 VM avec rédémarrage :  
`ansible-playbook -i inventories/staging main.yml -t "all,reboot"`

- Déploiement du complément ubridge :  
`ansible-playbook -i inventories/staging main.yml -t "ubridge"`

- Déploiement de gns3server, des compléments ubridge, dynamips et docker :  
`ansible-playbook -i inventories/staging main.yml -t "ubridge,dynamips,docker,gns3server"`

## Configurer GNS3 afin d'utiliser le serveur

Vous avez deux façons d'utiliser votre nouveau serveur GNS3 :
- [Connexion des clients GNS3.](https://docs.gns3.com/docs/getting-started/installation/one-server-multiple-clients)
- [En tant que ressources supplémentaires.](https://docs.gns3.com/docs/how-to-guides/configure-gns3-to-use-an-additional-remote-server)

## Auteur

Pascal MIRALLES
