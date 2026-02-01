## IMPORTATIONS NECESSAIRES ##
import random

## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    ## Initialisation de la grille ##
    def __init__(self, height, width):
        self.__burning_trees = set()    # On va stocker les arbres en feu dans un set
        self.__alive_trees = set()  
        self.__no_trees = set()    # On va stocker les cases vides dans un set
        self.__height = height
        self.__width = width

    ## Lire le contenu initial de la grille depuis un fichier ##
    def load_from_file(self, filename):
        
        ## Nettoyage des sets ##
        self.__burning_trees.clear()
        self.__alive_trees.clear()
        self.__no_trees.clear()
        ## Lecture du fichier ##
        with open(filename, 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line.rstrip('\n')):
                    if x < self.__width and y < self.__height: # On vérifie qu'on ne dépasse pas les dimensions
                        if char == 'o':  # On considère 'o' comme un arbre vivant
                            self.__alive_trees.add((x, y)) # On ajoute l'arbre vivant au set
                        elif char == '*':  # On considère '*' comme un arbre en feu
                            self.__burning_trees.add((x, y)) # On ajoute l'arbre en feu au set
                        else:  # On considère tout autre caractère comme une case vide
                            self.__no_trees.add((x, y)) # On ajoute la case vide au set
    
    ## Sauvegarder le contenu de la grille finale dans un fichier ##
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for y in range(self.__height):
                line = ''
                for x in range(self.__width):
                    if (x, y) in self.__burning_trees:
                        line += '*'  # On concatène l'arbre en feu
                    elif (x, y) in self.__alive_trees:
                        line += 'o'  # On concatène l'arbre vivant
                    else:
                        line += ' '  # On concatène une case vide
                file.write(line + '\n')

    ## Calculer la prochaine génération de la grille ##
    def evolve(self):
        new_burning_trees = set() # On crée un nouveau set pour les arbres en feu de la prochaine génération
        new_alive_trees = set()
        new_no_trees = set()    # On crée un nouveau set pour les cases vides de la prochaine génération

        ## Pousse aléatoire des arbres dans les cases vides ##
        for (x, y) in self.__no_trees:
            if random.random() < args[4]:  # PROBA_GROW
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        ## Enflammer aléatoirement les arbres vivants ##
        for (x, y) in self.__alive_trees:
            if random.random() < args[3]:  # PROBA_FIRE
                new_burning_trees.add((x, y))
            else:
                new_alive_trees.add((x, y))
        
        ## Propagation du feu aux arbres voisins ##
        for (x, y) in self.__burning_trees:
            ## L'arbre en feu brule et disparait ##
            new_no_trees.add((x, y))
            ## On parcourt les voisins et on enflamme les arbres adjacents qui sont étains vivants ##
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in self.__alive_trees:
                        new_burning_trees.add(neighbor)
        
        ## Mise à jour ##
        self.__burning_trees = new_burning_trees
        self.__alive_trees = new_alive_trees
        self.__no_trees = new_no_trees


## FONCTION DE SIMULATION ##
def start_simulation():
    print("Simulation started.")