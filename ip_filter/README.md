# IP Filter Forcepoint

## Description du projet

Ce projet est un **IP Filter Forcepoint** pour maintenir une **blacklist** d'adresses IP en filtrant des adresses IP à partir de divers sources externes comme des dépôts git. Ces sources externes sont sous la forme de liste d'adresses IP.

## Contexte de base

Ce projet a été créé à la suite d'un besoin de maintenir une blacklist d'adresses IP de manière **dynamique**, en l'actualisant automatiquement de manière régulière.

## Prérequis

Pour utiliser ce projet, il faut installer directement tous les paquets nécessaires à l'aide du fichier `requirements.txt`. Ceci est possible avec les commandes suivantes :

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install --upgrade pip
$ pip install -r ../requirements.txt
```

> :memo: **Note:** Assurez vous d'être dans le répertoire `ip_filter/` avant d'éxecuter les commandes.

## Exécuter l'IP Filter

Pour lancer le script, il suffit de se rendre dans à la racine du projet dans le dossier `forcepoint/` et d'entrer la commande suivante dans le terminal :

```bash
$ python3 /ip_filter/script2.py
```

## Structure du fichier de configuration

Voici la structure fichier de configuration ***config.yml*** qui stocke les paramètres de l'API Forcepoint.

```yaml
api_forcepoint:
  version: 1.0
  key: api_private_key
  url: http://api.url.com
  port: 80
```

> :bulb: **Tip:** Les valeurs indiquées ne sont que des exemples.
