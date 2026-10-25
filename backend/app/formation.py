"""Programme de formation et règles de déblocage des cours."""

SEUIL_REUSSITE = 5


def _q(question, options, reponse):
    return {"question": question, "options": options, "reponse": reponse}


NIVEAUX = [
    {
        "id": "debutant",
        "nom": "Débutant",
        "description": "Comprendre les marchés, les cours et les premiers ordres.",
        "cours": [
            {
                "id": "debutant-1",
                "titre": "Découvrir les marchés financiers",
                "resume": "Les marchés, les actifs et les risques de base.",
                "sections": [
                    {"titre": "À quoi sert un marché ?", "texte": "Un marché met en relation des acheteurs et des vendeurs. Le prix observé évolue lorsque leurs intentions et les quantités disponibles changent."},
                    {"titre": "Les grandes familles d’actifs", "texte": "Une action représente une part d’entreprise ; une obligation est une créance ; une matière première est une ressource négociée ; une cryptomonnaie s’échange sur un réseau numérique. Chaque actif a ses propres horaires, risques et unités."},
                    {"titre": "Rendement et risque", "texte": "Un rendement potentiel plus élevé s’accompagne souvent de variations plus importantes. Le capital n’est jamais garanti : n’investissez pas de l’argent dont vous avez besoin à court terme."},
                ],
                "quiz": [
                    _q("Quel est le rôle principal d’un marché financier ?", ["Mettre en relation acheteurs et vendeurs", "Garantir un profit", "Fixer tous les prix pour toujours", "Supprimer le risque"], 0),
                    _q("Qu’est-ce qu’une action ?", ["Une part d’une entreprise", "Un prêt à une banque", "Une matière première", "Une monnaie garantie"], 0),
                    _q("Un rendement élevé signifie-t-il un risque nul ?", ["Oui", "Non, le risque peut aussi être élevé", "Oui, si l’actif est coté", "Seulement pour les cryptos"], 1),
                    _q("Une obligation est principalement…", ["Une créance", "Une part de pétrole", "Un ordre de vente", "Un indicateur graphique"], 0),
                    _q("Avant d’investir, il faut notamment comprendre…", ["Les risques et l’horizon de placement", "Seulement le dernier prix", "La couleur du graphique", "Le nom du courtier uniquement"], 0),
                ],
            },
            {
                "id": "debutant-2",
                "titre": "Lire un cours et un graphique",
                "resume": "Prix, variation, chandeliers et volume.",
                "sections": [
                    {"titre": "Cours et variation", "texte": "Le cours est le prix d’une transaction ou la dernière valeur disponible. La variation compare ce prix à une période de référence. Une variation positive passée ne garantit pas une hausse future."},
                    {"titre": "Lire une bougie", "texte": "Une bougie représente une période : ouverture, plus haut, plus bas et clôture. Le corps relie ouverture et clôture ; les mèches montrent les extrêmes atteints."},
                    {"titre": "Le volume", "texte": "Le volume mesure les unités échangées pendant une période. Il aide à décrire l’activité, mais ne prédit pas à lui seul la direction du prochain mouvement."},
                ],
                "quiz": [
                    _q("Quels sont les quatre prix d’une bougie ?", ["Ouverture, plus haut, plus bas, clôture", "Achat, vente, profit, perte", "Hier, aujourd’hui, demain, moyenne", "Volume, risque, cash, marge"], 0),
                    _q("Que montrent les mèches d’une bougie ?", ["Les extrêmes de la période", "Le bénéfice garanti", "Le volume annuel", "La date de règlement"], 0),
                    _q("Le volume décrit surtout…", ["L’activité échangée", "La prochaine hausse certaine", "Le prix minimum futur", "Le risque nul"], 0),
                    _q("Une variation passée garantit-elle la même variation demain ?", ["Oui", "Non", "Oui, pour les matières premières", "Seulement si elle est positive"], 1),
                    _q("La clôture correspond généralement…", ["Au dernier prix de la période", "Au plus haut obligatoire", "Au volume échangé", "Au prix de demain"], 0),
                ],
            },
            {
                "id": "debutant-3",
                "titre": "Passer son premier ordre",
                "resume": "Différencier achat, vente, quantité et liquidités.",
                "sections": [
                    {"titre": "Acheter et vendre", "texte": "Un achat augmente une position et utilise des liquidités. Une vente réduit une position existante et restitue des liquidités selon le prix d’exécution."},
                    {"titre": "Quantité et montant", "texte": "Le montant approximatif d’un ordre est le prix multiplié par la quantité. Vérifiez l’unité de cotation : un contrat, une once et une unité de crypto ne représentent pas la même exposition."},
                    {"titre": "Simulation sans risque réel", "texte": "Dans ce simulateur, les ordres sont virtuels. Ils servent à apprendre le fonctionnement d’un portefeuille, sans être envoyés à un courtier."},
                ],
                "quiz": [
                    _q("Que fait un ordre d’achat ?", ["Il augmente une position et débite le cash", "Il garantit une hausse", "Il supprime une position sans coût", "Il télécharge un cours"], 0),
                    _q("Comment estime-t-on le montant d’un ordre simple ?", ["Prix × quantité", "Prix + date", "Volume ÷ symbole", "Cash × rendement"], 0),
                    _q("Peut-on vendre davantage que sa position dans le simulateur ?", ["Oui toujours", "Non, la vente à découvert est refusée", "Seulement le week-end", "Seulement les cryptos"], 1),
                    _q("Les ordres de la plateforme sont-ils envoyés à un courtier ?", ["Oui", "Non, ils sont simulés", "Uniquement la nuit", "Seulement après un gain"], 1),
                    _q("Avant de confirmer un ordre, vérifiez…", ["Le symbole, le sens, la quantité et le prix", "La météo seulement", "Le nom de la page", "Uniquement la couleur"], 0),
                ],
            },
        ],
        "quiz": [
            _q("Un marché met principalement en relation…", ["Acheteurs et vendeurs", "Uniquement les banques centrales", "Des graphiques et des calendriers", "Des ordres garantis"], 0),
            _q("Une bougie montre…", ["Ouverture, plus haut, plus bas et clôture", "Uniquement le rendement annuel", "Le nombre de comptes", "Le cash disponible"], 0),
            _q("Le volume mesure…", ["Les unités échangées", "Le profit futur", "Le risque maximal garanti", "Le prix d’ouverture"], 0),
            _q("Acheter un actif…", ["Augmente la position et utilise du cash", "Garantit un gain", "Diminue toujours le risque", "N’a aucun coût"], 0),
            _q("Un rendement passé garantit-il un rendement futur ?", ["Oui", "Non", "Uniquement si positif", "Uniquement en simulation"], 1),
        ],
    },
    {
        "id": "intermediaire",
        "nom": "Intermédiaire",
        "description": "Mesurer les performances et construire une méthode disciplinée.",
        "cours": [
            {
                "id": "intermediaire-1",
                "titre": "Calculer rendement et performance",
                "resume": "Rendement simple, périodes et comparaison.",
                "sections": [
                    {"titre": "Rendement simple", "texte": "Le rendement simple entre deux dates est (prix final / prix initial − 1) × 100. Il peut être positif ou négatif et dépend de la période choisie."},
                    {"titre": "Comparer correctement", "texte": "Comparez des actifs sur des périodes identiques et avec des hypothèses cohérentes. Les dividendes, frais, devise et inflation peuvent modifier une comparaison."},
                    {"titre": "Historique et prudence", "texte": "Les données historiques décrivent le passé. Une performance observée n’est pas une promesse ; un échantillon court peut donner une image trompeuse."},
                ],
                "quiz": [
                    _q("Quelle formule donne le rendement simple ?", ["(final / initial − 1) × 100", "final + initial", "initial / volume", "final − date"], 0),
                    _q("Pour comparer deux actifs, il est préférable d’utiliser…", ["La même période et des hypothèses cohérentes", "Des périodes choisies pour chaque actif", "Uniquement leur prix nominal", "Leur symbole"], 0),
                    _q("Un rendement historique élevé garantit-il la suite ?", ["Oui", "Non", "Oui si calculé en pourcentage", "Oui pour un actif liquide"], 1),
                    _q("Un rendement de −10 % signifie que…", ["La valeur a baissé de 10 % sur la période", "La valeur est nulle", "Le volume a diminué de 10 %", "Le gain est garanti"], 0),
                    _q("Les frais peuvent-ils changer la performance nette ?", ["Oui", "Non", "Seulement pour les obligations", "Seulement si le rendement est négatif"], 0),
                ],
            },
            {
                "id": "intermediaire-2",
                "titre": "Tendance, supports et moyennes mobiles",
                "resume": "Outils descriptifs, limites et confirmation.",
                "sections": [
                    {"titre": "Tendance", "texte": "Une tendance résume la direction dominante observée sur une période. Une tendance haussière peut connaître des replis ; elle n’élimine ni les retournements ni les faux signaux."},
                    {"titre": "Moyenne mobile", "texte": "Une moyenne mobile lisse les cours passés sur un nombre défini de séances. Elle réagit avec retard et dépend de la fenêtre choisie."},
                    {"titre": "Supports et résistances", "texte": "Ces zones désignent des niveaux où le prix a souvent réagi dans l’historique. Ce ne sont pas des barrières certaines : une cassure peut survenir."},
                ],
                "quiz": [
                    _q("Une moyenne mobile est calculée à partir…", ["Des cours passés sur une fenêtre", "Des prix futurs connus", "Du mot de passe", "Des ordres non exécutés uniquement"], 0),
                    _q("Une moyenne mobile réagit généralement…", ["Avec retard", "Avant le marché", "Sans données historiques", "Avec certitude"], 0),
                    _q("Un support est…", ["Une zone de réaction historique possible", "Une garantie de prix plancher", "Un ordre d’achat automatique", "Un coupon obligataire"], 0),
                    _q("Une tendance haussière exclut-elle les replis ?", ["Oui", "Non", "Uniquement en crypto", "Uniquement sur une séance"], 1),
                    _q("Les supports et résistances doivent être considérés comme…", ["Des repères incertains", "Des garanties", "Des prix officiels futurs", "Des volumes"], 0),
                ],
            },
            {
                "id": "intermediaire-3",
                "titre": "Diversifier et gérer une position",
                "resume": "Exposition, diversification et risque de concentration.",
                "sections": [
                    {"titre": "Diversification", "texte": "Répartir une exposition entre plusieurs actifs peut réduire le risque spécifique, mais n’empêche pas les pertes. Des actifs différents peuvent chuter ensemble en période de crise."},
                    {"titre": "Taille d’une position", "texte": "La taille d’une position détermine son poids dans le portefeuille. Une forte concentration amplifie l’effet d’un mouvement défavorable sur le patrimoine."},
                    {"titre": "Suivi", "texte": "Surveillez l’exposition totale, les liquidités et les hypothèses de votre stratégie. Modifier un plan sous le coup de l’émotion peut accroître les coûts et les erreurs."},
                ],
                "quiz": [
                    _q("La diversification…", ["Peut réduire le risque spécifique sans supprimer toutes les pertes", "Garantit un profit", "Élimine les crises", "Remplace le suivi"], 0),
                    _q("Une position concentrée…", ["Amplifie l’effet d’un mouvement sur le portefeuille", "Garantit une meilleure performance", "Réduit toujours le risque", "N’a pas d’impact"], 0),
                    _q("Des actifs différents peuvent-ils baisser ensemble ?", ["Oui", "Non", "Jamais en crise", "Seulement si leur prix est égal"], 0),
                    _q("La taille d’une position aide à mesurer…", ["L’exposition du portefeuille", "Le nom de la bourse", "La date d’achat uniquement", "Le niveau de formation"], 0),
                    _q("La diversification doit-elle être accompagnée d’un suivi ?", ["Oui", "Non", "Seulement en simulation", "Seulement après un gain"], 0),
                ],
            },
        ],
        "quiz": [
            _q("Le rendement simple compare…", ["Prix final au prix initial", "Volume au symbole", "Date à la quantité", "Cash au mot de passe"], 0),
            _q("Une moyenne mobile utilise…", ["Les cours passés", "Les cours futurs", "Un prix garanti", "La quantité d’ordres"], 0),
            _q("Un support historique est-il garanti ?", ["Oui", "Non", "Oui en tendance haussière", "Oui pour le cuivre"], 1),
            _q("La diversification peut-elle empêcher toute perte ?", ["Oui", "Non", "Oui si quatre actifs", "Oui si les actifs sont différents"], 1),
            _q("Une position très concentrée…", ["Augmente l’impact d’un mouvement défavorable", "Supprime la volatilité", "Garantit un profit", "N’affecte pas le portefeuille"], 0),
        ],
    },
    {
        "id": "avance",
        "nom": "Avancé",
        "description": "Comprendre volatilité, risque et évaluation d’une stratégie.",
        "cours": [
            {
                "id": "avance-1",
                "titre": "Volatilité et risque de marché",
                "resume": "Variabilité des rendements et interprétation.",
                "sections": [
                    {"titre": "Mesurer la volatilité", "texte": "La volatilité résume la dispersion des rendements autour de leur moyenne sur une période. Elle ne donne pas le sens du prochain mouvement et ne décrit pas tous les risques."},
                    {"titre": "Fenêtre d’observation", "texte": "Une estimation sur cinq séances peut différer d’une estimation sur soixante séances. Plus la période est courte, plus l’indicateur peut réagir aux mouvements récents."},
                    {"titre": "Limites", "texte": "La volatilité historique peut sous-estimer un événement rare. Le risque de liquidité, de contrepartie, de modèle et les pertes extrêmes nécessitent d’autres analyses."},
                ],
                "quiz": [
                    _q("La volatilité mesure principalement…", ["La dispersion des rendements", "Le sens certain du prochain cours", "Le cash du compte", "Le nombre d’investisseurs"], 0),
                    _q("Une volatilité élevée prédit-elle le sens du mouvement ?", ["Oui", "Non", "Toujours à la baisse", "Toujours à la hausse"], 1),
                    _q("Une fenêtre de 5 jours et de 60 jours donnent-elles nécessairement la même estimation ?", ["Oui", "Non", "Seulement sur l’or", "Seulement si le volume est nul"], 1),
                    _q("La volatilité historique couvre-t-elle tous les risques ?", ["Oui", "Non", "Oui en période calme", "Oui pour les actions"], 1),
                    _q("Un risque de liquidité est lié…", ["À la difficulté de négocier rapidement sans impact important", "À la moyenne mobile", "À la date de création du compte", "Au thème de l’interface"], 0),
                ],
            },
            {
                "id": "avance-2",
                "titre": "Ordres, liquidité et glissement",
                "resume": "Spread, exécution et impact du marché.",
                "sections": [
                    {"titre": "Fourchette achat-vente", "texte": "Le spread est l’écart entre le meilleur prix acheteur et vendeur. Il représente un coût implicite, souvent plus élevé lorsque la liquidité est faible."},
                    {"titre": "Glissement", "texte": "Le prix obtenu peut différer du prix attendu lorsque le marché bouge ou que l’ordre est important par rapport aux échanges disponibles."},
                    {"titre": "Limites du simulateur", "texte": "Un backtest ou une simulation sans spread, frais ni glissement peut surestimer la performance. Documentez les hypothèses d’exécution."},
                ],
                "quiz": [
                    _q("Le spread est…", ["L’écart entre prix acheteur et vendeur", "La volatilité annuelle", "Le bénéfice net", "La taille du compte"], 0),
                    _q("Le glissement désigne…", ["L’écart entre prix attendu et prix obtenu", "Une hausse garantie", "Une erreur de calendrier", "Une action gratuite"], 0),
                    _q("Un marché peu liquide peut présenter…", ["Un spread et un impact plus élevés", "Un prix toujours garanti", "Aucun risque d’exécution", "Un rendement certain"], 0),
                    _q("Ignorer les coûts d’exécution peut…", ["Surestimer une performance simulée", "Améliorer le calcul réel", "Supprimer le risque", "Garantir un meilleur prix"], 0),
                    _q("Une hypothèse de backtest doit être…", ["Documentée", "Cachée", "Toujours optimiste", "Remplacée par le résultat"], 0),
                ],
            },
            {
                "id": "avance-3",
                "titre": "Tester une stratégie sans biais",
                "resume": "Données de test, surajustement et biais temporels.",
                "sections": [
                    {"titre": "Séparer les périodes", "texte": "Réservez une période de test distincte de la période utilisée pour concevoir ou ajuster une stratégie. Un résultat sur les données d’entraînement n’est pas une validation indépendante."},
                    {"titre": "Surajustement", "texte": "Une stratégie trop adaptée au passé peut capturer du bruit. Plus on essaie de variantes, plus il faut se méfier des meilleurs résultats obtenus par hasard."},
                    {"titre": "Données du futur", "texte": "À chaque décision, seuls les renseignements réellement disponibles à cette date doivent être utilisés. Toute fuite d’information future invalide l’évaluation."},
                ],
                "quiz": [
                    _q("Pourquoi garder une période de test indépendante ?", ["Pour estimer la généralisation hors entraînement", "Pour augmenter artificiellement le score", "Pour supprimer les frais", "Pour choisir le meilleur passé"], 0),
                    _q("Le surajustement signifie qu’une stratégie…", ["S’adapte trop aux particularités passées", "Est forcément robuste", "N’utilise pas de données", "Est toujours rentable"], 0),
                    _q("Utiliser une donnée future dans une décision historique provoque…", ["Une fuite d’information", "Une diversification", "Un spread", "Une clôture"], 0),
                    _q("Multiplier les essais de stratégie augmente le risque…", ["De retenir un résultat chanceux", "De supprimer le bruit", "De garantir un gain", "De réduire les coûts"], 0),
                    _q("Un bon résultat d’entraînement suffit-il à valider une stratégie ?", ["Oui", "Non", "Oui si le graphique est lisse", "Oui si la période est courte"], 1),
                ],
            },
        ],
        "quiz": [
            _q("La volatilité résume…", ["La dispersion des rendements", "Le sens certain du marché", "Le cash disponible", "Le spread uniquement"], 0),
            _q("Le spread correspond à…", ["L’écart entre prix acheteur et vendeur", "Une performance annuelle", "Un test statistique", "Une position ouverte"], 0),
            _q("Le glissement compare…", ["Le prix attendu et obtenu", "Le volume et le rendement", "Deux niveaux de cours", "Le capital et le dividende"], 0),
            _q("Un test indépendant sert à…", ["Évaluer une stratégie hors données d’ajustement", "Améliorer l’entraînement", "Éviter tous les risques", "Garantir le futur"], 0),
            _q("Une fuite d’information future rend-elle le test fiable ?", ["Oui", "Non", "Oui si le score est bas", "Oui sur crypto seulement"], 1),
        ],
    },
    {
        "id": "expert",
        "nom": "Expert",
        "description": "Élaborer un cadre robuste, contrôlé et documenté.",
        "cours": [
            {
                "id": "expert-1",
                "titre": "Risque de portefeuille et corrélations",
                "resume": "Exposition agrégée, dépendances et scénarios.",
                "sections": [
                    {"titre": "Risque agrégé", "texte": "Le risque du portefeuille dépend de la taille des positions, de la volatilité et des co-mouvements entre actifs. Additionner les risques individuels sans tenir compte des dépendances peut être trompeur."},
                    {"titre": "Corrélation", "texte": "La corrélation historique décrit une relation linéaire sur un échantillon donné. Elle peut changer et ne mesure pas toute dépendance, surtout pendant les crises."},
                    {"titre": "Scénarios", "texte": "Les scénarios de choc complètent les mesures statistiques : hausse brutale des taux, baisse des actifs risqués, rupture de liquidité ou variation de change."},
                ],
                "quiz": [
                    _q("Le risque d’un portefeuille dépend notamment…", ["Des tailles de positions et de leurs co-mouvements", "Uniquement du nombre de lignes", "Du thème de l’application", "Uniquement du rendement moyen"], 0),
                    _q("La corrélation historique est-elle stable et garantie ?", ["Oui", "Non", "Oui pendant une crise", "Oui si positive"], 1),
                    _q("Une corrélation faible garantit-elle une protection en crise ?", ["Oui", "Non", "Toujours pour deux actifs", "Oui à court terme"], 1),
                    _q("Les scénarios de choc servent à…", ["Explorer les conséquences d’événements défavorables", "Prédire exactement les dates de crise", "Garantir le capital", "Calculer les frais uniquement"], 0),
                    _q("Les risques individuels peuvent-ils être simplement additionnés sans examiner les dépendances ?", ["Oui", "Non", "Toujours si les actifs sont différents", "Oui pour les cryptos"], 1),
                ],
            },
            {
                "id": "expert-2",
                "titre": "Stress tests et scénarios extrêmes",
                "resume": "Scénarios historiques, hypothétiques et limites.",
                "sections": [
                    {"titre": "Scénarios historiques", "texte": "Un scénario historique rejoue des mouvements observés, appliqués aux expositions actuelles. Il permet d’étudier une situation passée, pas de prévoir qu’elle se reproduira."},
                    {"titre": "Scénarios hypothétiques", "texte": "Un scénario hypothétique combine des chocs plausibles, même s’ils n’ont pas été observés simultanément. Les hypothèses doivent être explicites et discutées."},
                    {"titre": "Utiliser les résultats", "texte": "Un stress test n’est ni une probabilité ni une perte maximale garantie. Il sert à révéler des vulnérabilités et à préparer des décisions de gestion."},
                ],
                "quiz": [
                    _q("Un scénario historique indique-t-il que le choc se répétera ?", ["Oui", "Non", "Oui si récent", "Oui si le marché est liquide"], 1),
                    _q("Un scénario hypothétique permet de…", ["Tester des chocs plausibles combinés", "Garantir une perte maximale", "Supprimer les hypothèses", "Calculer le prix futur exact"], 0),
                    _q("Un stress test est…", ["Un outil d’exploration de vulnérabilités", "Une prévision certaine", "Une garantie de capital", "Une probabilité exacte"], 0),
                    _q("Les hypothèses de scénario doivent-elles être explicites ?", ["Oui", "Non", "Uniquement si le résultat est négatif", "Seulement en simulation"], 0),
                    _q("Une perte sous scénario est-elle une perte maximale garantie ?", ["Oui", "Non", "Oui si historique", "Oui si le portefeuille est diversifié"], 1),
                ],
            },
            {
                "id": "expert-3",
                "titre": "Gouvernance et contrôle d’une stratégie",
                "resume": "Documentation, suivi, limites et revue indépendante.",
                "sections": [
                    {"titre": "Documenter", "texte": "Décrivez l’objectif, les données, les règles d’entrée et de sortie, les coûts, les limites et les cas d’échec connus. Une stratégie doit être compréhensible et reproductible."},
                    {"titre": "Contrôler dans le temps", "texte": "Comparez régulièrement les résultats réels et attendus, surveillez les changements de marché et définissez des seuils d’arrêt ou de revue avant qu’une crise survienne."},
                    {"titre": "Revue indépendante", "texte": "Une validation indépendante aide à repérer les erreurs, les biais et les conflits d’intérêts. Les décisions doivent rester traçables et proportionnées au risque."},
                ],
                "quiz": [
                    _q("Une documentation de stratégie devrait inclure…", ["Règles, données, coûts et limites", "Uniquement son meilleur rendement", "Seulement son nom", "Aucun cas d’échec"], 0),
                    _q("Un seuil de revue ou d’arrêt devrait être…", ["Défini à l’avance", "Inventé après une perte", "Toujours absent", "Basé sur la couleur du graphique"], 0),
                    _q("Une validation indépendante aide à détecter…", ["Erreurs et biais", "Les prix futurs certains", "Toutes les crises à venir", "Un rendement garanti"], 0),
                    _q("Les résultats doivent-ils être traçables ?", ["Oui", "Non", "Seulement si rentables", "Seulement pour l’or"], 0),
                    _q("Une stratégie robuste est-elle automatiquement sans risque ?", ["Oui", "Non", "Oui si testée", "Oui si documentée"], 1),
                ],
            },
        ],
        "quiz": [
            _q("Le risque agrégé dépend notamment…", ["Des expositions et de leurs dépendances", "Uniquement du nombre d’actifs", "Du nom du portefeuille", "De la date de création"], 0),
            _q("Une corrélation historique peut-elle changer ?", ["Oui", "Non", "Jamais en crise", "Seulement si négative"], 0),
            _q("Un stress test est-il une prévision certaine ?", ["Oui", "Non", "Oui s’il est historique", "Oui s’il est sévère"], 1),
            _q("Les hypothèses de stratégie doivent-elles être documentées ?", ["Oui", "Non", "Seulement le rendement", "Seulement après validation"], 0),
            _q("Une revue indépendante peut-elle aider à trouver des biais ?", ["Oui", "Non", "Seulement en marché haussier", "Uniquement en simulation"], 0),
        ],
    },
]

