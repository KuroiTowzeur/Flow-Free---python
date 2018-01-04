import os
from constante import *


def sort_file(image):
    image = sorted(image, key=lambda image: int(image.split('-')[1]))  # tri par numero de niveau
    image = sorted(image, key=lambda image: int(image.split('-')[0]))  # tri par grille
    return image


def write_file(user, image):
    path = 'scores_joueurs/Score_{}.txt'.format(user)
    with open(path, 'w') as file:
        for ligne in image:
            file.write(ligne)


def read_file(user):
    path = 'scores_joueurs/Score_{}.txt'.format(user)
    with open(path, 'r') as file:
        image = file.readlines()
    return image


def init_dic_scores(pack=regularpack):
    dic_score = {plateau[0]: {} for plateau in regularpack}
    return dic_score


def load_score(user):
    '''renvoie un dictionnaire contenant les scores du joueur : user'''
    path = 'scores_joueurs/Score_{}.txt'.format(user)

    dic_score = init_dic_scores()

    if os.path.exists(path):  # si le fichier existe
        with open(path, 'r') as file:
            l = [ligne.replace('\n', '').split('-') for ligne in file.readlines()]
            l = [[int(ligne[n]) for n in range(3)] + [ligne[3]] for ligne in l]

            for numero_ligne, ligne in enumerate(l):
                taille_grille, numero_niveau, action, state = ligne
                dic_score[taille_grille][numero_niveau] = (numero_ligne, action, state)

    else:  # si le fichier n'existe pas
        file = open(path, 'w')
        file.close()

    return dic_score


def presence(dic_score, taille_grille, numero_niveau):
    listes_niveaux = dic_score[taille_grille]
    keys = list(listes_niveaux.keys())
    return (numero_niveau in keys)


def n_ligne(dic_score, taille_grille, numero_niveau):
    return dic_score[taille_grille][numero_niveau][0]


def save_score(user, taille_grille, numero_niveau, action, state):
    scores = load_score(user)
    format = str(taille_grille) + '-' + str(numero_niveau) + '-' + str(action) + '-' + str(state)

    if presence(scores, taille_grille, numero_niveau):  # si il y a déjà un score

        ligne_existante = n_ligne(scores, taille_grille, numero_niveau)

        if action < scores[taille_grille][numero_niveau][1]:  # Est ce que c'est un meilleur score ?
            image = read_file(user)
            image[ligne_existante] = format + '\n'

            image = sort_file(image)
            write_file(user, image)

    else:  # il ny a aucun score, on l'ajoute donc
        image = read_file(user)
        image.append(format + '\n')

        image = sort_file(image)
        write_file(user, image)

def cb_map_clear(dic_score):
    nb_map = 0
    for taille_grille, plateau in dic_score.items():
        nb_map += len(plateau)
    return(nb_map)

