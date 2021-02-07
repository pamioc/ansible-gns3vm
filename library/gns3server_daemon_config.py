#!/usr/bin/env python3
# -*- coding: UTF-8 -*
# Module de création de fichier de configuration du service DOCKER

# Copyright: (c) 2021, Pascal MIRALLES <miralles.p@orange.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
module: gns3server_daemon_config
version_added: "1.0"
short_description: Configuration du démon gns3server.
description: Module de génération du fichier de configuration du démon gns3server.
options:
  config-file:
    description:
      - Nom du fichier de configuration du démon gns3server.
    type: str
    default: "/etc/gns3/gns3_server.conf"
    required: false

  force:
    description:
      - Force la modification du fichier de configuration du démon gns3server si il existe déjà.
    type: bool
    default: false
    required: false

  interface:
    description:
      - Nom de l'interface réseau d'écoute du démon gns3server.
    type: str
    required: true

  port:
    description:
      - Numéro du port d'écoute du démon gns3server.
    type: str
    default: 3080
    required: false

  data-root:
    description:
      - Emplacement de stockage des répertoires projects, images, configs, appliances et symbols.
    type: str
    default: /opt/gns3
    required: false

  auth:
    description:
      - Option permettant d'activer l'authentification HTTP.
    type: bool
    default: false
    required: false

  user:
    description:
      - Nom d'utilisateur pour l'authentification HTTP.
    type: str
    default: gns3
    required: false

  password:
    description:
      - Mot de passe pour l'authentification HTTP.
    type: str
    default: gns3
    required: false

  enable_kvm:
    description:
      - (Qemu) Accès avec permissions lecture/écriture au périphérique KVM (/dev/kvm).
      - A priorité sur enable_hardware_acceleration.
    type: bool
    default: true
    required: false

  require_kvm:
    description:
      - (Qemu) Exiger l'installation de KVM pour pouvoir démarrer les VM.
      - A priorité sur require_hardware_acceleration.
    type: bool
    default: true
    required: false

  enable_hardware_acceleration:
    description:
      - Activer l'accélération matérielle.
    type: bool
    default: true
    required: false

  require_hardware_acceleration:
    description:
      - Nécessite une accélération matérielle pour démarrer les VM.
    type: bool
    default: false
    required: false
 
  debug:
    description:
      - Activation du mode debug du module.
      - Affichage de variables dans la sortie du module.
    type: bool
    default: false
    required: false

author:
  - Pascal MIRALLES (@pamioc)
notes:
  - Support du mode de vérification C(check_mode).
seealso:

'''

EXAMPLES = r'''
- name: "Configuration par défaut en utilisant l'interface réseau `eth0` seulement si le fichier de configuration n'existe pas"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    interface: "eth0"

- name: "Configuration par défaut ou modification de la configuration actuelle en utilisant l'interface d'écoute eth0"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    force: true
    interface: "eth0"

- name: "Configuration par défaut utilisant eth0 et définition de l'authentification HTTP seulement si le fichier de configuration n'existe pas"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    interface: "eth0"
    auth: true
    user: admin
    password: MotDePasse

- name: "Définition ou modification de la configuration utilisant eth0, désactivation du pré-requis KVM (Démarrage de VM Qemu impossible) et activation du mode debug du module"
  gns3server_daemon_config:
    config-file: "/etc/gns3/gns3_server.conf"
    force: true
    debug: true
    interface: "eth0"
    require_kvm: false

'''

RETURN = r'''
parametres:
  description: Les paramètres transmis au module.
  returned: mode debug
  type: dict
  sample: {
    "force": true,
    "debug": true,
    "interface": "eth0",
    "require_kvm": false
  }

config_actuelle:
  description: Les paramètres de la configuration si il en existe une.
  returned: mode debug
  type: dict
  sample: {
    "Server": {
      "host": "0.0.0.0",
      "port": 3080,
      "auth": False,
      "user": "gns3",
      "password": "gns3"
    },
    "IOU": {
      "license_check": True
    },
    "Qemu": {
      "enable_kvm": False,
      "require_kvm": False
    }
  }

config_daemon:
  description: Les paramètres de la configuration qui seront appliqués.
  returned: mode debug
  type: dict
  sample: {
    "Server": {
      "host": "192.168.10.21",
      "port": 3080,
      "auth": True,
      "user": "gns3",
      "password": "gns3"
    },
    "IOU": {
      "license_check": True
    },
    "Qemu": {
      "enable_kvm": True,
      "require_kvm": True
    }
  }

