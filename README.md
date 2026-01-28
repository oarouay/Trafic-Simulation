# Simulation de Trafic

Une simulation interactive de trafic urbain avec feux de circulation, voitures, piétons et véhicules d'urgence développée en Python avec Pygame.

## Description

Cette simulation présente une intersection avec :
- **Feux de circulation** automatiques avec cycle temporisé
- **Voitures** de différents types (compactes, berlines, coupés, sport, véhicules d'urgence)
- **Piétons** animés traversant aux passages piétons
- **Véhicules d'urgence** (police, ambulance) avec sirènes et feux clignotants
- **Détection de collision** et système d'évitement
- **Sons** (klaxons, sirènes)

## Prérequis

### Python
- Python 3.7 ou version supérieure

### Bibliothèques nécessaires

Installez Pygame avec pip :

```bash
pip install pygame
```

## Structure du projet

```
Trafic-Simulation-main/
├── main.py                    # Fichier principal à exécuter
├── Car.py                     # Classe des voitures
├── Pedestrian.py              # Classe des piétons
├── TrafficLight.py            # Classe des feux de circulation
├── TrafficLightController.py  # Contrôleur des feux
├── Button.py                  # Classe des boutons d'interface
├── assets/                    # Ressources graphiques et sonores
│   ├── cars/                  # Images des voitures
│   ├── pedestrians/           # Images des piétons
│   ├── trafficlight/          # Images des feux
│   ├── sound/                 # Fichiers audio
│   └── fonts/                 # Polices
└── README.md
```

## Installation et exécution

### 1. Cloner ou télécharger le projet
```bash
git clone <url-du-repo>
cd Trafic-Simulation-main
```

### 2. Installer les dépendances
```bash
pip install pygame
```

### 3. Exécuter le programme
```bash
python main.py
```

## Utilisation

### Menu principal
- **START** : Lancer la simulation
- **QUIT** : Quitter l'application

### Contrôles de la simulation
- **ESC** : Retourner au menu principal
- **Bouton FINISH** : Terminer la simulation
- **Clic souris** : Interaction avec les boutons

## Fonctionnalités

### Système de trafic
- **Feux adaptatifs** : Durée variable selon le trafic (5-15 secondes)
- **Extension intelligente** : +0.8 seconde par voiture en attente
- **Cycle de base** : Vert (adaptatif) → Jaune (2s) → Rouge
- **Alternance** : Nord-Sud / Est-Ouest
- **Respect des feux** : Véhicules civils s'arrêtent au rouge
- **Affichage temps réel** : Informations de trafic à l'écran

### Véhicules
- **Types** : Compacte, Berline, Coupé, Sport, Police, Ambulance
- **Couleurs** : Aléatoires selon le type
- **Vitesses** : Variables (1.0 à 3.0 unités/frame)
- **Sons** : Klaxons différents par véhicule

### Véhicules d'urgence
- **Priorité** : Passent au rouge
- **Effets visuels** : Feux clignotants (bleu/rouge pour police, rouge/blanc pour ambulance)
- **Audio** : Sirènes automatiques

### Piétons
- **Animation** : Marche avec alternance des pieds
- **Traversée** : Aux passages piétons
- **Évitement** : S'arrêtent devant les voitures

### Détection de collision
- Prévention des accidents voiture-voiture
- Prévention des accidents voiture-piéton
- Klaxon automatique en cas de danger

### Système adaptatif intelligent
- **Détection de trafic** : Compte les voitures en attente
- **Prolongation automatique** : Feu vert étendu selon la demande
- **Optimisation du flux** : Réduction des embouteillages
- **Limites intelligentes** : Durée min/max pour équité
- **Affichage en temps réel** : Statistiques de trafic visibles

## Configuration système

### Résolution d'écran
- **Menu** : 600x600 pixels
- **Simulation** : Taille adaptée à l'image d'intersection

### Performance
- **FPS** : 60 images par seconde
- **Spawn** : Voitures toutes les 1-3 secondes
- **Spawn** : Piétons toutes les 3-6 secondes

## Dépannage

### Erreurs communes

**"No module named 'pygame'"**
```bash
pip install pygame
```

**"FileNotFoundError: assets/..."**
- Vérifiez que le dossier `assets/` est présent
- Exécutez le programme depuis le répertoire `Trafic-Simulation-main/`

**Pas de son**
- Vérifiez que les fichiers audio sont présents dans `assets/sound/`
- Vérifiez les paramètres audio de votre système

### Problèmes de performance
- Réduisez le nombre de véhicules en modifiant `spawn_interval` dans `main.py`
- Fermez d'autres applications gourmandes en ressources

## Développement

### Modification des paramètres

**Durée des feux adaptatifs** (dans `TrafficLightController.py`) :
```python
self.base_green_duration = 5    # Durée minimum du vert
self.max_green_duration = 15    # Durée maximum du vert
self.extension_per_car = 0.8    # Secondes ajoutées par voiture
self.yellow_duration = 2        # Durée du jaune (fixe)
```

**Vitesse des véhicules** (dans `main.py`) :
```python
speed = random.uniform(1, 3.0)  # Vitesse min, max
```

**Fréquence d'apparition** (dans `main.py`) :
```python
spawn_interval = random.uniform(1, 3)  # Voitures
pedestrian_spawn_interval = random.uniform(3, 6)  # Piétons
```

## Auteur

Projet de simulation de trafic développé en Python/Pygame.

## Licence

Ce projet est à des fins éducatives et de démonstration.