
VS
VentaScope
Application de Collecte et Analyse Descriptive des Données de Ventes
INF 232 — EC2 : Analyse de données
TP : Développement d'une application de collecte des données en ligne

Étudiant
Nkoum Belinga Felix Berenger
Matière
INF 232 — EC2
Secteur
Commerce & Ventes — Cameroun
Technologie
Python — Streamlit + Plotly + Pandas
Email prof.
rollinfrancis28@gmail.com


1. Présentation de l'Application
VentaScope est une application web complète développée en Python avec le framework Streamlit. Elle permet la collecte structurée, la gestion et l'analyse descriptive automatique des données commerciales et de ventes.

L'application cible le secteur du Commerce et des Ventes au Cameroun, avec des paramètres adaptés au contexte local (10 régions, monnaie FCFA, noms de vendeurs locaux).

▸ Objectifs du TP
    • Collecter des données de ventes via un formulaire web interactif
    • Stocker et gérer les enregistrements en session
    • Produire une analyse descriptive automatique (statistiques + graphiques)
    • Exporter les données en CSV, JSON et Excel
    • Héberger l'application sur un serveur en ligne (Streamlit Cloud)

2. Qualités de l'Application
▸ Créativité et Imagination
L'application adopte un design sombre et moderne inspiré des outils de data analytics professionnels. Le nom VentaScope est affiché en grand avec son logo doré en haut de chaque page. Le secteur d'activité choisi — Commerce & Ventes au Cameroun — ancre l'outil dans un contexte réel et pertinent, avec :
    • Interface bicolore noir/or (identité visuelle forte)
    • Données de démonstration préchargées avec des vendeurs et produits camerounais
    • Adaptation aux 10 régions administratives du Cameroun
    • Monnaie FCFA et formats locaux

▸ Robustesse
    • Validation des champs obligatoires avant enregistrement
    • Gestion des erreurs avec messages clairs à l'utilisateur
    • Filtres multi-critères sur les données (catégorie, statut, recherche textuelle)
    • Calculs statistiques stables avec NumPy et Pandas
    • Export en 3 formats différents (CSV, JSON, Excel)

▸ Efficacité
    • Analyse descriptive mise à jour instantanément après chaque saisie
    • Navigation simple en 3 pages via sidebar
    • Graphiques interactifs avec Plotly (zoom, survol, filtrage)
    • Tableau de statistiques complet généré automatiquement
    • Déploiement en 1 clic sur Streamlit Cloud

3. Modules de l'Application

Module
Fonctionnalité
Technologies
➕ Saisie
Formulaire de collecte des ventes
Streamlit Forms
📋 Base de données
Tableau interactif + filtres + export
Pandas DataFrame
📊 Analyse descriptive
Statistiques + 5 graphiques interactifs
Plotly + NumPy

▸ Module 1 — Saisie des données
Le formulaire de saisie collecte les informations suivantes pour chaque transaction :

Champ
Type
Description
Date de vente
Date
Date de la transaction
Vendeur
Texte
Nom du vendeur responsable
Produit / Service
Texte
Désignation du produit vendu
Catégorie
Liste
Électronique, Informatique, Services…
Quantité
Nombre entier
Nombre d'unités vendues
Prix unitaire
Nombre (FCFA)
Prix par unité en FCFA
Région
Liste
10 régions du Cameroun
Canal de vente
Liste
Boutique, En ligne, Téléphone…
Statut
Liste
Complétée / En attente / Annulée
Client
Texte
Nom ou référence client (optionnel)
Remarques
Texte long
Observations diverses
Total (calculé)
Auto
Quantité × Prix unitaire

▸ Module 2 — Base de données
    • Affichage tabulaire de toutes les transactions enregistrées
    • Recherche en temps réel (texte libre sur tous les champs)
    • Filtres par catégorie et par statut (multi-sélection)
    • Compteur de résultats dynamique
    • Export CSV — format universel pour tableurs
    • Export JSON — format structuré pour développeurs
    • Export Excel (.xlsx) — format professionnel avec openpyxl
    • Réinitialisation complète de la base de données

▸ Module 3 — Analyse descriptive
L'onglet Analyse produit automatiquement les éléments suivants :

Indicateurs clés (KPIs) :
    • Nombre total de transactions enregistrées
    • Chiffre d'affaires total (hors ventes annulées)
    • Montant moyen par transaction
    • Transaction maximale enregistrée

Graphiques interactifs (Plotly) :
    • Camembert — Répartition des ventes par catégorie
    • Histogramme horizontal — Chiffre d'affaires par région
    • Courbe temporelle — Évolution du CA dans le temps
    • Camembert — Répartition par canal de vente
    • Barres — Distribution des statuts de transaction
    • Barres — Performance comparative des vendeurs