'''

from ansible.module_utils.basic import AnsibleModule

# Chargement des modules necessaires
import os
import socket
import configparser

# Vérification de l'existence d'une interface réseau
def verif_interface_reseau(interface):
  val_ret = False
  try:
    socket.if_nametoindex(interface)
    val_ret = True
  except OSError:
    val_ret = False
  return val_ret

# Récupération de l'adresse IP d'une interface
def get_ip_address(ifname):
  import fcntl
  import struct
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return socket.inet_ntoa(fcntl.ioctl(
    s.fileno(),
    0x8915,  # SIOCGIFADDR
    struct.pack('256s', bytes(ifname[:15], 'utf-8'))
  )[20:24])

# Définition de la fonction de lecture du fichier actuel
def lecture_config(fichier):
  parametres = dict()
  config = configparser.ConfigParser()
  config.read(fichier)
  sections = config.sections()
  for section in sections:
    options = config.options(section)
    temp_dict = dict()
    for option in options:
      temp_dict[option] = config.get(section,option)
    parametres[section] = temp_dict
  return parametres

# Définition de la fonction d'enregistrement du fichier de configuration
def ecriture_config(fichier, parametres):
  config = configparser.ConfigParser()
  config.read_dict(parametres)
  config.update(parametres)
  try:
    with open(fichier, 'w') as f:
      config.write(f)
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
  if 'Server' not in configuration:
    if parametres['data-root'] != None:
      data_root = parametres['data-root']
    else:
      data_root = '/opt/gns3'
    configuration = {
      'Server': {
        'host': '0.0.0.0', 'port': '3080',
        'auth': 'False', 'user': 'gns3', 'password': 'gns3',
        'ssl': 'False',
        'configs_path': data_root + '/configs', 'images_path': data_root + '/images', 'projects_path': data_root + '/projects', 'appliances_path': data_root + '/appliances', 'symbols_path': data_root + '/symbols',
        'allowed_interfaces': 'virbr0,br0', 'default_nat_interface': 'virbr0'
      },
      'IOU': { 'iourc_path': data_root + '/iourc.txt', 'license_check': 'True' },
      'Qemu': {
        'enable_kvm': 'True', 'require_kvm': 'True',
        'enable_hardware_acceleration': 'True', 'require_hardware_acceleration': 'False'
      }
    }

  # Définition du modèle de la configuration globale
  modele_config = {
    'Server': (
      'host', 'port',
      'auth', 'user', 'password',
      'ssl', 'certfile', 'certkey',
      'configs_path', 'images_path', 'projects_path', 'appliances_path', 'symbols_path',
      'report_errors',
      'console_start_port_range', 'console_end_port_range', 'vnc_console_start_port_range', 'vnc_console_end_port_range',
      'udp_start_port_range', 'udp_end_port_range',
      'ubridge_path',
      'allowed_interfaces', 'default_nat_interface'
    ),
    'Dynamips': (
      'dynamips_path', 'allocate_aux_console_ports', 'mmap_support', 'sparse_memory_support', 'ghost_ios_support'
    ),
    'IOU': (
      'iourc_path', 'license_check'
    ),
    'Qemu': (
      'enable_kvm', 'require_kvm', 'enable_hardware_acceleration', 'require_hardware_acceleration'
    ),
    'VPCS': (
      'vpcs_path'
    )
  }
  # On adapte les paramètres
  for option in parametres:
    if parametres[option] == None:
      continue
    if option == 'interface':
        configuration['Server']['host'] = get_ip_address(parametres['interface'])
        #configuration.update({'Server': '{'host': get_ip_address(parametres['interface'])
        continue
    if option == 'data-root':
      for type in ( 'configs', 'images', 'projects', 'appliances', 'symbols'):
        configuration['Server'][type + '_path'] = parametres[option] + '/' + type
      continue
    for section in modele_config:
      if modele_config[section].count(option) > 0:
        if section not in configuration:
          configuration[section] = dict()
        configuration[section][option] = str(parametres[option])
        break
  return configuration

# Définition de la fonction d'exécution du module
def run_module():
  # Définition des options
  module_args = {
    'config-file': { 'type': str, 'default': '/etc/gns3/gns3_server.conf', 'required': False },
    'force': { 'type': bool, 'default': False, 'required': False },
    'interface': { 'type': str, 'required': True },
    'port': { 'type': int, 'required': False },
    'data-root': { 'type': str, 'required': False },
    'auth': { 'type': bool, 'required': False },
    'user': { 'type': str, 'required': False },
    'password': { 'type': str, 'required': False },
    'require_kvm': { 'type': bool, 'required': False },
    'enable_kvm': { 'type': bool, 'required': False },
    'enable_hardware_acceleration': { 'type': bool, 'required': False },
    'require_hardware_acceleration': { 'type': bool, 'required': False },
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

  # Vérification de la présence de l'interface réseau spécifiée
  if not verif_interface_reseau(module.params['interface']):
    module.fail_json(msg = "Interface [" + module.params['interface'] + "] introuvable", **result)

  # Initialisation des variables de configuration
  config_actuelle = dict()
  config_daemon = dict()

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

