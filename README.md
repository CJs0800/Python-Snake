# Snake Terminal (Python) - V1

Projet Python public orienté **offline first** : un Snake jouable directement dans le terminal, sans interface graphique et avec un rendu ASCII simple basé sur `print`.

## Objectif

Cette V1 pose une base propre, modulaire et maintenable, prête pour les évolutions futures (tailles de map, vitesses, modes, plusieurs fruits).

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

## Fonctionnalites V1

- Ecran/menu d'accueil :
  - commencer une partie (mode Classique),
  - afficher les evolutions a venir,
  - quitter.
- Mode jouable unique : **Classique**.
- Une map par defaut.
- Une seule nourriture simultanee.
- Le snake avance, mange, grandit et la partie se termine sur collision.
- Rendu terminal ASCII avec bordures visibles.
- Score affiche en continu.
- Fin de partie propre avec retour menu ou sortie.

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
│   └── renderer.py
└── tests
    └── test_logic.py
```

Separation des responsabilites :

- `models.py` : structures de donnees (etat, position, directions)
- `logic.py` : regles metier (deplacement, collisions, nourriture)
- `renderer.py` : rendu terminal (frames ASCII)
- `input_handler.py` : lecture clavier non bloquante
- `menu.py` : ecrans de navigation
- `app.py` : orchestration application (menu + boucle de jeu)
- `config.py` : constantes/configuration centralisee

## Tests

Tests unitaires simples sur la logique metier :

```bash
python3 -m unittest discover -s tests -v
```

## Roadmap (versions suivantes)

- V2 : choix de taille de map
- V3 : choix de vitesse
- V4 : plusieurs fruits simultanes
- V5 : modes de jeu additionnels
