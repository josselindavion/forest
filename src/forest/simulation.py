## IMPORTATIONS NECESSAIRES ##
import random
import pygame  # On importe pygame ici pour la méthode draw

## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    ## Initialisation de la grille ##
    def __init__(self, height, width, args):
        self.__burning_trees = set()
        self.__alive_trees = set()
        self.__no_trees = set()
        self.__height = height
        self.__width = width
        
        ## Initialisation de la grille avec des arbres vivants ##
        tree_number = args.nbtrees
        while len(self.__alive_trees) < tree_number:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.__alive_trees.add((x, y))
        
        ##  Remplir le set des cases vides ##
        for y in range(height):
            for x in range(width):
                if (x, y) not in self.__alive_trees:
                    self.__no_trees.add((x, y))

    ## Sauvegarder le contenu de la grille finale dans un fichier ##
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for y in range(self.__height):
                line = ''
                for x in range(self.__width):
                    if (x, y) in self.__burning_trees:
                        line += '*'
                    elif (x, y) in self.__alive_trees:
                        line += 'o'
                    else:
                        line += ' '
                file.write(line + '\n')

    ## Affichage graphique avec Pygame (NOUVEAU) ##
    def draw(self, screen, cell_size):
        ## Couleurs
        COLOR_BG = (30, 30, 30)        # Gris foncé (sol brulé/vide)
        COLOR_TREE = (34, 139, 34)     # Vert forêt
        COLOR_FIRE = (255, 69, 0)      # Rouge orange feu
        
        screen.fill(COLOR_BG) # On remplit tout en "vide" par défaut

        ## Dessiner les arbres vivants
        for (x, y) in self.__alive_trees:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, COLOR_TREE, rect)

        ## Dessiner les arbres en feu (avec un petit effet visuel)
        for (x, y) in self.__burning_trees:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, COLOR_FIRE, rect)

    ## Calculer la prochaine génération de la grille ##
    def evolve(self, args):
        new_burning_trees = set()
        new_alive_trees = set()
        new_no_trees = set()

        ## Pousse aléatoire des arbres dans les cases vides ##
        for (x, y) in self.__no_trees:
            if random.random() < args.tree_probability:
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        ## Enflammer aléatoirement les arbres vivants (feu spontané) ##
        for (x, y) in self.__alive_trees:
            if random.random() < args.fire_probability:
                new_burning_trees.add((x, y))
            else:
                new_alive_trees.add((x, y))
        
        ## Propagation du feu aux arbres voisins ##
        for (x, y) in self.__burning_trees:
            new_no_trees.add((x, y)) ## L'arbre en feu meurt
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    
                    ## Si le voisin est un arbre vivant (de la grille actuelle), il prend feu
                    ## On l'ajoute au futur set de feu
                    if neighbor in self.__alive_trees:
                        new_burning_trees.add(neighbor)
                        
        ## Nettoyage logique ##
        ## Si un arbre a été mis dans "new_alive" mais qu'il a pris feu à cause d'un voisin,
        ## il doit être retiré des vivants pour ne pas être dupliqué
        new_alive_trees = new_alive_trees - new_burning_trees

        ## Mise à jour ##
        self.__burning_trees = new_burning_trees
        self.__alive_trees = new_alive_trees
        self.__no_trees = new_no_trees