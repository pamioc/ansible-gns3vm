#!/usr/bin/env python3
# -*- coding: UTF-8 -*
# Module de vérification des pré-requis CPU, KVM et TUN/TAP pour l'installation de GNS3 VM SERVER

# Copyright: (c) 2021, Pascal MIRALLES <miralles.p@orange.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: verif_sys
version_added: "1.0"
short_description: Vérification de périphériques CPU, KVM et TUN/TAP.
description: Module de vérification des pré-requis CPU, KVM et TUN/TAP pour l'installation d'un serveur GNS3 VM.
options:
  cpu:
    description:
      - Vérification de la compatibilité du processeur (Drapeau VMX/SVM).
    type: bool
    default: True
    required: False
  kvm:
    description:
      - Vérification de la présence du périphérique de virtualisation KVM.
    type: bool
    default: True
    required: False
  tun:
    description:
      - Vérification de la présence du périphérique réseau virtuel TUN/TAP.
    type: bool
    default: True
    required: False
author:
  - Pascal MIRALLES (@pamioc)
notes:
  - Support du mode de vérification C(check_mode).
seealso:

'''

EXAMPLES = r'''
- name: "Vérification des périphériques sauf le processeur"
  verif_sys:
    cpu: False

- name: "Aucune vérification des périphériques"
  verif_sys:
    cpu: False
    kvm: False
    tun: False

'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule  

# Chargement des modules necessaires
import os

# Fonction de récupération des information du CPU
def cpu_vmx_svm():
  with open('/proc/cpuinfo', 'r') as cpuinfo:
    for ligne in cpuinfo:
      data = ligne.replace('\t','').replace('\n','').split(':')
      if data[0] == 'flags':
        if 'vmx' in data[1] or 'svm' in data[1]:
          return True
  return False

# Definition de la fonction d'exécution du module
def run_module():
  # Définition des options
  module_args = dict(
    cpu = dict(type = bool, default = True, required = False),
    kvm = dict(type = bool, default = True, required = False),
    tun = dict(type = bool, default = True, required = False)
  )

  # Initialisation du dictionnaire de sortie
  result = dict(changed = False)

  # Création de l'objet module
  module = AnsibleModule(
    argument_spec = module_args,
    supports_check_mode = True
  )

  # Sortie si le mode de vérification est activé
  if module.check_mode:
    module.exit_json(**result)

  # Vérification de la compatibilité du CPU
  if module.params['cpu']:
    if not cpu_vmx_svm():
      module.fail_json(msg = "Drapeau VMX/SVM introuvable sur le CPU", **result)

  # Vérification de la présence du periphérique kvm
  if module.params['kvm']:
    if not os.path.exists("/dev/kvm"):
      module.fail_json(msg = "Périphérique kvm introuvable", **result)

  # Vérification de la présence du periphérique tun/tap
  if module.params['tun']:
    if not os.path.exists("/dev/net/tun"):
      module.fail_json(msg = "Périphérique tun/tap introuvable", **result)

  # Fin d'exécution normale
  #module.exit_json(changed = False, module_args = module.params)
  module.exit_json(**result)

# Définition de fonction principale
def main():
  run_module()

# Execution du programme
if __name__ == '__main__':
  main()

