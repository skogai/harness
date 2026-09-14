# Project 08. Dessinez votre workflow sous forme de graphe

> Cours associé : [L14. Des boucles simples à l'ingénierie des graphes](./../../lectures/lecture-14-graph-engineering/index.md)

## Ce que vous allez faire

C'est le projet de transition de « Loop » à « Graph ». Au cours précédent, vous avez construit un loop maker-checker — implémenter, vérifier, donner un retour, réimplémenter, toutes les décisions se produisant dans la fenêtre de contexte d'un seul agent. Dans ce cours, ce que vous allez faire, c'est **dessiner explicitement la structure cachée dans la boucle** : nœuds, arêtes, état partagé, règles de routage, écrits mot à mot.

Vous ferez trois expériences progressives : d'abord dessiner le loop maker-checker de P07 en graphe explicite, puis ajouter un nœud de fan-out/fan-in parallèle, et enfin ajouter une arête de retour conditionnelle et un nœud d'approbation humaine. Ce que vous ressentirez de bout en bout, c'est une chose : **le graphe n'est pas une invention ; c'est ce que votre loop devient de lui-même quand il devient suffisamment complexe.**

## De quoi vous avez besoin

- Claude Code ou Codex
- Git
- Le loop maker-checker que vous avez construit en P07 (ou n'importe quel workflow d'agent que vous pouvez faire tourner en boucle)
- Un éditeur de texte ou un outil de dessin (dessiner n'est pas pour faire joli, c'est pour écrire la structure clairement ; `mermaid` ou un `graph.md` écrit à la main feront l'affaire)

## Étapes concrètes

### Préparation

1. Partez du dépôt terminé en P07, ou utilisez directement n'importe quel workflow d'agent que vous faites tourner.
2. Créez trois branches : `p08-explicit-graph`, `p08-parallel`, `p08-human-in-the-loop`.
3. Préparez un `state.md` comme fichier d'état partagé : exigences, progression, résultats de vérification, tout s'y écrit. C'est le « plan de travail commun » du graphe.

### Expérience 1 : dessiner le Loop en graphe explicite

Passez sur la branche `p08-explicit-graph`.

1. **Listez tous les nœuds** : écrivez chaque étape du loop maker-checker de P07 comme un nœud. Pour chaque nœud, précisez : sa responsabilité, son entrée, sa sortie, s'il est un agent ou du code déterministe.
2. **Dessinez toutes les arêtes** : listez chaque arête entre les nœuds. Mettez en évidence deux arêtes spéciales :
   - Arête conditionnelle : vérification passée/échouée, quel chemin
   - Arête de retour arrière : en cas d'échec, on revient à quel nœud
3. **Écrivez l'état partagé** : listez explicitement les champs de l'état (exigences, code, résultats de test, conclusion de revue), qui les lit, qui les écrit.
4. **Écrivez les règles de routage** : avec le langage if-then le plus simple, écrivez les règles « où aller ensuite », par exemple :
   ```
   si la vérification passe → nœud de fusion
   si la vérification échoue → nœud d'implémentation
   si le nœud d'implémentation manque d'informations → nœud de recherche
   ```
5. **Écrivez `graph.md`** : organisez tout ce qui précède en un document. Dessinez un graphe avec mermaid, et joignez le tableau des nœuds et les règles de routage.
6. **Répondez à cette question** : une fois dessiné, trouvez au moins une **arête qui était implicite** — un chemin de décision qui était caché dans le contexte de l'agent, dont vous-même ne connaissiez pas l'existence.

### Expérience 2 : ajouter un nœud de Fan-out / Fan-in parallèle

Passez sur la branche `p08-parallel`.

1. **Choisissez un point parallélisable** : trouvez un endroit de la tâche qui peut être découpé en deux parties indépendantes. Par exemple :
   - L'implémentation découpée en deux modules indépendants, deux agents écrivent en parallèle
   - La vérification découpée en deux revues indépendantes : une qui exécute tests et lint, une qui fait la revue de code (instructions différentes, préoccupations différentes)
   - La recherche découpée en deux directions, deux agents explorent chacun une piste
2. **Écrivez la règle de fan-out** : dans l'état partagé, enregistrez « cette tâche est découpée en N sous-tâches parallèles », chaque sous-tâche ayant un contexte indépendant et un nœud indépendant.
3. **Écrivez la règle de fan-in** : une fois toutes les sous-tâches terminées, qui fusionne les résultats ? Quel est le critère de fusion (par exemple : fusionner seulement si les deux revues passent, ou s'il suffit qu'une passe) ?
4. **Isolez avec des worktrees** : chaque sous-tâche parallèle tourne dans son propre worktree git, pour éviter physiquement les collisions de fichiers (revenez sur la primitive Worktree du cours 13).
5. **Exécutez une fois et enregistrez** : notez le temps wall-clock avant/après le parallélisme, la consommation de tokens, la qualité du résultat. Le parallélisme est-il vraiment plus rapide ? Ou le coût de coordination mange-t-il le temps gagné ?

### Expérience 3 : ajouter une arête de retour arrière et un nœud d'approbation humaine

Passez sur la branche `p08-human-in-the-loop`.

C'est la plus importante des trois expériences. Vous allez ajouter deux types de nœuds au graphe :

1. **Arête de retour arrière conditionnelle** : ajoutez au nœud de vérification un chemin « partiellement passé » — au lieu de tout renvoyer au nœud d'implémentation, revenez avec un retour concret au **nœud qui a produit le problème**. Par exemple : si les tests passent tous mais que la revue de code révèle une erreur de compréhension des exigences, revenez au nœud de recherche plutôt qu'au nœud d'implémentation. Cela exige que votre état partagé enregistre « à quelle couche le problème s'est produit ».
2. **Nœud d'approbation humaine (Human-in-the-loop)** : ajoutez un nœud humain avant le nœud de fusion. À ce point, le graphe **s'arrête**, et attend que vous écriviez « approuvé » ou « rejeté » dans `state.md`. Le nœud d'approbation peut avoir une règle de timeout : sans réponse après N heures, rejet automatique ou escalade automatique.
3. **Écrivez le format de l'interruption** : comment l'approbation est-elle demandée clairement — ce qui s'est passé, ce qui a été modifié, pourquoi ça a besoin d'un humain, et quelles sont les conséquences de l'approbation ou du rejet.
4. **Exécutez au moins 2 cycles complets** : à chaque cycle, allez jusqu'au nœud d'approbation humaine, et approuvez ou rejetez une fois vous-même. Enregistrez : votre décision d'approbation correspond-elle au jugement du nœud de vérification ? Le nœud d'approbation a-t-il arrêté quelque chose que le nœud de vérification n'avait pas arrêté ?

## Comment mesurer le résultat

| Indicateur | Expérience 1 (graphe explicite) | Expérience 2 (parallélisme) | Expérience 3 (collaboration homme-machine) |
|------|--------------------------------|-----------------------------|--------------------------------------------|
| Visibilité de la structure | Combien d'arêtes implicites avez-vous trouvées ? | L'état partagé peut-il soutenir des sous-tâches parallèles ? | L'arête de retour arrière peut-elle localiser précisément la couche du problème ? |
| Localisation de l'échec | En cas d'échec, pouvez-vous pointer directement quelle arête est fausse ? | Quand une sous-tâche parallèle échoue, pouvez-vous localiser laquelle ? | Quand l'approbation est rejetée, pouvez-vous désigner à quelle couche est le problème ? |
| Coût de collaboration | Combien de temps avez-vous passé à dessiner ? | Temps gagné par le parallélisme vs. coût de coordination | Temps d'attente de l'approbation vs. valeur du problème arrêté |
| Observabilité | Ce qui se passe à chaque étape, est-ce maintenant visible ? | L'état de chaque sous-tâche parallèle est-il visible ? | La demande d'approbation est-elle écrite assez clairement ? |
| Fiabilité | La description du graphe correspond-elle à l'exécution réelle ? | Le critère de fusion fan-in est-il fiable ? | Les règles de timeout/escalade se déclenchent-elles vraiment ? |

## Ce qu'il faut livrer

- `graph.md` (la description complète du graphe de l'expérience 1 : graphe mermaid + tableau des nœuds + tableau des arêtes + champs de l'état partagé + règles de routage)
- La liste des arêtes implicites trouvées à l'expérience 1 (au moins une)
- Les règles de fan-out/fan-in de l'expérience 2 et l'enregistrement d'une exécution parallèle (comparaison temps/coût/qualité)
- Les règles d'arête de retour arrière, le format du nœud d'approbation et les 2 cycles de collaboration homme-machine de l'expérience 3
- La rétrospective finale : en passant du loop au graphe, qu'est-ce qui a changé dans votre façon de travailler ? Quelles tâches méritent d'être dessinées en graphe, lesquelles non ?

## Cours associés

- [Lecture 14 — Des boucles simples à l'ingénierie des graphes](../../lectures/lecture-14-graph-engineering/index.md)
- [Lecture 13 — Du prompting manuel aux boucles autonomes](../../lectures/lecture-13-loop-engineering/index.md) (votre loop est un nœud du graphe ; ce projet déplie la structure interne du nœud)
- [Lecture 09 — Pourquoi les agents déclarent victoire trop tôt](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (pourquoi le nœud de vérification doit être indépendant du nœud d'implémentation ; dans un graphe, c'est un problème de structure)
- [Lecture 11 — Pourquoi l'observabilité appartient au harness](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (plus le graphe est complexe, plus il faut voir ce que fait chaque nœud)