# Exporter Forcepoint

## Description du projet

Ce projet est un **Exporter Forcepoint** pour l'exportation de metrics dans **Prometheus**. Ces metrics correspondent aux logs les plus récents enregistrés dans **Forcepoint**.

## Contexte de base

Ce projet a été créé à la suite d'un besoin de centralisation des alertes de logs provenant de différents applications de sécurité, d'antivirus ou de firewalls pour les transférer sur une application de visualisation de données permettant la visualisation sous la forme de graphiques et de tableaux de bord comme **Grafana** par exemple.

## Prérequis

Pour utiliser ce projet, il faut:
* Avoir [Docker](https://www.docker.com/get-started/) d'installé sur la machine.

## Installation de l'Exporter

Pour installer l'Exporter, il vous suffit de créer une image Docker du projet à l'aide du `Dockerfile` fournis. Pour ce faire, la commande est la suivante.

Dans le terminal, entrez la commande :

```bash
$ docker build . -t forcepoint_exporter
```
> :memo: **Note:** Assurez-vous d'être dans le répertoire du projet `forcepoint/` avant d'exécuter la commande ci-dessus

L'image **forcepoint_exporter** doit être créée : 

```bash
$ docker images
```

## Exécuter l'Exporter

Pour lancer l'Exporter, il suffit d'entrer la commande suivante dans le terminal :

```bash
$ docker run --rm -v </path/to/your/username>/forcepoint/config.yml:/forcepoint/config.yml -p 9401:9400 forcepoint_exporter
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

## Dashboard Grafana

Dans le fichier `Forcepoint-1685540516652.json` contient la configuration du dashboard au format *JSON* directement importable dans Grafana.

Voici à quoi ressemble le dashboard :

![ForcepointDashboard](https://edu-git.ac-versailles.fr/dharal1/forcepoint/-/blob/main/exporter/png/dashboard_forcepoint.png)
