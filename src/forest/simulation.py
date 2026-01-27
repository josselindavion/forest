## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    ## Initialisation de la grille ##
    def __init__(self, height, width):
        self.__burning_trees = set()    # On va stocker les arbres en feu dans un set
        self.__alive_trees = set()      # On va stocker les arbres vivants dans un set
        self.__height = height
        self.__width = width

    ## Lire le contenu initial de la grille depuis un fichier ##
    def load_from_file(self, filename):
        pass

    ## Sauvegarder le contenu de la grille finale dans un fichier ##
    def save_to_file(self, filename):
        pass

    ## Calculer la prochaine génération de la grille ##
    def evolve(self):
        pass

## FONCTION DE SIMULATION ##
def start_simulation():
    print("Simulation started.")