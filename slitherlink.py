##############################################################################
#                                                                            #
#                             Projet Slitherlink                             #
#                                                                            #
##############################################################################


import fltk
import os
import ast
import datetime
from doctest import testmod


def est_trace(etat, segment):
    """
    Renvoie True si le segment est tracé, False sinon

    :param etat: dict
    :param segment: tuple
    :return value: bool

    >>> est_trace({}, ((0, 0), (0, 1)))
    False
    >>> est_trace({((0, 0), (0, 1)): 1}, ((0, 0), (0, 1)))
    True
    """
    if segment in etat and etat[segment] == 1:
        return True
    return False


def est_interdit(etat, segment):
    """
    Renvoie True si le segment est interdit, False sinon

    :param etat: dict
    :param segment: tuple
    :return value: bool

    >>> est_interdit({}, ((0, 0), (0, 1)))
    False
    >>> est_interdit({((0, 0), (0, 1)): -1}, ((0, 0), (0, 1)))
    True
    """
    if segment in etat and etat[segment] == -1:
        return True
    return False


def est_vierge(etat, segment):
    """
    Renvoie True si le segment est vierge, False sinon

    :param etat: dict
    :param segment: tuple
    :return value: bool

    >>> est_vierge({}, ((0, 0), (0, 1)))
    True
    >>> est_vierge({((0, 0), (0, 1)): 1}, ((0, 0), (0, 1)))
    False
    """
    if segment not in etat:
        return True
    return False


def tracer_segment(etat, segment):
    """
    Trace segment dans etat

    :param etat: dict
    :param segment: tuple
    :return value: dict

    >>> tracer_segment({}, ((0, 0), (1, 0)))
    {((0, 0), (1, 0)): 1}
    """
    etat[segment] = 1
    return etat


def interdire_segment(etat, segment):
    """
    Interdit segment dans etat

    :param etat: dict
    :param segment: tuple
    :return value: dict

    >>> interdire_segment({}, ((0, 0), (1, 0)))
    {((0, 0), (1, 0)): -1}
    """
    etat[segment] = -1
    return etat


def effacer_segment(etat, segment):
    """
    Efface segment dans etat

    :param etat: dict
    :param segment: tuple
    :return value: dict

    >>> effacer_segment({((0, 0), (1, 0)): 1}, ((0, 0), (1, 0)))
    {}
    """
    etat.pop(segment)
    return etat


def tracer_segment_graphique(etat, segment, coord, epaisseur):
    """
    Trace un segment graphiquement et utilise tracer_segment pour le tracer
    dans etat

    :param etat: dict
    :param segment: tuple
    :param coord: list
    :param epaisseur: int
    :return value: dict
    """
    a, b, c, d = coord
    segment_str = codeTag(segment)
    if est_trace(etat, segment):
        etat = effacer_segment_graphique(etat, segment)
    elif est_interdit(etat, segment):
        etat = effacer_segment_graphique(etat, segment)
        fltk.efface(segment_str)
        etat = tracer_segment(etat, segment)
        fltk.ligne(b, a, d, c, epaisseur=epaisseur,
                   tag=segment_str)
    else:
        etat = tracer_segment(etat, segment)
        fltk.ligne(b, a, d, c, epaisseur=epaisseur,
                   tag=segment_str)
    return etat


def trace_croix(coord, epaisseur, segment_str):
    """
    Dessine une croix rouge utilisée pour interdire un segment

    :param coord: list
    :param epaisseur: int
    :param segment_str: str
    """
    a, b, c, d = coord
    fltk.ligne((b+d)/2-5, (a+c)/2-5, (b+d)/2+5, (a+c) /
               2+5, epaisseur=epaisseur/3, couleur='red', tag=segment_str)
    fltk.ligne((b+d)/2+5, (a+c)/2-5, (b+d)/2-5, (a+c) /
               2+5, epaisseur=epaisseur/3, couleur='red', tag=segment_str)


def codeTag(segment):
    """
    Code un tag exclusif à un segment en str, c'est utilisé pour supprimer un
    segment avec fltk.efface(tag)

    :param segment: tuple
    :return value: str

    >>> codeTag(((0, 0), (0, 1)))
    '@@@A'
    >>> codeTag(((1, 2), (2, 2)))
    'ABBB'
    """
    segment_str = ''
    for point in segment:
        for coord in point:
            segment_str += chr(ord('@')+(int(coord)))
    return segment_str


