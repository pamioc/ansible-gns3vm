[![Licence](https://img.shields.io/github/license/pamioc/ansible-gns3vm.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Debian 10](https://img.shields.io/badge/debian-10-da1e4e.svg)](https://www.debian.org)
[![Python 3.7](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org)
[![Ansible 2.10](https://img.shields.io/badge/ansible-2.10%2B-black.svg)](https://www.ansible.com)

# verif_sys

Module Ansible de vérification des prérequis CPU, KVM et TUN/TAP pour l'installation d'un serveur GNS3 VM.

#### Systèmes supportés :

Linux Debian.

## Prérequis

**Manageur Ansible :**
- Ansible v2.10

**Cible :**
- Python v3

## Options

Nom | Description | Type | Par défaut | Requis
:-: | - | :-: | :-: | :-:
`cpu` | Vérification de la compatibilité du processeur (Drapeau VMX/SVM) | Booléen | `True` | Non
`kvm` | Vérification de la présence du périphérique de virtualisation KVM | Booléen | `True` | Non
`tun` | Vérification de la présence du périphérique réseau virtuel TUN/TAP | Booléen | `True` | Non

## Utilisation

Exemples d'une tâche de vérification de tous les périphériques :
```yaml
---
- name: "Vérification de tous les périphériques"
  verif_sys:
    cpu: True
    kvm: True
    tun: True
```
Exemples d'une tâche de vérification des périphériques en excluant le contrôle du processeur :
```yaml
---
- name: "Vérification des périphériques sauf le processeur"
  verif_sys:
    cpu: False
```

Exemples d'une tâche ne faisant aucune vérification des périphériques :
```yaml
---
- name: "Aucune vérification des périphériques"
  verif_sys:
    cpu: False
    kvm: False
    tun: False
```

## Auteur

Pascal MIRALLES