COMPLEMENTS_COURS = {
    "debutant-1": {
        "objectifs": [
            "Distinguer un actif financier d’un marché où il s’échange.",
            "Expliquer pourquoi un prix évolue lorsque l’offre et la demande changent.",
            "Associer le rendement potentiel au risque et à l’horizon de placement.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : pourquoi un prix bouge",
                "texte": "Imaginons qu’une matière première soit proposée à 100 dollars l’unité. Si beaucoup d’acheteurs souhaitent l’acquérir immédiatement et que peu de vendeurs sont prêts à céder leur stock, certains acheteurs acceptent d’offrir davantage. À l’inverse, si de nombreux détenteurs vendent en même temps, ils peuvent devoir accepter des offres plus basses. Le prix est donc le résultat de transactions et de négociations, pas une valeur immuable fixée par le graphique. Une nouvelle économique peut modifier les anticipations, mais elle ne permet pas de connaître avec certitude le prochain prix.",
            },
            {
                "titre": "Mise en pratique et points à retenir",
                "texte": "Dans le simulateur, comparez une matière première et une cryptomonnaie : notez leur symbole, leur unité, leurs horaires de cotation et les risques qui leur sont propres. Avant de prendre une décision, formulez trois questions : qu’est-ce qui pourrait faire baisser cet actif, combien de temps puis-je immobiliser cet argent, et quelle perte pourrais-je supporter ? Le mot « marché » ne signifie pas « profit ». Aucun actif n’est sûr dans toutes les situations et un compte de simulation sert à apprendre, pas à promettre un résultat réel.",
            },
        ],
        "reflexe": "Un trader sérieux commence par comprendre ce qu’il négocie et ce qu’il peut perdre. N’entrez jamais en position uniquement parce qu’un actif vient de monter.",
    },
    "debutant-2": {
        "objectifs": [
            "Lire les prix d’ouverture, de clôture, le plus haut et le plus bas.",
            "Interpréter le corps et les mèches d’un chandelier.",
            "Décrire ce que le volume indique et ce qu’il ne peut pas prédire.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : décomposer une bougie",
                "texte": "Supposons qu’un actif ouvre à 50, termine la séance à 54, touche 56 au plus haut et 48 au plus bas. Le corps va de 50 à 54, tandis que les mèches prolongent la bougie jusqu’à 48 et 56. La clôture est supérieure à l’ouverture : le prix a progressé pendant cette séance, mais il a aussi connu des mouvements dans les deux sens. Une seule bougie ne dit pas ce qui arrivera demain. Vérifiez également l’échelle du graphique et la durée représentée par chaque bougie : une bougie quotidienne et une bougie horaire ne racontent pas la même période.",
            },
            {
                "titre": "Lire sans tirer de conclusion hâtive",
                "texte": "Examinez plusieurs séances puis demandez-vous si l’activité et les prix évoluent ensemble. Un volume élevé signifie qu’un grand nombre d’unités a changé de mains selon la convention de la place de marché ; il ne prouve pas que les acheteurs ont gagné, car chaque transaction a aussi un vendeur. Les données peuvent être incomplètes ou calculées différemment selon les actifs. Dans vos notes, séparez les observations (« la clôture est supérieure à l’ouverture ») des interprétations (« la tendance va continuer »). Cette distinction évite de confondre description et prévision.",
            },
        ],
        "reflexe": "Décrivez le graphique avant de l’interpréter. Un signal n’est pas un ordre : exigez un scénario, un risque acceptable et un motif clair avant d’agir.",
    },
    "debutant-3": {
        "objectifs": [
            "Calculer le montant indicatif d’un ordre à partir du prix et de la quantité.",
            "Décrire l’effet d’un achat et d’une vente sur les liquidités.",
            "Vérifier le symbole et l’unité avant de confirmer un ordre simulé.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : prix, quantité et exposition",
                "texte": "À un prix simulé de 25 dollars, acheter 4 unités représente un montant indicatif de 100 dollars avant frais ou autres ajustements éventuels. Si le prix baisse ensuite à 20 dollars, ces unités valent 80 dollars : la variation est une perte latente de 20 dollars. Le calcul simplifié ne tient pas compte des frais, du spread, des règles propres à un contrat ou de la devise de référence. Pour les matières premières, une cotation peut correspondre à une unité spécifique ; vérifiez toujours ce que représente la quantité saisie.",
            },
            {
                "titre": "La vérification avant validation",
                "texte": "Avant de confirmer, relisez quatre éléments : l’actif choisi, le sens achat ou vente, la quantité et le prix affiché. Un achat doit rester compatible avec les liquidités disponibles. Une vente ne peut pas dépasser les unités détenues dans ce simulateur. Après l’opération, contrôlez les liquidités et les positions du portefeuille : c’est un moyen de repérer immédiatement une erreur de saisie. Tous les ordres de cette application sont fictifs ; ils ne sont jamais transmis à un intermédiaire financier.",
            },
        ],
        "reflexe": "Écrivez votre raison d’entrer et la condition qui invaliderait votre idée avant de cliquer. Si vous ne pouvez pas nommer ce risque, ne passez pas l’ordre.",
    },
    "intermediaire-1": {
        "objectifs": [
            "Appliquer la formule du rendement simple à deux prix.",
            "Interpréter le signe et l’horizon d’un rendement en pourcentage.",
            "Identifier les éléments qui rendent une comparaison injuste.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : interpréter un rendement",
                "texte": "Un actif passe de 80 à 100. Son rendement simple est (100 / 80 − 1) × 100, soit 25 %. S’il passe ensuite de 100 à 80, sa baisse est de 20 %, et non de 25 % : les pourcentages dépendent du prix de départ. Après une perte de 20 %, il faut une hausse de 25 % pour revenir de 80 à 100. Précisez toujours les dates et le prix de référence. Un pourcentage sans période ne permet pas de comparer deux performances de manière sérieuse.",
            },
            {
                "titre": "Comparer avec une méthode cohérente",
                "texte": "Pour comparer deux actifs, utilisez la même date de départ et la même date de fin, puis indiquez si les frais, les dividendes, les intérêts, la devise et l’inflation sont pris en compte. Une performance avant frais n’est pas une performance nette. L’ordre dans lequel les rendements arrivent compte aussi lorsque des retraits ou des dépôts sont effectués. Les prix passés constituent un historique, pas une distribution complète des futurs rendements possibles. Notez les hypothèses de calcul avant de tirer une conclusion.",
            },
        ],
        "reflexe": "Évaluez une méthode sur plusieurs périodes et après les coûts. Ne confondez pas un rendement spectaculaire sur une courte fenêtre avec une stratégie reproductible.",
    },
    "intermediaire-2": {
        "objectifs": [
            "Expliquer le retard d’une moyenne mobile.",
            "Distinguer observation d’une tendance et prévision certaine.",
            "Utiliser supports et résistances comme des zones incertaines.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : choisir une fenêtre",
                "texte": "Une moyenne mobile sur cinq séances accorde une place importante aux cours récents. Une moyenne sur soixante séances est plus lissée, mais réagit plus lentement à un changement récent. Si un cours chute brutalement, la moyenne courte se rapproche plus vite de ce cours ; la longue évolue plus progressivement. Ces indicateurs utilisent des observations déjà réalisées : ils ne devancent pas le marché. Changer la longueur de la fenêtre peut modifier le signal obtenu, donc il faut choisir cette fenêtre avant d’évaluer une stratégie, et non seulement après avoir vu le meilleur résultat.",
            },
            {
                "titre": "Des repères, pas des ordres automatiques",
                "texte": "Un support peut être une zone où le prix a rebondi à plusieurs reprises dans le passé, et une résistance une zone où des hausses ont rencontré des ventes. Il ne s’agit pas de lignes infranchissables : une annonce, un manque de liquidité ou un changement d’anticipations peut les traverser. Regardez la période du graphique, le nombre d’observations et les autres éléments disponibles. Décrivez ce que vous observez, indiquez votre scénario contraire et évitez de transformer un repère visuel en certitude.",
            },
        ],
        "reflexe": "Définissez à l’avance le signal qui confirme votre idée et celui qui la contredit. Ne déplacez pas vos règles après coup pour justifier une position perdante.",
    },
    "intermediaire-3": {
        "objectifs": [
            "Distinguer diversification et garantie de capital.",
            "Relier la taille d’une position à son poids dans le portefeuille.",
            "Repérer une concentration excessive et ses conséquences possibles.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : poids d’une position",
                "texte": "Un portefeuille de 10 000 euros comporte une position de 4 000 euros dans un seul actif : cette position représente 40 % de la valeur totale. Si cet actif baisse de 25 % et que les autres positions ne changent pas, la perte sur cette seule ligne est de 1 000 euros, soit 10 % du portefeuille initial. Le calcul est volontairement simple et ignore les corrélations, les frais et les mouvements des autres actifs. Il montre pourquoi le montant investi compte autant que l’opinion sur la direction du prix.",
            },
            {
                "titre": "Diversifier en comprenant les limites",
                "texte": "Détenir plusieurs actifs différents peut réduire l’impact d’un problème propre à l’un d’eux. Cela ne supprime ni les risques communs ni les pertes : en période de tension, plusieurs actifs peuvent chuter simultanément ou devenir difficiles à vendre. Vérifiez les expositions sous-jacentes, et pas uniquement le nombre de lignes. Établissez une limite de taille adaptée à votre situation et réexaminez-la à intervalles réguliers. La diversification est une façon de répartir le risque, pas une promesse de rendement.",
            },
        ],
        "reflexe": "Choisissez votre risque maximal par position avant d’entrer, puis calculez la quantité à partir de cette limite. N’augmentez pas la taille pour vous refaire après une perte.",
    },
    "avance-1": {
        "objectifs": [
            "Interpréter un écart-type de rendements sans le confondre avec une perte maximale.",
            "Comparer des mesures réalisées sur des fenêtres différentes.",
            "Compléter la volatilité par l’analyse d’autres risques.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : même moyenne, volatilité différente",
                "texte": "Deux placements peuvent afficher le même rendement moyen sur une période, alors que l’un évolue de façon régulière et l’autre alterne de fortes hausses et baisses. L’écart-type des rendements sera généralement plus élevé pour le second. La volatilité est calculée à partir d’un échantillon et d’une fréquence donnés : précisez si les rendements sont quotidiens, hebdomadaires ou mensuels et si la mesure est annualisée. Sans ces précisions, deux nombres de volatilité peuvent ne pas être comparables.",
            },
            {
                "titre": "Ce que la mesure ne dit pas",
                "texte": "Une volatilité historique résume les fluctuations observées, mais elle ne fixe pas la perte future maximale et n’indique pas le sens de la prochaine variation. Les événements rares, les ruptures de marché, les changements de corrélation et les problèmes de liquidité peuvent être mal représentés dans l’historique. Complétez la mesure par des scénarios défavorables, l’analyse de la baisse maximale, l’exposition et la capacité réelle à sortir d’une position. Toute estimation statistique comporte des hypothèses et une incertitude.",
            },
        ],
        "reflexe": "Réduisez votre exposition lorsque les variations deviennent difficiles à supporter. La volatilité sert à mesurer et adapter le risque, jamais à deviner seule le prochain mouvement.",
    },
    "avance-2": {
        "objectifs": [
            "Calculer le spread à partir des meilleurs prix vendeur et acheteur.",
            "Décrire les facteurs à l’origine du glissement à l’exécution.",
            "Intégrer les coûts de transaction à l’évaluation d’une stratégie.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : coût du spread",
                "texte": "Si le meilleur acheteur propose 99,90 et le meilleur vendeur demande 100,10, le spread est de 0,20. Un acheteur au marché paie en principe le côté vendeur disponible ; s’il revend immédiatement au meilleur prix acheteur sans changement de marché, il peut donc subir un écart lié au spread. Le spread peut varier avec l’heure, l’activité, la taille de l’ordre et la volatilité. Un prix de clôture historique ne garantit pas qu’un ordre de même taille aurait pu être exécuté à ce prix.",
            },
            {
                "titre": "Évaluer une exécution réaliste",
                "texte": "Un ordre important par rapport au volume disponible peut déplacer le prix obtenu : c’est une forme d’impact de marché. Le glissement peut aussi venir du délai entre la décision et l’exécution. Dans un test de stratégie, indiquez les frais, le spread, le type d’ordre, le retard de données et une hypothèse de glissement. Répétez éventuellement l’analyse avec des coûts plus sévères pour examiner la sensibilité. Une simulation qui suppose une exécution parfaite tend à produire des résultats optimistes.",
            },
        ],
        "reflexe": "Choisissez le type d’ordre en comprenant son compromis : un ordre au marché privilégie l’exécution, un ordre limite contrôle le prix mais peut ne pas être exécuté.",
    },
    "avance-3": {
        "objectifs": [
            "Séparer les données de conception, de validation et de test.",
            "Expliquer le surajustement et le biais de sélection.",
            "Éviter toute information qui n’était pas disponible au moment de la décision.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : chronologie sans fuite",
                "texte": "Pour tester une règle créée avec les données de 2018 à 2022, on peut réserver 2023 à 2024 pour une évaluation qui n’a pas servi à régler ses paramètres. À chaque date historique, les indicateurs ne doivent utiliser que les prix déjà connus à cette date. Utiliser par erreur la clôture du jour pour décider d’un ordre exécuté à l’ouverture du même jour introduit une information impossible à connaître au moment de l’ordre. Le calendrier des calculs et des transactions est donc aussi important que la formule.",
            },
            {
                "titre": "Se méfier du meilleur résultat",
                "texte": "Si l’on essaie des centaines de combinaisons, l’une d’elles peut sembler excellente simplement parce qu’elle correspond au bruit de l’échantillon. C’est le surajustement, renforcé par la sélection a posteriori des résultats les plus favorables. Gardez une période de test intacte, consignez le nombre d’essais, vérifiez la robustesse sur plusieurs périodes et incluez les coûts. Un résultat hors échantillon reste incertain ; une validation historique n’est pas une garantie de performance future.",
            },
        ],
        "reflexe": "Tenez un journal de stratégie : motif de l’entrée, plan, taille, sortie, frais et émotion ressentie. Analysez une série d’opérations, pas un seul gain ou une seule perte.",
    },
    "expert-1": {
        "objectifs": [
            "Relier poids des positions, volatilité et dépendances au risque global.",
            "Interpréter les corrélations comme des estimations instables.",
            "Compléter les indicateurs par une analyse de scénarios.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : la dépendance compte",
                "texte": "Un portefeuille composé de deux positions de même taille n’est pas nécessairement deux fois moins risqué qu’une position unique. Si les deux actifs sont fortement corrélés, ils peuvent baisser ensemble et offrir peu de compensation. Une approximation de la variance du portefeuille combine les poids, les volatilités et les covariances entre actifs. Le résultat dépend des estimations utilisées ; une matrice de corrélation construite sur une période calme peut décrire imparfaitement une crise. Examinez également la concentration par secteur, devise et facteur économique.",
            },
            {
                "titre": "Contrôler les dépendances",
                "texte": "Comparez plusieurs fenêtres d’estimation, repérez les observations manquantes et vérifiez que les séries sont alignées sur les mêmes dates. Les actifs ne négocient pas nécessairement aux mêmes heures ni selon les mêmes calendriers. Une corrélation linéaire ne résume pas les dépendances dans les queues de distribution : deux marchés peuvent être généralement indépendants et devenir simultanément vulnérables lors d’un choc. Présentez les limites de l’estimation et complétez-la par des stress tests, une analyse de liquidité et des scénarios de concentration.",
            },
        ],
        "reflexe": "Regardez l’exposition totale, pas seulement chaque position séparément. Plusieurs paris différents en apparence peuvent dépendre du même facteur de marché.",
    },
    "expert-2": {
        "objectifs": [
            "Différencier scénario historique, scénario hypothétique et prévision.",
            "Construire un scénario cohérent en précisant les hypothèses.",
            "Interpréter les pertes simulées comme des indicateurs de vulnérabilité.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : construire un choc",
                "texte": "Considérez un portefeuille exposé à des actions, des obligations et une devise. Un scénario hypothétique peut combiner une baisse de 20 % des actions, une hausse des taux et une dépréciation de la devise, même si ces mouvements exacts ne se sont pas produits ensemble dans l’échantillon. Définissez l’horizon, les chocs, le traitement des corrélations et les hypothèses d’exécution. Calculez ensuite l’impact par position et au niveau agrégé. Le résultat dépend entièrement du scénario choisi : ce n’est ni une prédiction ni une probabilité.",
            },
            {
                "titre": "Exploiter les résultats avec prudence",
                "texte": "Un stress test utile aide à identifier les positions qui contribuent le plus à une perte, les besoins de liquidité et les limites à surveiller. Testez plusieurs variantes, dont des chocs combinés, et expliquez les limites des données. Un scénario historique est compréhensible, mais l’avenir peut être plus sévère ou prendre une forme différente. Les résultats ne représentent pas une perte maximale garantie. Servez-vous-en pour discuter de mesures de réduction du risque, sans laisser un seul indicateur remplacer le jugement et la gouvernance.",
            },
        ],
        "reflexe": "Demandez-vous comment votre plan résiste à un scénario défavorable avant d’engager du capital. Si une perte simulée est inacceptable, ajustez l’exposition ou abstenez-vous.",
    },
    "expert-3": {
        "objectifs": [
            "Documenter une stratégie pour qu’un tiers puisse la reproduire.",
            "Définir à l’avance des limites et des critères de revue.",
            "Organiser un contrôle indépendant et une piste d’audit.",
        ],
        "sections": [
            {
                "titre": "Exemple guidé : fiche de stratégie",
                "texte": "Une fiche exploitable indique l’objectif, les instruments autorisés, la source et la période des données, les règles d’entrée et de sortie, la taille des positions, les coûts retenus et les cas où la stratégie ne doit pas fonctionner. Elle décrit aussi les tests effectués, leurs limites et les changements de paramètres. Un collègue doit pouvoir reconstruire les résultats à partir de cette documentation. Si une règle ne peut pas être expliquée ou répétée, le résultat correspondant est difficile à contrôler.",
            },
            {
                "titre": "Surveillance et décisions traçables",
                "texte": "Fixez avant le lancement des seuils qui déclenchent une revue, une réduction du risque ou une suspension. Surveillez les écarts entre comportement attendu et observé, les changements de données, la liquidité et les erreurs opérationnelles. Consignez la date, la donnée utilisée, la décision et son responsable. Une revue indépendante recherche les erreurs de calcul, les biais et les conflits d’intérêts ; elle ne certifie pas l’absence de perte future. La gouvernance doit évoluer lorsque l’instrument, le marché ou le modèle change.",
            },
        ],
        "reflexe": "Protégez votre discipline par des règles écrites : perte maximale, arrêt après une série d’erreurs, revue du journal et pause lorsque l’émotion prend le dessus.",
    },
}

