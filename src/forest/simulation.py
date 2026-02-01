## IMPORTATIONS NECESSAIRES ##
import random

## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    ## Initialisation de la grille ##
    def __init__(self, height, width, args):
        self.__burning_trees = set()    # On va stocker les arbres en feu dans un set
        self.__alive_trees = set()  
        self.__no_trees = set()    # On va stocker les cases vides dans un set
        self.__height = height
        self.__width = width
        ## Initialisation de la grille avec des arbres vivants (nombre args[0]) et des cases vides aléatoires ##
        tree_number = args.nbtrees
        while len(self.__alive_trees) < tree_number:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.__alive_trees.add((x, y))

    
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
    def evolve(self,args):
        new_burning_trees = set() # On crée un nouveau set pour les arbres en feu de la prochaine génération
        new_alive_trees = set()
        new_no_trees = set()    # On crée un nouveau set pour les cases vides de la prochaine génération

        ## Pousse aléatoire des arbres dans les cases vides ##
        for (x, y) in self.__no_trees:
            if random.random() < args.tree_probability:  # PROBA_GROW
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        ## Enflammer aléatoirement les arbres vivants ##
        for (x, y) in self.__alive_trees:
            if random.random() < args.fire_probability:  # PROBA_FIRE
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