def interdire_segment_graphique(etat, segment, coord, epaisseur):
    """
    Interdit un segment graphiquement et utilise interdire_segment pour
    l'interdire dans etat

    :param etat: dict
    :param segment: tuple
    :param coord: list
    :param epaisseur: int
    :return value: dict
    """
    segment_str = codeTag(segment)
    if est_interdit(etat, segment):
        etat = effacer_segment_graphique(etat, segment)
        fltk.efface(segment_str)
    elif est_trace(etat, segment):
        etat = effacer_segment_graphique(etat, segment)
        fltk.efface(segment_str)
        etat = interdire_segment(etat, segment)
        trace_croix(coord, epaisseur, segment_str)
    else:
        etat = interdire_segment(etat, segment)
        trace_croix(coord, epaisseur, segment_str)
    return etat


def effacer_segment_graphique(etat, segment):
    """
    Efface un segment graphiquement et utilise effacer_segment pour
    l'effacer dans etat

    :param etat: dict
    :param segment: tuple
    :return value: dict
    """
    segment_str = codeTag(segment)
    etat = effacer_segment(etat, segment)
    fltk.efface(segment_str)
    return etat


def segments_traces(etat, sommet):
    """
    Renvoie la liste des segments tracés autour d'un sommet

    :param etat: dict
    :param sommet: tuple
    :return value: list

    >>> segments_traces({((2, 2), (3, 2)): 1, ((2, 2), (2, 3)): 1}, (2, 2))
    [((2, 2), (3, 2)), ((2, 2), (2, 3))]
    """
    liste_segments = []
    for segment in etat:
        if sommet in segment and etat[segment] == 1:
            liste_segments.append(segment)
    return liste_segments


def statut_case(indices, etat, case):
    """
    Retourne le statut de la case passée en paramètre. 0 si l'indice est
    satisfait, -1 et 1 si il ne l'est pas, pas assez ou trop de segments
    autour

    :param indices: list
    :param etat: dict
    :param case: tuple

    >>> indices = [[None, 3, 1]]
    >>> etat = {((0, 1), (0, 2)): 1, ((0, 2), (0, 3)): 1, ((0, 3), (1, 3)): 1}
    >>> statut_case(indices, etat, (0, 1))
    -1
    >>> statut_case(indices, etat, (0, 2))
    1
    >>> etat = {((0, 1), (0, 2)): 1, ((0, 2), (0, 3)): 1}
    >>> statut_case(indices, etat, (0, 2))
    0
    """
    x, y = case
    if indices[x][y] is None:
        return None
    else:
        liste_segments = [(case, (x, y+1)), (case, (x+1, y)),
                          ((x+1, y), (x+1, y+1)), ((x, y+1), (x+1, y+1))]
        nombre_segments = 0

        for segment in etat:
            if segment in liste_segments and etat[segment] == 1:
                nombre_segments += 1
        if int(indices[x][y]) == nombre_segments:
            return 0
        elif int(indices[x][y]) < nombre_segments:
            return 1
        elif int(indices[x][y]) > nombre_segments:
            return -1


def indices_satisfaits(indices, etat):
    """
    Renvoie True si tous les indices sont satisfaits, False sinon

    :param indices: list
    :param etat: dict

    >>> indices = [[2, 1]]
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (1, 1)): 1}
    >>> indices_satisfaits(indices, etat)
    True
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1}
    >>> indices_satisfaits(indices, etat)
    False
    """
    indice = []
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] is not None:
                case = (i, j)
                indice.append(statut_case(indices, etat, case))
    for elem in indice:
        if elem != 0:
            return False
    return True


def longueur_boucle(etat, segment):
    """
    Renvoie la longueur de la boucle si les segments forment une boucle sinon
    renvoie None

    :param etat: dict
    :param sommet: tuple

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (1, 1)): 1}
    >>> etat2 = {((1, 0), (1, 1)): 1, ((0, 0), (1, 0)): 1}
    >>> etat.update(etat2)
    >>> longueur_boucle(etat, ((0, 0), (1, 0)))
    4
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (1, 1)): 1}
    >>> longueur_boucle(etat, ((0, 1), (1, 1)))
    """
    depart = segment[0]
    precedent = segment[0]
    courant = segment[1]
    nb_seg = 0
    while courant != depart:
        segments_courant = []
        for seg in etat:
            if etat[seg] == 1:
                point1, point2 = seg
                if point1 == courant or point2 == courant:
                    segments_courant.append(seg)
        if len(segments_courant) != 2:
            return None
        else:
            nb_seg += 1
            for seg in segments_courant:
                if precedent not in seg:
                    precedent = courant
                    for point in seg:
                        if point != precedent:
                            courant = point
    nb_seg += 1
    return nb_seg


