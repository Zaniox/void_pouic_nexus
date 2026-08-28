# ⚡ VOID POUIC NEXUS : TRANSCENDENCE EDITION

> **Jeu d'arcade cyberpunk rythmé et ultra-réactif développé en Python pur (Zero Dépendance).**  
> *Architecture par @zanioxx_off*

---

## 🌌 Aperçu

**VOID POUIC NEXUS : TRANSCENDENCE** est un jeu réflexe haute cadence combinant synchronisation visuelle, effets de distorsion néon, visualiseur audio temps réel et synthèse sonore PCM spatialisée à 44.1 kHz via l'API WinMM.

![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%2B-blue?style=for-the-badge&logo=python)
![Dependencies](https://img.shields.io/badge/Dependencies-0%20(Pure%20Standard%20Lib)-brightgreen?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)

---

## ✨ Fonctionnalités Majeures

- 🎧 **Moteur Audio PCM Spatialisé (44.1 kHz)** : Synthèse d'ondes procédurales stéréo (onde Pouic élastique, sub-bass slam, résonance nodale stéréo).
- 🎨 **4 Thèmes Cyberpunk Glassmorphism** :
  - *VOID AMETHYST*
  - *CYBER ICE*
  - *SOLAR FLARE*
  - *MATRIX NEON*
- ⚡ **Système de Précision & Overdrive** :
  - Évaluations : `PERFECT!`, `GREAT!`, `GOOD`.
  - Mode Fever Overdrive (Multiplicateur de score x2).
  - Étape centrale : **POUIC SLAM** destructeur.
- 📊 **Télémétrie & Statistiques en direct** : Graphique d'historique de réaction (ms), compteur CPS, rangs de maîtrise (Novice à Void Emperor).
- 🖥️ **Zéro Dépendance externe** : Fonctionne directement avec la bibliothèque standard Python (`tkinter`, `ctypes`, `wave`, `math`, `threading`).

---

## 🎮 Contrôles

| Action | Clavier / Raccourci | Souris |
| :--- | :--- | :--- |
| **Séquence P-O-U-I-C** | Touches <kbd>P</kbd> <kbd>O</kbd> <kbd>U</kbd> <kbd>I</kbd> <kbd>C</kbd> | Clic gauche sur les orbes |
| **POUIC SLAM** | <kbd>ESPACE</kbd> ou <kbd>ENTRÉE</kbd> ou <kbd>P</kbd> | Clic sur le réacteur central |
| **Changer de Thème** | <kbd>T</kbd> | Via Paramètres |
| **Ajuster le Volume** | <kbd>+</kbd> / <kbd>-</kbd> | — |
| **Couper le Son** | <kbd>M</kbd> | — |
| **Plein Écran** | <kbd>F11</kbd> | — |
| **Retour / Quitter** | <kbd>ÉCHAP</kbd> | — |

---

## 🚀 Installation & Lancement

### Prérequis
- **Système** : Windows 10 / 11
- **Python** : Python 3.10 ou supérieur

### Lancement direct
```bash
python main.py
```
*(ou double-cliquez sur `main.py`)*

---

## 📁 Structure du Projet

```text
void-pouic-nexus/
├── main.py          # Script principal du jeu (Moteur, UI, Audio)
├── README.md        # Présentation et documentation
├── requirements.txt # Spécifications des dépendances
└── .gitignore       # Fichiers ignorés par Git
```

---

## 📜 Licence

Projet sous licence libre — Développé avec passion par **@zanioxx_off**.
