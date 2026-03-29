import re

with open('rapport.tex', 'r') as f:
    content = f.read()

# Replace Data Generation Section
old_data_section = r"\\subsection\{Génération et Structure des Données\}.*?\\subsection\{Prétraitement et Normalisation\}"
new_data_section = r"""\\subsection{Génération et Structure des Données}
Le jeu de données a été construit en simulant les caractéristiques métadonnées de fichiers PE sains (Label 0) et malveillants (Label 1). Pour chaque exécutable, 5 descripteurs (features) ont été retenus :
\\begin{itemize}
    \\item \\textbf{SizeOfImage} : La taille en mémoire de l'exécutable.
    \\item \\textbf{Entropy} : L'entropie de Shannon calculée sur les octets du fichier. Une entropie élevée (ex. $> 7.0$) est souvent corrélée à un code condensé (packé) ou chiffré, technique courante chez les malwares.
    \\item \\textbf{NumberOfSections} : Le nombre de sections définies dans l'en-tête PE.
    \\item \\textbf{Imports} : Le nombre de fonctions importées depuis des DLL externes. Un nombre anormalement faible ou ciblé peut être suspect.
    \\item \\textbf{Exports} : Le nombre de fonctions exportées (surtout pertinent pour les DLL).
\\end{itemize}

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.7\\textwidth]{images/class_distribution.png}
    \\caption{Distribution équilibrée des classes (Sain vs Malveillant)}
\\end{figure}

L'analyse exploratoire a mis en évidence des comportements distincts selon la nature du fichier. Par exemple, la distribution de l'entropie montre une nette tendance des malwares à présenter une entropie élevée (souvent supérieure à 7), indiquant possiblement l'utilisation de techniques de packing (compression/chiffrement) destinées à obfusquer le code malveillant.

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.7\\textwidth]{images/entropy_distribution.png}
    \\caption{Distribution de l'entropie selon la nature du fichier}
\\end{figure}

Afin d'évaluer la pertinence de chaque variable, une matrice de corrélation a été calculée. Elle permet de s'assurer qu'aucune caractéristique n'est redondante (colinéarité) et identifie les relations éventuelles avec la variable cible (Label).

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.7\\textwidth]{images/correlation_matrix.png}
    \\caption{Matrice de corrélation des caractéristiques}
\\end{figure}

\\subsection{Prétraitement et Normalisation}"""

content = re.sub(old_data_section, new_data_section, content, flags=re.DOTALL)

# Replace Evaluation Section
old_eval_section = r"\\subsection\{Résultats de l'Évaluation\}.*?\\section\{Optimisation du Modèle Champion\}"
new_eval_section = r"""\\subsection{Résultats de l'Évaluation}
La métrique clé retenue pour l'évaluation est le \\textbf{F1-Score}, car il offre un compromis optimal entre le Rappel (détection exhaustive des menaces) et la Précision (limitation des faux positifs) :
\\[ F1 = 2 \\cdot \\frac{\\text{Précision} \\cdot \\text{Rappel}}{\\text{Précision} + \\text{Rappel}} \\]

Les résultats obtenus sur l'ensemble de test (30\\% des données) montrent d'excellentes performances globales. Le tableau et le graphique comparatifs ci-dessous mettent en évidence ces résultats :

\\begin{table}[H]
    \\centering
    \\begin{tabular}{|l|c|c|c|}
    \\hline
    \\textbf{Modèle} & \\textbf{F1-Score} & \\textbf{Précision} & \\textbf{Rappel} \\\\ \\hline
    SVM & \\textbf{1.0000} & 1.0000 & 1.0000 \\\\ \\hline
    Random Forest & 0.9983 & 0.9967 & 1.0000 \\\\ \\hline
    KNN & 1.0000 & 1.0000 & 1.0000 \\\\ \\hline
    \\end{tabular}
    \\caption{Comparaison des performances des modèles évalués}
\\end{table}

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.7\\textwidth]{images/model_comparison.png}
    \\caption{Comparatif visuel des F1-Scores}
\\end{figure}

Bien que le KNN affiche également un score parfait sur ce dataset synthétique, le \\textbf{SVM} a été désigné \\textit{Modèle Champion} pour la suite, compte tenu de sa capacité de généralisation et de sa robustesse reconnue face aux problèmes de classification de malwares en haute dimension.

\\section{Optimisation du Modèle Champion}"""

content = re.sub(old_eval_section, new_eval_section, content, flags=re.DOTALL)

with open('rapport.tex', 'w') as f:
    f.write(content)

print("Rapport mis à jour.")
