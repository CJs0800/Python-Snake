# Snake Terminal (Python) - V3

Projet Python public orienté **offline first** : un Snake jouable directement dans le terminal, sans interface graphique et avec un rendu ASCII simple basé sur `print`.

## Objectif

Cette V3 ajoute la gestion de plusieurs vitesses de jeu tout en conservant une base propre, modulaire et maintenable pour les futures evolutions.

## Prerequis

- Python **3.11+**
- Terminal local (macOS, Linux, Windows)

## Lancer le jeu

Depuis la racine du projet :

```bash
python3 main.py
```

Alternative :

```bash
python3 -m snake_game
```

## Controles

- Deplacement : `ZQSD` ou `WASD` ou fleches
- Retour menu pendant une partie : `X`

## Fonctionnalites V3

- Ecran/menu d'accueil :
  - commencer une partie (mode Classique),
  - choisir la taille de map avant le lancement,
  - choisir la vitesse avant le lancement,
  - afficher les evolutions a venir,
  - quitter.
- Mode jouable unique : **Classique**.
- Cinq tailles de map disponibles :
  - Tres-petite (12x8)
  - Petite (16x10)
  - Moyenne (20x12)
  - Grande (28x16)
  - Tres grande (36x20)
- Une seule nourriture simultanee.
- Trois vitesses disponibles :
  - Lent
  - Normal
  - Rapide
- Le snake avance, mange, grandit et la partie se termine sur collision.
- Rendu terminal ASCII avec bordures visibles.
- Score affiche en continu.
- Fin de partie propre avec retour menu ou sortie.
- Recap au lancement de partie : map, vitesse, mode et controles.

## Architecture

```text
.
├── main.py
├── pyproject.toml
├── README.md
├── snake_game
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   ├── config.py
│   ├── input_handler.py
│   ├── logic.py
│   ├── menu.py
│   ├── models.py
│   ├── renderer.py
│   └── timing.py
└── tests
    ├── test_config.py
    └── test_logic.py
```

Separation des responsabilites :

- `models.py` : structures de donnees (etat, position, directions)
- `logic.py` : regles metier (deplacement, collisions, nourriture)
- `renderer.py` : rendu terminal (frames ASCII)
- `input_handler.py` : lecture clavier non bloquante
- `menu.py` : ecrans de navigation
- `app.py` : orchestration application (menu + boucle de jeu)
- `config.py` : constantes/configuration centralisee, y compris les presets de map et de vitesse
- `timing.py` : cadence de boucle de jeu (frame pacing)

## Tests

Tests unitaires simples sur la logique metier et la configuration :

```bash
python3 -m unittest discover -s tests -v
```

## Roadmap (versions suivantes)

- V4 : plusieurs fruits simultanes
- V5 : modes de jeu additionnels
