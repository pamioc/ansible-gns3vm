#!/usr/bin/env python3
# -*- coding: UTF-8 -*
# Module de création de fichier de configuration du service DOCKER

# Copyright: (c) 2021, Pascal MIRALLES <miralles.p@orange.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
module: docker_daemon_config
version_added: "1.0"
short_description: Configuration du démon docker
description: Module de génération du fichier de configuration du démon docker dans le cadre de l'installation d'un serveur GNS3 VM.
  Si le fichier de configuration est déjà présent, la configuration est modifiée uniquement si l'option `force` est activée.
options:
  data-root:
    description:
      - Emplacement de stockage des données docker.
    type: str
    default: "/var/lib/docker"
    required: False

  dns:
    description:
      - Liste de serveurs DNS à utiliser séparés par des virgules.
    type: str
    required: False

  dns-search:
    description:
      - Liste de domaines de recherche DNS à utiliser séparés par des virgules.
    type: str
    required: False

  config-file:
    description:
      - Nom du fichier de configuration du démon docker.
    type: str
    default: "/etc/docker/daemon.json"
    required: False

  force:
    description:
      - Force la modification du fichier de configuration du démon docker si il existe déjà.
    type: bool
    default: False
    required: False

  debug:
    description:
      - Activation du mode debug du module.
      - Affichage de variables dans la sortie du module.
    type: bool
    default: False
    required: False

author:
  - Pascal MIRALLES (@pamioc)
notes:
  - Support du mode de vérification C(check_mode).
seealso:

'''

EXAMPLES = r'''
- name: "Définition d'un emplacement de stockage sans écraser la configuration actuelle en mode debug du module"
  docker_daemon_config:
    data-root: "/srv/docker"
    debug: true

- name: "Définition d'un emplacement de stockage en modifiant la configuration actuelle si elle existe"
  docker_daemon_config:
    data-root: "/srv/docker"
    config-file: "/etc/docker/daemon.json"
    force: true

- name: "Définition d'un emplacement de stockage et les paramètres DNS en modifiant la configuration actuelle si elle existe"
  docker_daemon_config:
    data-root: "/srv/docker"
    force: true
    dns: "8.8.8.8,8.8.8.4"
    dns-search: "domain.local,reseau.lan"

'''

RETURN = r'''
parametres:
  description: Les paramètres transmis au module.
  returned: mode debug
  type: dict
  sample: {
    "data-root": "/srv/docker",
    "debug": true,
    "config-file": "/etc/docker/daemon.json",
    "force": true
  }

config_actuelle:
  description: Les paramètres de la configuration actuelle si il en existe une.
  returned: mode debug
  type: dict
  sample: {
    "data-root": "/var/lib/docker"
  }

config_daemon:
  description: Les paramètres de la configuration qui seront appliqués.
  returned: mode debug
  type: dict
  sample: {
    "data-root": "/srv/docker",
    "dns": [ "8.8.8.8", "8.8.4.4" ],
    "dns-search": [ "domain.local", "reseau.lan" ]
  }

'''

from ansible.module_utils.basic import AnsibleModule

# Chargement des modules necessaires
import os
import json

# Définition de la fonction de lecture du fichier actuel
def lecture_config(fichier):
  valeurs = dict()
  with open(fichier, "r") as f:
    parametres = json.load(f)
    valeurs.update(parametres)
  return valeurs

# Définition de la fonction d'enregistrement du fichier de configuration
def ecriture_config(fichier, parametres):
  try:
    with open(fichier, 'w') as f:
      json.dump(parametres, f, indent = 2)
    return True
  except IOError:
    return False

# Définition de la fonction de mise à jour de la configuration
def maj_config(config, parametres):
  import copy
  # Création de la variable de configuration finale
  configuration = copy.deepcopy(config)
  # Si aucune section Server alors la configuration actuelle est vide
  # donc on crée une configuration par défaut
  if len(configuration) == 0:
    configuration = {
      'data-root': '/var/lib/docker'
    }

  # Définition du modèle de la configuration globale
  modele_config = {
    'str': (
      'data-root'
    ),
    'list': (
      'dns', 'dns-search'
    ),
    'bool': (
    )
  }

  # On adapte les paramètres
  for option in parametres:
    if parametres[option] == None:
      continue
    for type in modele_config:
      if modele_config[type].count(option) > 0:
        if type == 'str':
          configuration[option] = str(parametres[option])
        elif type == 'list':
          configuration[option] = parametres[option].split(',')
        elif type == 'bool':
          configuration[option] = eval(parametres[option].capitalize())

  return configuration

# Définition de la fonction d'exécution du module
def run_module():
  # Définition des options
  module_args = {
    'data-root': { 'type': str, 'required': False },
    'dns': { 'type': str, 'required': False },
    'dns-search': { 'type': str, 'required': False },
    'config-file': { 'type': str, 'default': '/etc/docker/daemon.json', 'required': False },
    'force': { 'type': bool, 'default': False, 'required': False },
    'debug': { 'type': bool, 'default': False, 'required': False }
  }

  # Initialisation du dictionnaire de sortie
  result = dict(changed = False)

  # Création de l'objet module
  module = AnsibleModule(
    argument_spec = module_args,
    supports_check_mode = True
  )

  # Ajout des paramètres dans la variable de retour en mode debug
  if module.params['debug']:
    result['parametres'] = module.params

  # Sortie si le mode de vérification est activé
  if module.check_mode:
    module.exit_json(**result)

  # Initialisation des variables de configuration
  config_daemon = dict()
  config_actuelle = dict()

  # Test si le fichier de configuration est présent
  if os.path.exists(module.params['config-file']):
    # Si l'option force est activé alors on lit le fichier de configuration
    if module.params['force']:
      config_actuelle = lecture_config(module.params['config-file'])
    # Sinon on sort car aucun paramètre ne sera enregistré
    else:
      module.exit_json(**result)

  # Ajout des paramètres dans la variable de retour en mode debug
  if module.params['debug']:
    result['config_actuelle'] = config_actuelle

  # Mise à jour des valeurs dans la variable configuration
  config_daemon = maj_config(config_actuelle, module.params)

  # Ajout des paramètres dans la variable de retour en mode debug
  if module.params['debug']:
    result['config_daemon'] = config_daemon

  # Test si la nouvelle configuration est différente
  if not config_daemon == config_actuelle:
    # Ecriture du fichier de configuration
    if not ecriture_config(module.params['config-file'], config_daemon):
      module.fail_json(msg = "Ecriture du fichier de configuration du service docker impossible", **result)
    else:
      # La modification de configuration a été effectuée
      result['changed'] = True

  # Fin d'exécution normale
  module.exit_json(**result)

# Definition de la fonction principale
def main():
  run_module()

# Execution du programme
if __name__ == '__main__':
  main()
