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
        
        ## Nettoyage des sets ##
        self.__burning_trees.clear()
        self.__alive_trees.clear()

        ## Lecture du fichier ##
        with open(filename, 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line.rstrip('\n')):
                    if x < self.__width and y < self.__height: # On vérifie qu'on ne dépasse pas les dimensions
                        if char == 'o':  # On considère 'o' comme un arbre vivant
                            self.__alive_trees.add((x, y)) # On ajoute l'arbre vivant au set
                        elif char == '*':  # On considère '*' comme un arbre en feu
                            self.__burning_trees.add((x, y)) # On ajoute l'arbre en feu au set
    
    ## Sauvegarder le contenu de la grille finale dans un fichier ##
    def save_to_file(self, filename):
        pass

    ## Calculer la prochaine génération de la grille ##
    def evolve(self):
        pass

## FONCTION DE SIMULATION ##
def start_simulation():
    print("Simulation started.")