QUESTIONS_COURS = {
    "debutant-1": [
        _q("Si davantage d’acheteurs souhaitent acheter alors que peu de vendeurs offrent l’actif, le prix peut…", ["Monter, sans certitude", "Être garanti", "Devenir nul", "Ne jamais varier"], 0),
        _q("Une matière première et une crypto peuvent avoir…", ["Des horaires et risques différents", "Le même contrat dans tous les cas", "Un prix obligatoirement fixe", "Le même niveau de risque"], 0),
        _q("Avant un placement, l’horizon aide à comprendre…", ["Quand l’argent peut être nécessaire", "Le prix exact de demain", "Le volume certain", "La prochaine crise"], 0),
        _q("Le prix affiché d’un actif est principalement…", ["Une observation de marché, pas une valeur immuable", "Une promesse de remboursement", "Une garantie de profit", "Une prévision certaine"], 0),
        _q("Un compte de simulation sert principalement à…", ["Apprendre avec des opérations fictives", "Obtenir un rendement réel", "Supprimer les pertes", "Envoyer un ordre à la banque"], 0),
    ],
    "debutant-2": [
        _q("Une bougie ouvre à 50 et clôture à 54 : son corps va de…", ["50 à 54", "48 à 56", "0 à 54", "50 au volume"], 0),
        _q("Une séance a touché 48 et 56 : ces valeurs sont…", ["Le plus bas et le plus haut", "L’ouverture et la clôture forcément", "Le spread et les frais", "Deux volumes"], 0),
        _q("Chaque transaction implique généralement…", ["Un acheteur et un vendeur", "Deux acheteurs sans vendeur", "Un profit garanti", "Un prix futur"], 0),
        _q("Avant de comparer deux graphiques, vérifiez…", ["Leur échelle et la durée des bougies", "Seulement leur couleur", "La taille de l’écran", "Le nombre de boutons"], 0),
        _q("Séparer l’observation de l’interprétation sert à…", ["Éviter de confondre constat et prévision", "Garantir une hausse", "Remplacer les données", "Augmenter le volume"], 0),
    ],
    "debutant-3": [
        _q("4 unités à 25 dollars représentent un montant indicatif de…", ["100 dollars", "29 dollars", "625 dollars", "4 dollars"], 0),
        _q("Si ces 4 unités passent de 25 à 20 dollars, leur valeur devient…", ["80 dollars", "100 dollars", "20 dollars", "125 dollars"], 0),
        _q("Un calcul prix × quantité peut omettre…", ["Les frais et le spread", "Le symbole", "La quantité", "Le prix de départ"], 0),
        _q("Avant de confirmer un ordre, il faut relire…", ["Actif, sens, quantité et prix", "Seulement le prix", "Uniquement le graphique", "Le nom d’utilisateur d’un autre compte"], 0),
        _q("Les ordres de la plateforme de simulation sont…", ["Fictifs, non transmis à un courtier", "Des ordres réels", "Des garanties de rendement", "Toujours exécutés par une banque"], 0),
    ],
    "intermediaire-1": [
        _q("Un prix passe de 80 à 100 : le rendement simple est…", ["25 %", "20 %", "−20 %", "80 %"], 0),
        _q("Un prix passe de 100 à 80 : son rendement simple est…", ["−20 %", "−25 %", "20 %", "25 %"], 0),
        _q("Après une baisse de 20 %, le prix doit remonter de…", ["25 % pour retrouver son niveau initial", "20 %", "10 %", "80 %"], 0),
        _q("Un rendement en pourcentage sans période est…", ["Insuffisant pour bien comparer", "Toujours annualisé", "Toujours net de frais", "Une prévision"], 0),
        _q("Une comparaison nette cohérente peut nécessiter de préciser…", ["Frais, dividendes et devise", "La couleur des lignes", "La taille du navigateur", "Le nom du compte"], 0),
    ],
    "intermediaire-2": [
        _q("Une moyenne mobile sur 5 jours réagit souvent…", ["Plus vite qu’une moyenne sur 60 jours", "Plus lentement dans tous les cas", "Avant le cours", "Sans historique"], 0),
        _q("La moyenne mobile est calculée à partir…", ["Des observations passées de sa fenêtre", "Des cours futurs", "Des profits garantis", "Du nombre de comptes"], 0),
        _q("Un support historique doit être vu comme…", ["Une zone d’observation possible", "Une ligne infranchissable", "Un prix garanti", "Un ordre exécuté"], 0),
        _q("Une cassure d’une résistance est…", ["Possible malgré les observations passées", "Impossible", "Une garantie de baisse", "Une erreur de calcul"], 0),
        _q("Choisir une fenêtre après avoir vu le meilleur résultat peut…", ["Favoriser une évaluation biaisée", "Garantir la robustesse", "Supprimer les frais", "Rendre les prix futurs connus"], 0),
    ],
    "intermediaire-3": [
        _q("4 000 euros dans un portefeuille de 10 000 euros représentent…", ["40 %", "4 %", "10 %", "400 %"], 0),
        _q("Une baisse de 25 % sur une position de 4 000 euros correspond à…", ["1 000 euros de baisse", "250 euros", "4 000 euros", "25 euros"], 0),
        _q("Détenir plusieurs actifs supprime-t-il les risques communs ?", ["Non", "Oui", "Toujours si quatre actifs", "Oui pendant une crise"], 0),
        _q("Le nombre de lignes suffit-il pour évaluer la diversification ?", ["Non, il faut aussi examiner les expositions", "Oui", "Uniquement en actions", "Seulement si les prix sont égaux"], 0),
        _q("La diversification est…", ["Une répartition du risque, pas une garantie", "Un profit assuré", "Une absence de suivi", "Une prédiction"], 0),
    ],
    "avance-1": [
        _q("La volatilité résume généralement…", ["La dispersion des rendements", "Le sens du prochain mouvement", "La perte maximale garantie", "Le nombre d’ordres"], 0),
        _q("Pour comparer deux volatilités, il faut vérifier…", ["Fréquence, fenêtre et annualisation", "Leur couleur", "Le nom des actifs uniquement", "Le solde bancaire"], 0),
        _q("Une volatilité élevée prouve-t-elle que le prix va baisser ?", ["Non", "Oui", "Toujours", "Seulement en crypto"], 0),
        _q("Un événement rare peut être…", ["Mal représenté dans la volatilité historique", "Toujours prévu par l’écart-type", "Sans effet sur le risque", "Un indicateur technique"], 0),
        _q("Une analyse complémentaire du risque peut inclure…", ["Liquidité et scénarios défavorables", "Uniquement la moyenne mobile", "La couleur du thème", "Le nom du portefeuille"], 0),
    ],
    "avance-2": [
        _q("Prix acheteur 99,90 et vendeur 100,10 : le spread est…", ["0,20", "200", "100,10", "99,90"], 0),
        _q("Un achat immédiat se fait généralement au…", ["Prix vendeur disponible", "Prix acheteur seulement", "Prix futur", "Prix moyen annuel garanti"], 0),
        _q("Un ordre important par rapport au volume disponible peut…", ["Déplacer le prix d’exécution", "Garantir le prix", "Supprimer le spread", "Réduire le volume historique"], 0),
        _q("Un test qui ignore les coûts d’exécution risque de…", ["Surestimer la performance", "Garantir une exécution parfaite", "Prédire les frais", "Réduire les transactions réelles"], 0),
        _q("Une analyse de sensibilité utile peut…", ["Tester des coûts de transaction plus sévères", "Supprimer les hypothèses", "Choisir le résultat le plus favorable seulement", "Éviter les dates"], 0),
    ],
    "avance-3": [
        _q("Une période de test indépendante ne doit pas servir à…", ["Régler les paramètres de la stratégie", "Mesurer une performance hors entraînement", "Vérifier une hypothèse", "Documenter les résultats"], 0),
        _q("Utiliser la clôture du jour pour décider d’un ordre placé avant cette clôture crée…", ["Une fuite d’information", "Une diversification", "Un spread nul", "Une validation indépendante"], 0),
        _q("Essayer de nombreuses variantes puis garder la meilleure augmente le risque de…", ["Sélectionner un résultat chanceux", "Supprimer le bruit", "Garantir l’avenir", "Réduire l’échantillon"], 0),
        _q("Le surajustement peut produire…", ["Un résultat passé qui se généralise mal", "Une garantie hors échantillon", "Une volatilité nulle", "Une absence de biais"], 0),
        _q("Même un bon résultat hors échantillon reste…", ["Incertain pour l’avenir", "Une garantie de profit", "Sans besoin de coûts", "Une information future"], 0),
    ],
    "expert-1": [
        _q("Deux positions fortement corrélées peuvent…", ["Baisser ensemble", "Toujours se compenser", "Supprimer le risque", "Garantir une diversification"], 0),
        _q("Le risque agrégé dépend notamment…", ["Des poids, volatilités et covariances", "Du nombre de boutons", "Du nom de l’actif uniquement", "Du thème choisi"], 0),
        _q("Une corrélation estimée en période calme décrit-elle nécessairement une crise ?", ["Non", "Oui", "Toujours", "Uniquement si positive"], 0),
        _q("Deux marchés qui négocient à des heures différentes peuvent nécessiter…", ["Un contrôle de l’alignement des dates", "Une suppression de l’historique", "Une garantie de covariance nulle", "Aucune vérification"], 0),
        _q("La corrélation linéaire résume-t-elle toutes les dépendances extrêmes ?", ["Non", "Oui", "Toujours", "Seulement pour deux actifs"], 0),
    ],
    "expert-2": [
        _q("Un scénario hypothétique peut combiner…", ["Des chocs plausibles non observés ensemble", "Des profits garantis", "Des données du futur", "Des prix certains"], 0),
        _q("Un stress test dépend directement…", ["Des hypothèses de scénario", "D’une probabilité certaine", "Du thème sombre", "De l’identifiant du compte"], 0),
        _q("Un scénario historique indique-t-il que le passé se répétera ?", ["Non", "Oui", "Toujours", "Si le portefeuille est diversifié"], 0),
        _q("Pour exploiter un test, il est utile d’identifier…", ["Les positions contributrices et besoins de liquidité", "Uniquement le meilleur résultat", "La couleur du graphique", "Un rendement garanti"], 0),
        _q("Un résultat de stress test représente-t-il nécessairement la perte maximale ?", ["Non", "Oui", "Toujours si sévère", "Seulement pour les actions"], 0),
    ],
    "expert-3": [
        _q("Une fiche de stratégie reproductible décrit…", ["Règles, données, coûts et limites", "Uniquement le meilleur rendement", "Le nom de la stratégie", "Aucun cas d’échec"], 0),
        _q("Une limite de revue devrait idéalement être définie…", ["Avant le lancement", "Après chaque résultat défavorable seulement", "Jamais", "Par le graphique seul"], 0),
        _q("Une piste d’audit consigne notamment…", ["Date, donnée, décision et responsable", "Uniquement le profit", "La couleur du tableau", "Les hypothèses cachées"], 0),
        _q("Une revue indépendante aide à repérer…", ["Erreurs, biais et conflits d’intérêts", "Le prix exact de demain", "Toutes les crises futures", "Un rendement assuré"], 0),
        _q("Une stratégie documentée est-elle sans risque ?", ["Non", "Oui", "Toujours", "Si elle a été testée"], 0),
    ],
}

