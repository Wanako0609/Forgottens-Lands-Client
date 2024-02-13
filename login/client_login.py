from login.network_login import NetworkLogin
import uuid
import bcrypt


def str_list(string):
    liste_data = string.split(",")
    return [liste_data[0], liste_data[1], liste_data[2]]


def list_str(liste):
    return str(liste[0]) + "," + str(liste[1]) + "," + str(liste[2])


def hash_mot_de_passe(mot_de_passe):
    # Générer un hachage de mot de passe avec bcrypt
    return bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())


def est_uuid_valide(chaine):
    try:
        uuid.UUID(chaine)
        return True
    except ValueError:
        return False


def login_func():
    user = input("Nom d'utilisateur : ")
    password = input("Mot de Passe : ")
    return [0, user, password]


def register_func():
    user = input("Nom d'utilisateur : ")
    password = input("Mot de Passe : ")
    return [1, user, password]


def causer_erreur(str):
    print(str)
    assert False, str


def login_user():

    data = []
    # Envoie du login et mdp cypté
    response = True
    while response:
        compte = input("Avez vous un compte ? (oui/non) : ")
        if compte == "oui":
            data = login_func()
            response = False
        elif compte == "non":
            data = register_func()
            response = False

    # Connection
    n = NetworkLogin()
    recu = n.send(list_str(data))
    if est_uuid_valide(recu):
        print("Reponse : ", recu)
        return recu

    causer_erreur(recu)