def nombre_segments(etat):
    """
    Renvoie la nombre de segments au total dans segments

    :param etat: dict

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1}
    >>> nombre_segments(etat)
    2
    """
    nb_total_seg = 0
    for segment in etat:
        if etat[segment] == 1:
            nb_total_seg += 1
    return nb_total_seg


def victoire(etat, indices, segment):
    """
    Renvoie True si le joueur gagne, False sinon

    :param etat: dict
    :param indices: list
    :param segment: tuple

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1, ((0, 2), (1, 2)): 1}
    >>> etat2 = {((1, 2), (2, 2)): 1, ((2, 1), (2, 2)): 1}
    >>> etat3 = {((2, 0), (2, 1)): 1, ((1, 0), (2, 0)): 1, ((0, 0), (1, 0)): 1}
    >>> etat.update(etat2)
    >>> etat.update(etat3)
    >>> indices = [[2, 2], [2, 2]]
    >>> victoire(etat, indices, ((0, 0), (1, 0)))
    True
    """
    if segment is not None:
        if indices_satisfaits(indices, etat) and \
                longueur_boucle(etat, segment) == nombre_segments(etat):
            return True
    return False


def pixel_vers_case(x, y, marge, case):
    """
    Retourne la case en fonction de x, y en px
    marge et case correspondent à leurs tailles respectives

    :param x: int
    :param y: int
    :param marge: int
    :param case: int
    :return value: tuple

    >>> pixel_vers_case(30, 30, 25, 50)
    (0, 0)
    """
    return int((x - marge) // case), int((y - marge) // case)


def case_vers_pixel(a, b, marge, case):
    """
    Retourne les coordonnées en px d'une case en fonction de a et b
    marge et case correspondent à leurs tailles respectives

    :param a: int
    :param b: int
    :param marge: int
    :param case: int
    :return value: tuple

    >>> case_vers_pixel(0, 0, 25, 50)
    (25, 25)
    """
    return int(a * case + marge), int(b * case + marge)


def coordonnees_segments(i, j, marge, case, vertical, horizontal):
    """
    Retourne les coordonnées en px des sommets d'un segment

    :param i: int
    :param j: int
    :param marge: int
    :param case: int
    :param vertical: int
    :param horizontal: int
    :return value: tuple

    >>> coordonnees_segments(0, 0, 25, 50, 1, 0)
    (25, 25, 75, 25)
    >>> coordonnees_segments(0, 0, 25, 50, 0, 1)
    (25, 25, 25, 75)
    """
    a, b = case_vers_pixel(i, j, marge, case)
    c, d = case_vers_pixel(i + vertical, j + horizontal, marge, case)
    return a, b, c, d


def donne_segment(coord, marge, case):
    """
    Retourne le segment au format ((w, x), (y, z))

    :param coord: list
    :param marge: int
    :param case: int
    :return value: tuple

    >>> donne_segment([25, 25, 25, 75], 25, 50)
    ((0, 0), (0, 1))
    """
    a, b, c, d = coord
    segment = (pixel_vers_case(a, b, marge, case),
               pixel_vers_case(c, d, marge, case))
    return segment


def afficher_etat(etat, marge, case, epaisseur):
    """
    Affiche etat graphiquement

    :param etat: dict
    :param marge: int
    :param case: int
    :param epaisseur: int
    """
    for segment in etat:
        a, b = case_vers_pixel(
            segment[0][0], segment[0][1], marge, case)
        c, d = case_vers_pixel(
            segment[1][0], segment[1][1], marge, case)
        fltk.ligne(b, a, d, c, epaisseur=epaisseur)


def affiche_etat_console(etat):
    """
    Affiche etat dans la console

    :param etat: dict

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1}
    >>> affiche_etat_console(etat)
    {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1}
    """
    print(etat)


def donne_temps():
    """
    Donne l'heure actuelle

    return value: datetime.datetime
    """
    return datetime.datetime.now()


def calcule_temps(temps1, temps2, temps3):
    """
    Retourne le temps passé sur une grille sous la forme d'une liste avec
    [minutes, secondes]

    :param temps1: datetime.datetime
    :param temps2: datetime.datetime
    :param temps3: list
    :return value: list
    """
    diff = diff_temps(temps1, temps2)
    diff = divmod(diff.seconds, 60)
    temps = [int(diff[0]), int(diff[1])]
    temps3 = [int(temps3[0]), int(temps3[1])]
    temps[0] += temps3[0]
    temps[1] += temps3[1]
    temps = [str(temps[0]), str(temps[1])]
    if len(temps[0]) == 1:
        temps[0] = '0'+temps[0]
    if len(temps[1]) == 1:
        temps[1] = '0'+temps[1]
    return temps


def diff_temps(temps1, temps2):
    """
    Retourne la différence entre deux temps

    :return value: datetime.timedelta
    """
    return temps2 - temps1


def affiche_temps(temps):
    """
    Affiche le temps passé sur une grille

    :param temps: list
    """
    fltk.texte(250, 570, temps[0] + ':' + temps[1], couleur='green',
               ancrage='center', taille=12)


def affiche_victoire(texte, color):
    """
    Affiche le texte de victoire

    :param text: str
    :param color: str
    """
    fltk.texte(250, 550, texte, couleur=color,
               ancrage='center', taille=14)
    fltk.rectangle(10, 535, 165, 585, couleur='RoyalBlue3',
                   remplissage='RoyalBlue3')
    fltk.texte(90, 560, 'Afficher dans la console', couleur='white',
               ancrage='center', taille=10)


def bouton_quitter(texte):
    """
    Affiche le bouton "Quitter"

    :param texte: str
    """
    fltk.rectangle(340, 535, 490, 585, couleur='red3',
                   remplissage='red3', tag='quitter')
    fltk.texte(415, 560, texte, couleur='white',
               ancrage='center', taille=14, tag='quitter')


def efface_grille(grille):
    """
    Supprime la grille passée en paramètre dans le dossier "grilles"

    :param grille: str
    """
    os.remove('grilles/'+grille)


def gestion_solveur(etat, segment, som, graph, ind, marge, case, ep):
    """
    Gère les évènements du solveur (tracer et effacer des segments,
    récursivité) et retourne etat

    :param etat: dict
    :param segment: tuple
    :param som: int
    :param graph: bool
    :param ind: list
    :param marge: int
    :param case: int
    :param ep: int
    :return value: dict
    """
    if est_trace(etat, segment) is False:
        etat = tracer_segment_solveur(
            etat, segment, graph, marge, case, ep)
        if solveur(etat, ind, segment[som], graph, marge, case, ep) is True:
            return True
        else:
            if graph is True:
                etat = effacer_segment_graphique(etat, segment)
            else:
                etat = effacer_segment(etat, segment)
    return etat


def tracer_segment_solveur(etat, segment, graphique, marge, case, epaisseur):
    """
    Trace les segments du solveur en fonction du mode choisi : graphique ou non

    :param etat: dict
    :param segment: tuple
    :param graph: bool
    :param marge: int
    :param case: int
    :param ep: int
    :return value: dict
    """
    if graphique is True:
        a, b = case_vers_pixel(
            segment[0][0], segment[0][1], marge, case)
        c, d = case_vers_pixel(
            segment[1][0], segment[1][1], marge, case)
        etat = tracer_segment_graphique(
            etat, segment, [a, b, c, d], epaisseur)
    else:
        etat = tracer_segment(etat, segment)
    return etat


def indices_insatisfaits(indices, etat):
    """
    Reourne False si au moins un indice a trop de segments tracés autour

    :param indices: list
    :param etat: dict
    :return value: bool

    >>> indices = [[1]]
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1}
    >>> indices_insatisfaits(indices, etat)
    False
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] is not None:
                case = (i, j)
                if statut_case(indices, etat, case) == 1:
                    return False


def gestion_ev():
    """
    Gère les évènements pendant l'utilisation du solveur, la croix de la
    fenêtre et le bouton "Quitter"

    :return value: bool
    """
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)
    if tev == 'Quitte':
        return True
    elif tev == 'ClicGauche':
        x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
        if 340 <= x <= 490 and 535 <= y <= 585:
            return True


def solveur(etat, indices, sommet, graphique, marge, case, epaisseur):
    """
    Fonction récursive gérant le solveur, l'appel récursif se fait dans la
    fonciton gestion_solveur.

    :param etat: dict
    :param indices: list
    :param sommet: int
    :param graphique: bool
    :param marge: int
    :param case: int
    :param epaisseur: int
    :return value: bool
    """
    if graphique is True:
        fltk.attente(1/100)
    if (len(segments_traces(etat, sommet)) == 2 and
            indices_satisfaits(indices, etat)):
        affiche_victoire('Solution trouvée', 'green')
        return True
    elif gestion_ev():
        return True
    elif len(segments_traces(etat, sommet)) >= 2 or \
            indices_insatisfaits(indices, etat) is False:
        return False
    else:
        segment = (sommet, (sommet[0], sommet[1]))
        if segment[1][1] < len(indices[0]) and etat is not True:
            segment = (sommet, (sommet[0], sommet[1]+1))
            etat = gestion_solveur(
                etat, segment, 1, graphique, indices, marge, case, epaisseur)
        if segment[1][0] < len(indices) and etat is not True:
            segment = (sommet, (sommet[0]+1, sommet[1]))
            etat = gestion_solveur(
                etat, segment, 1, graphique, indices, marge, case, epaisseur)
        if sommet[1] > 0 and etat is not True:
            segment = ((sommet[0], sommet[1]-1), sommet)
            etat = gestion_solveur(
                etat, segment, 0, graphique, indices, marge, case, epaisseur)
        if sommet[0] > 0 and etat is not True:
            segment = ((sommet[0]-1, sommet[1]), sommet)
            etat = gestion_solveur(
                etat, segment, 0, graphique, indices, marge, case, epaisseur)
        if etat is True:
            return True
    return False


def selectionne_sommet(etat, indices, graphique, taille_marge, taille_case):
    """
    Fonction qui sélectionne les points pour le solveur par ordre de priorité,
    d'abord les sommets autour d'un indice '3', puis '2', puis '1' et enfin
    tous les autres

    :param etat: dict
    :param indices: list
    :param graphique: bool
    :param taille_marge: int
    :param taille_case: int
    :return value: bool
    """
    for indice in range(3, -1, -1):
        for i in range(len(indices)):
            for j in range(len(indices[i])):
                if indice == 0:
                    indice = None
                else:
                    indice = str(indice)
                if indices[i][j] == indice:
                    case = (i, j)
                    x, y = case
                    liste_sommets = [case, (x, y+1), (x+1, y), (x+1, y+1)]
                    for sommet in liste_sommets:
                        if solveur(etat, indices, sommet, graphique,
                                   taille_marge, taille_case, 8) is True:
                            return True
    return False


def newSolveur(graphique, largeur, hauteur):
    """
    Gère l'affichage et la gestion des modes solveur et solveur graphique

    :param graphique: bool
    :param largeur: int
    :param hauteur: int
    """
    fltk.efface_tout()
    grille, etat, _ = selection_grille(hauteur, largeur, os.listdir('grilles'))
    taille_case, taille_marge, indices = affiche_grille(
        grille, largeur, largeur)
    bouton_quitter('Stop')
    if graphique is False:
        fltk.attente(0.1)
    temps1 = donne_temps()
    if selectionne_sommet(etat, indices, graphique, taille_marge,
                          taille_case) is True:
        if graphique is False:
            afficher_etat(etat, taille_marge, taille_case, epaisseur=8)
    else:
        affiche_victoire('Aucune solution', 'red')
    affiche_temps(calcule_temps(temps1, donne_temps(), [0, 0]))
    fltk.efface('quitter')
    bouton_quitter('Quitter')
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicGauche':
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if 340 <= x <= 490 and 535 <= y <= 585:
                break
            elif 10 <= x <= 165 and 535 <= y <= 585:
                affiche_etat_console(etat)
        elif tev == 'Quitte':
            break


def ajoute_indice(grille, ajouter, i, j):
    """
    Ajoute un indice à grille

    :param grille: list
    :param ajouter: str
    :param i: int
    :param j: int
    :return value: list

    >>> grille = ['__', '__']
    >>> ajoute_indice(grille, '0', 0, 0)
    ['0_', '__']
    """
    grille_lst = list(grille[i])
    grille_lst[j] = ajouter
    grille_lst = "".join(grille_lst)
    grille[i] = grille_lst
    return grille


def createur_grille(largeur, hauteur):
    """
    Gère et affiche le mode permettant de créer des grilles graphiquement

    :param largeur: int
    :param hauteur: int
    """
    fltk.efface_tout()
    taille, _, _ = selection_grille(
        hauteur, largeur, ['2x2', '3x3', '4x4', '5x5', '6x6'])
    taille = taille[:1]
    grille = []
    for _ in range(int(taille)):
        grille.append('_' * int(taille) + '\n')
    case, marge, indices = affiche_grille(
        grille, largeur, largeur)
    bouton_quitter('Quitter')
    fltk.rectangle(10, 535, 165, 585, couleur='RoyalBlue3',
                   remplissage='RoyalBlue3')
    fltk.texte(90, 560, 'Enregistrer : "Grille' +
               str(numero_grille()) + '"', couleur='white',
               ancrage='center', taille=10)
    save = False
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicGauche':
            y, x = fltk.abscisse(ev), fltk.ordonnee(ev)
            if marge < x < largeur - marge and marge < y < largeur - marge:
                i, j = pixel_vers_case(x, y, marge, case)
                if indices[i][j] is None:
                    indices[i][j] = 0
                    grille = ajoute_indice(grille, str(indices[i][j]), i, j)
                elif int(indices[i][j]) < 3:
                    ind = int(indices[i][j])
                    ind += 1
                    indices[i][j] = ind
                    grille = ajoute_indice(grille, str(indices[i][j]), i, j)

                else:
                    indices[i][j] = None
                    ajoute_indice(grille, '_', i, j)
                fltk.efface_tout()
                case, marge, indices = affiche_grille(
                    grille, largeur, largeur)
                bouton_quitter('Quitter')
                fltk.rectangle(10, 535, 165, 585, couleur='RoyalBlue3',
                               remplissage='RoyalBlue3')
                fltk.texte(90, 560, 'Enregistrer : "Grille' +
                           str(numero_grille()) + '"', couleur='white',
                           ancrage='center', taille=10)
            if 340 <= y <= 490 and 535 <= x <= 585:
                break
            if 10 <= y <= 165 and 535 <= x <= 585 and save is False:
                sauvegarde_grille(grille, {}, False, 0)
                fltk.texte(250, 560, 'Grille Sauvegardée', couleur='green',
                           ancrage='center', taille=14)
                save = True
        elif tev == 'Quitte':
            break


def sauvegarde_grille(grille, etat, temp, temps):
    """
    Sauvegarde une grille dans le dossier "grilles"

    :param grille: dict
    """
    if temp is False:
        f = open('grilles/grille' + str(numero_grille()) + '.txt', 'w')
    else:
        f = open('grilles/reprendre-grille.txt', 'w')
    for ligne in grille:
        f.write(ligne)
    f.close()
    if temp is True:
        f = open('grilles/reprendre-grille.txt', 'a')
        f.write(str(etat))
        f.write('\n'+str(temps))
        f.close()


def numero_grille():
    """
    Retourne le numéro de la dernière grille + 1

    :return value: int
    """
    n_grille = []
    for grille in os.listdir('grilles'):
        try:
            n_grille.append(int(grille[6:].replace('.txt', '')))
        except ValueError:
            pass
    return max(n_grille) + 1


def trieLstGrille(grilles):
    """
    Trie les grilles du dossiers "grilles" et retourne une liste avec les
    grilles dans l'ordre croissant

    :param grilles: list
    :return value: list

    >>> trieLstGrille(['Grille2', 'Grille1'])
    ['Grille1', 'Grille2']
    """
    grilleDict = {}
    dico = {}
    if 'reprendre-grille.txt' in grilles:
        dico.update({'reprendre-grille.txt': 0})
    for grille in grilles:
        try:
            grilleDict[grille] = int(grille[6:].replace('.txt', ''))
        except ValueError:
            pass
    dico.update(dict(sorted(grilleDict.items(), key=lambda item: item[1])))
    lstGrille = list(dico.keys())
    for grille in grilles:
        if grille not in lstGrille:
            lstGrille.append(grille)
    return lstGrille


def affiche_selection_grille(grilles, hauteur):
    """
    Affiche le menu de sélection des grilles

    :param grilles: list
    :param hauteur: int
    :return value: dict
    """
    elem = {}
    x = 0
    n = 0
    for grille in grilles:
        y = n * 50
        if y >= hauteur:
            x += 125
            n = 0
            y = n * 50
        elem[grille] = [x, y, x + 125, y + 50]
        fltk.rectangle(x, y, x + 125, y + 50)
        grille = grille.replace('.txt', '')
        grille = grille.replace('-', ' ')
        grille = grille.capitalize()
        fltk.texte(x + 62.5, y + 25, grille, ancrage='center', taille=10)
        n += 1
    return elem


def selection_grille(hauteur, largeur, grilles):
    """
    Affiche et gère le menu de sélection des grilles

    :param hauteur: int
    :param largeur: int
    :param grilles: list
    :return value: tuple
    """
    fltk.rectangle(0, 0, largeur, hauteur,
                   couleur='white', remplissage='white')
    trieLstGrille(grilles)
    grilles = trieLstGrille(grilles)
    etat = {}
    temps = [0, 0]
    elem = affiche_selection_grille(grilles, hauteur)
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicGauche':
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            for grille in elem:
                if elem[grille][0] <= x <= elem[grille][2] and \
                        elem[grille][1] <= y <= elem[grille][3]:
                    if os.listdir('grilles')[0] in grilles:
                        f = open('grilles/' + grille)
                        grille = []
                        for line in f.readlines():
                            if line[:1] != '{' and line[:1] != '[':
                                grille.append(line)
                            elif line[:1] == '[':
                                temps = ast.literal_eval(line)
                            else:
                                etat = ast.literal_eval(line)
                        f.close()
                    return grille, etat, temps


def affiche_grille(grille, hauteur, largeur):
    """
    Affiche graphiquement la grille passée en paramètre et créer la liste des
    indices

    :param grille: list
    :param hauteur: int
    :param largeur: int
    :return value: tuple
    """
    fltk.rectangle(0, 0, largeur, hauteur+100,
                   couleur='white', remplissage='white')
    taille_marge = 25
    taille_marge_const = taille_marge
    taille_marge_y = taille_marge
    taille_case = (largeur - 2*taille_marge) / len(grille)
    rayon = 8
    indices = []
    for ligne in range(len(grille)):
        taille_marge = taille_marge_const
        if ligne < len(grille):
            ligne_indices = []
        for colonne in range(len(grille[0])):
            if ligne < len(grille) and grille[ligne][colonne] != '_' and\
                    grille[ligne][colonne] != '\n':
                ligne_indices.append(grille[ligne][colonne])
                fltk.texte(taille_marge + .5 * taille_case,
                           taille_marge_y + .5 *
                           taille_case, grille[ligne][colonne],
                           ancrage='center')

            elif ligne < len(grille) and grille[ligne][colonne] != '\n':
                ligne_indices.append(None)
            fltk.cercle(taille_marge, taille_marge_y,
                        rayon, remplissage="black")
            taille_marge += taille_case
        taille_marge_y += taille_case
        indices.append(ligne_indices)
    taille_marge = taille_marge_const
    for colonne in range(len(grille[0])):
        fltk.cercle(taille_marge, taille_marge_y,
                    rayon, remplissage="black")
        taille_marge += taille_case
    return taille_case, taille_marge_const, indices


def clic_dans_grille(x, y, marge, case, largeur, ep, etat, function, segment):
    """
    Gère les clics dans la grille dans le mode "jouer"

    :param x: int
    :param y: int
    :param marge: int
    :param case: int
    :param largeur: int
    :param ep: int
    :param etat: dict
    :param function: function
    :param segment: tuple
    :return value: tuple
    """
    i, j = pixel_vers_case(x, y, marge, case)
    dx = (x - marge) / case
    dy = (y - marge) / case
    if (-0.2 < dx - round(dx) < 0.2) is True:
        if dx - round(dx) < 0:
            i += 1
        a, b, c, d = coordonnees_segments(i, j, marge, case, 0, 1)
        if d < largeur and b > 0:
            segment = donne_segment([a, b, c, d], marge, case)
            etat = function(etat, segment, [a, b, c, d], ep)
    elif (-0.2 < dy - round(dy) < 0.2) is True:
        if dy - round(dy) < 0:
            j += 1
        a, b, c, d = coordonnees_segments(i, j, marge, case, 1, 0)
        if c < largeur and a > 0:
            segment = donne_segment([a, b, c, d], marge, case)
            etat = function(etat, segment, [a, b, c, d], ep)
    return etat, segment


def onclick(ev, clic, etat, marge, case, largeur, epaisseur, win):
    """
    Gère les clics dans le mode "jouer", appelle la fonction clic_dans_grille
    si le clic est dans la grille

    :param ev: tuple
    :param clic: int
    :param etat: dict
    :param marge: int
    :param case: int
    :param largeur: int
    :param epaisseur: int
    :param win: bool
    :return value: bool
    """
    functions = [tracer_segment_graphique, interdire_segment_graphique]
    function = functions[clic]
    segment = None
    y, x = fltk.abscisse(ev), fltk.ordonnee(ev)
    if 340 <= y <= 490 and 535 <= x <= 585:
        return etat, False
    elif win is True and 10 <= y <= 165 and 535 <= x <= 585:
        affiche_etat_console(etat)
    elif x < 500:
        etat, segment = clic_dans_grille(
            x, y, marge, case, largeur, epaisseur, etat, function, segment)
    return etat, segment


def jouer(largeur, hauteur):
    """
    Gère le mode jouer

    :param largeur: int
    :param hauteur: int
    """
    grille, etat, temps3 = selection_grille(
        hauteur, largeur, os.listdir('grilles'))
    taille_case, taille_marge, indices = affiche_grille(
        grille, largeur, largeur)
    epaisseur = 8
    temp = False
    if etat != {}:
        afficher_etat(etat, taille_marge, taille_case, epaisseur)
        temp = True
    bouton_quitter('Quitter')
    segment = None
    win = False
    temps1 = donne_temps()
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicGauche':
            etat, segment = onclick(
                ev, 0, etat, taille_marge, taille_case, largeur,
                epaisseur, win)
        elif tev == 'ClicDroit':
            etat, segment = onclick(
                ev, 1, etat, taille_marge, taille_case, largeur,
                epaisseur, win)
        if tev == 'Quitte' or segment is False:
            if win is False:
                sauvegarde_grille(grille, etat, True,
                                  calcule_temps(temps1, donne_temps(),
                                                temps3))
            break
        if victoire(etat, indices, segment) is True:
            affiche_victoire('Victoire !', 'green')
            win = True
            affiche_temps(calcule_temps(temps1, donne_temps(), temps3))
            if temp is True:
                efface_grille('reprendre-grille.txt')


def affiche_menu(largeur, hauteur):
    """
    Affiche le menu principal avec fltk

    :param largeur: int
    :param hauteur: int
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, largeur, hauteur,
                   couleur='white', remplissage='white')
    fltk.texte(250, 100, 'Slitherlink', ancrage='center')
    fltk.rectangle(100, 160, 400, 230, couleur='lime green',
                   remplissage='lime green')
    fltk.rectangle(100, 260, 400, 330, couleur='RoyalBlue3',
                   remplissage='RoyalBlue3')
    fltk.rectangle(100, 360, 400, 430, couleur='RoyalBlue3',
                   remplissage='RoyalBlue3')
    fltk.rectangle(100, 460, 400, 530, couleur='RoyalBlue3',
                   remplissage='RoyalBlue3')
    fltk.texte(250, 195, 'Jouer', couleur='white', ancrage='center', taille=16)
    fltk.texte(250, 295, 'Solveur', couleur='white',
               ancrage='center', taille=16)
    fltk.texte(250, 395, 'Solveur Graphique',
               couleur='white', ancrage='center', taille=16)
    fltk.texte(250, 495, 'Créateur de Grilles',
               couleur='white', ancrage='center', taille=16)


def menu():
    """
    Gère les évènements du menu
    """
    hauteur = 600
    largeur = 500
    fltk.cree_fenetre(largeur, hauteur)
    affiche_menu(largeur, hauteur)
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicGauche':
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if 100 <= x <= 400 and 160 <= y <= 230:
                fltk.efface_tout()
                jouer(largeur, hauteur)
            elif 100 <= x <= 400 and 260 <= y <= 330:
                newSolveur(False, largeur, hauteur)
            elif 100 <= x <= 400 and 360 <= y <= 430:
                newSolveur(True, largeur, hauteur)
            elif 100 <= x <= 400 and 460 <= y <= 530:
                createur_grille(largeur, hauteur)
            affiche_menu(largeur, hauteur)
        elif tev == 'Quitte':
            break
    fltk.ferme_fenetre()


if __name__ == '__main__':
    testmod()
    menu()