Tableau de statistiques descriptives :

Statistique
Variable : Prix unitaire
Variable : Quantité
Variable : Total
Effectif (N)
Calculé
Calculé
Calculé
Minimum
Calculé
Calculé
Calculé
Maximum
Calculé
Calculé
Calculé
Somme
Calculé
Calculé
Calculé
Moyenne (μ)
Calculé
Calculé
Calculé
Médiane
Calculé
Calculé
Calculé
Écart-type (σ)
Calculé
Calculé
Calculé
Q1 (25e percentile)
Calculé
Calculé
Calculé
Q3 (75e percentile)
Calculé
Calculé
Calculé
Variance
Calculé
Calculé
Calculé
Asymétrie (Skewness)
Calculé
Calculé
Calculé
Kurtosis
Calculé
Calculé
Calculé

Corrélations :
    • Matrice de corrélation (heatmap colorée)
    • Nuage de points : Prix unitaire vs Montant total
    • Nuage de points : Quantité vs Montant total (coloré par statut)

4. Architecture Technique

▸ Stack technologique
Bibliothèque
Version
Usage
streamlit
≥ 1.32.0
Framework web — interface utilisateur
pandas
≥ 2.0.0
Manipulation et analyse des données
numpy
≥ 1.24.0
Calculs statistiques (moyenne, écart-type…)
plotly
≥ 5.18.0
Graphiques interactifs
openpyxl
≥ 3.1.0
Export Excel (.xlsx)

▸ Structure des fichiers
Fichier
Description
app.py
Code source principal de l'application (Python)
requirements.txt
Liste des dépendances Python à installer
README.md / README.docx
Documentation complète de l'application

▸ Stockage des données
Les données sont stockées en mémoire via st.session_state de Streamlit. Cette approche garantit :
    • Persistance des données durant toute la session utilisateur
    • Aucune dépendance à une base de données externe
    • Déploiement simplifié sans configuration serveur
    • Des données de démonstration sont préchargées au premier lancement

5. Guide de Déploiement

▸ Méthode 1 — Streamlit Cloud (recommandé)
Streamlit Cloud est la plateforme officielle pour héberger les applications Streamlit. C'est gratuit et permanent.

Étape
Action
1
Créer un compte gratuit sur github.com
2
Créer un repository public nommé 'ventascope'
3
Uploader app.py et requirements.txt dans le repository
4
Aller sur share.streamlit.io et se connecter avec GitHub
5
Sélectionner le repository et le fichier app.py
6
Cliquer sur 'Deploy' — le lien est généré en 2 minutes

Lien de l'application : https://ventascop2000-aclutdsvqwhcymrikttbd7.streamlit.app/

▸ Méthode 2 — Execution locale
Pour tester l'application en local avant déploiement :

Commande
Description
pip install -r requirements.txt
Installer toutes les dépendances
streamlit run app.py
Lancer l'application en local
http://localhost:8501
URL d'accès local dans le navigateur

6. Guide d'Utilisation

▸ Démarrage rapide
    • Ouvrir le lien de l'application dans un navigateur web
    • Des données de démonstration sont déjà préchargées
    • La navigation se fait via la barre latérale gauche (sidebar)

▸ Saisir une nouvelle vente
    • Cliquer sur '➕ Saisie des données' dans la sidebar
    • Remplir les champs obligatoires : Date, Vendeur, Produit, Quantité, Prix
    • Le total est calculé automatiquement (aperçu en bas du formulaire)
    • Cliquer sur '✓ Enregistrer' pour valider la transaction

▸ Consulter et exporter les données
    • Cliquer sur '📋 Base de données' dans la sidebar
    • Utiliser la barre de recherche pour filtrer par mot-clé
    • Appliquer des filtres par catégorie ou statut
    • Cliquer sur 'Export CSV', 'Export JSON' ou 'Export Excel' pour télécharger

▸ Analyser les données
    • Cliquer sur '📊 Analyse descriptive' dans la sidebar
    • Les 4 KPIs s'affichent automatiquement en haut
    • Onglet 'Graphiques' : 6 graphiques interactifs (zoom, survol)
    • Onglet 'Statistiques' : tableau complet des 12 indicateurs
    • Onglet 'Corrélations' : matrice et nuages de points

7. Lien de l'Application

🔗 Lien de l'application en ligne
https://ventascop2000-aclutdsvqwhcymrikttbd7.streamlit.app/
Application déployée et accessible en ligne 24h/24

Email du professeur : rollinfrancis28@gmail.com
Objet suggéré : TP INF 232 EC2 — VentaScope — Nkoum Belinga Felix Berenger

VentaScope — INF 232 EC2 — Nkoum Belinga Felix Berenger