QUESTIONS_NIVEAU = {
    "debutant": [
        _q("Une action représente…", ["Une part d’entreprise", "Une garantie de capital", "Une bougie", "Un spread"], 0),
        _q("Les mèches d’une bougie indiquent…", ["Les extrêmes atteints pendant la période", "Le profit futur", "Les frais", "Le cash"], 0),
        _q("Le rendement de 80 à 100 est…", ["25 %", "20 %", "80 %", "−20 %"], 0),
        _q("Le montant indicatif de 3 unités à 10 est…", ["30", "13", "7", "300"], 0),
        _q("Une hausse passée garantit-elle une hausse demain ?", ["Non", "Oui", "Toujours", "Uniquement sur le marché crypto"], 0),
    ],
    "intermediaire": [
        _q("Une moyenne mobile longue réagit généralement…", ["Plus lentement", "Avant le marché", "Sans données", "Avec certitude"], 0),
        _q("Une résistance historique est…", ["Une zone, pas une garantie", "Une barrière certaine", "Un prix futur fixé", "Un ordre exécuté"], 0),
        _q("Une baisse de 20 % demande ensuite quelle hausse pour revenir au départ ?", ["25 %", "20 %", "10 %", "80 %"], 0),
        _q("Des actifs différents peuvent-ils baisser ensemble ?", ["Oui", "Non", "Jamais", "Seulement si leur cours est identique"], 0),
        _q("La concentration augmente…", ["L’impact d’un mouvement sur une position importante", "La garantie de profit", "Le nombre de marchés", "La liquidité certaine"], 0),
    ],
    "avance": [
        _q("La volatilité est une mesure…", ["De dispersion", "Du sens certain du marché", "Du bénéfice", "Du spread uniquement"], 0),
        _q("Une période de test indépendante sert à…", ["Mesurer la stratégie hors ajustement", "Optimiser l’entraînement", "Supprimer les coûts", "Garantir le rendement"], 0),
        _q("Un écart entre meilleur acheteur et vendeur est…", ["Le spread", "Le surajustement", "La volatilité", "La corrélation"], 0),
        _q("Une fuite d’information future…", ["Rend l’évaluation historique invalide", "Améliore toujours la robustesse", "Réduit le risque", "Supprime le spread"], 0),
        _q("Des coûts d’exécution ignorés peuvent…", ["Surestimer les résultats", "Garantir le prix", "Supprimer le glissement", "Valider une stratégie"], 0),
    ],
    "expert": [
        _q("Le risque agrégé dépend notamment…", ["Des expositions et de leurs dépendances", "Uniquement du nombre de lignes", "Du nom de la stratégie", "Du thème de l’interface"], 0),
        _q("Une corrélation historique peut-elle changer en période de crise ?", ["Oui", "Non", "Jamais", "Seulement si elle est nulle"], 0),
        _q("Un stress test constitue-t-il une prévision certaine ?", ["Non", "Oui", "Toujours", "S’il est historique"], 0),
        _q("Une documentation utile devrait inclure…", ["Règles, données, coûts et limites", "Uniquement le rendement maximal", "Le nom du modèle seul", "Aucun cas d’échec"], 0),
        _q("Des scénarios hypothétiques servent notamment à…", ["Explorer des chocs plausibles", "Garantir une perte maximale", "Prédire le jour d’une crise", "Supprimer les incertitudes"], 0),
    ],
}

