# Snake Web Edition - Final Version

Version finale du projet Snake : une **IHM web offline-first** deployable sur **GitHub Pages**, inspiree visuellement du Snake de Google.

## Pourquoi JavaScript

GitHub Pages sert des fichiers statiques (HTML/CSS/JS). Une app Python interactive cote serveur n'est donc pas adaptee sans couche supplementaire.

Pour cette version finale, le jeu est implemente en **JavaScript** (client-side), sans dependance externe.

## Fonctionnalites finales

- Ecran d'accueil avec configuration avant lancement.
- Deux modes jouables :
  - `Classique` (1 fruit simultane)
  - `MultiFruit` (plusieurs fruits simultanes)
- Tailles de map : Tres-petite, Petite, Moyenne, Grande, Tres grande.
- Vitesses : Lent, Normal, Rapide.
- Score en temps reel.
- Gestion de pause / reprise / relance.
- Controles clavier + boutons tactiles.
- Rendu canvas avec style inspire du Snake Google.
- Deploiement direct sur GitHub Pages via dossier `docs/`.

## Lancer en local

Option simple :

```bash
python3 -m http.server 8000 --directory docs
```

Puis ouvrir :

- [http://localhost:8000](http://localhost:8000)

## Deploiement GitHub Pages

1. Pousser ce repo sur GitHub.
2. Aller dans `Settings` > `Pages`.
3. Choisir :
   - `Source`: `Deploy from a branch`
   - `Branch`: `main`
   - `Folder`: `/docs`
4. Sauvegarder.

Le site sera publie automatiquement.

## Controles

- Deplacement : Fleches, `ZQSD` ou `WASD`
- Pause/Reprise : `P`
- Relancer : `R`

## Architecture

```text
.
├── docs
│   ├── .nojekyll
│   ├── index.html
│   ├── styles.css
│   └── js
│       ├── app.js
│       ├── config.js
│       ├── engine.js
│       └── renderer.js
├── snake_game           # version terminal legacy (historique)
├── tests                # tests de la version terminale legacy
├── main.py              # point d'entree terminal legacy
└── pyproject.toml
```

## Notes

- La version web est la **version finale de reference**.
- Le code Python terminal est conserve comme historique/compatibilite.
