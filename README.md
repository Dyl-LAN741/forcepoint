![py](https://img.shields.io/badge/python-3.10-green?style=for-the-badge) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

# SMC Forcepoint Monitoring

## Build

- `exporter/`: script de création et d'exportation de métrics prometheus sur les informations des logs enregistrés sur **Forcepoint**.
- `ip_filter/`: script de mise à jour d'une blacklist dynamique d'adresses IP.
- `rundeck/`: script `ip_filter/` modifié pour être compatible avec un système **Rundeck**.
- `config.yml`: fichier de configation de l'API Forcepoint.

## Prérequis

Pour utiliser et lancer les scripts, il faut:

* Posséder [python](https://www.python.org/downloads/) >= version 3.6.

Vous pouvez également installer directement tous les paquets nécessaires à l'aide du fichier `requirements.txt`.