for niveau in NIVEAUX:
    niveau["quiz"].extend(QUESTIONS_NIVEAU[niveau["id"]])
    for cours in niveau["cours"]:
        complement = COMPLEMENTS_COURS[cours["id"]]
        cours["objectifs"] = complement["objectifs"]
        cours["sections"].extend(complement["sections"])
        cours["reflexe"] = complement["reflexe"]
        cours["quiz"].extend(QUESTIONS_COURS[cours["id"]])


def _varier_ordre_reponses(questions, decalage=0):
    for index, question in enumerate(questions):
        bonne = question["options"].pop(question["reponse"])
        position = (index * 3 + decalage) % (len(question["options"]) + 1)
        question["options"].insert(position, bonne)
        question["reponse"] = position


for index_niveau, niveau in enumerate(NIVEAUX):
    _varier_ordre_reponses(niveau["quiz"], index_niveau)
    for index_cours, cours in enumerate(niveau["cours"]):
        _varier_ordre_reponses(cours["quiz"], index_niveau + index_cours)


NIVEAUX_PAR_ID = {niveau["id"]: niveau for niveau in NIVEAUX}
COURS_PAR_ID = {
    cours["id"]: (niveau, cours)
    for niveau in NIVEAUX
    for cours in niveau["cours"]
}


def questions_publiques(questions):
    return [
        {"question": question["question"], "options": question["options"]}
        for question in questions
    ]


def corriger(questions, reponses):
    return [
        {
            "question": question["question"],
            "reponse_utilisateur": question["options"][reponse],
            "bonne_reponse": question["options"][question["reponse"]],
            "correcte": reponse == question["reponse"],
        }
        for question, reponse in zip(questions, reponses)
    ]


def noter(questions, reponses):
    if len(reponses) != len(questions):
        return None
    if any(type(reponse) is not int or not 0 <= reponse < len(question["options"])
           for question, reponse in zip(questions, reponses)):
        return None
    correctes = sum(
        reponse == question["reponse"]
        for question, reponse in zip(questions, reponses)
    )
    return round(correctes * 10 / len(questions))
