## IMPORTATIONS NECESSAIRES ##
import random
import pygame

## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    def __init__(self, height, width, args):
        self.__burning_trees = set()
        self.__alive_trees = set()
        self.__no_trees = set()
        self.__height = height
        self.__width = width
        
        # Initialisation de la grille
        tree_number = args.nbtrees
        while len(self.__alive_trees) < tree_number:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.__alive_trees.add((x, y))
        
        # Remplir le set des cases vides
        for y in range(height):
            for x in range(width):
                if (x, y) not in self.__alive_trees:
                    self.__no_trees.add((x, y))

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

    ## --- PARTIE GRAPHIQUE AMELIOREE --- ##
    def draw(self, screen, cell_size):
        # 1. PALETTE DE COULEURS "MODERNE"
        # Fond (Terre sombre)
        COLOR_BG = (45, 40, 40)       
        
        # Arbres (Vert nature + Ombre foncée)
        COLOR_TREE = (46, 139, 87)    # SeaGreen
        COLOR_TREE_SHADOW = (20, 60, 35)
        
        # Feu (Orange vibrant + Coeur jaune + Ombre rouge sombre)
        COLOR_FIRE = (255, 69, 0)     # OrangeRed
        COLOR_FIRE_CENTER = (255, 215, 0) # Gold
        COLOR_FIRE_SHADOW = (139, 0, 0) # DarkRed

        # Remplissage du fond
        screen.fill(COLOR_BG) 

        # Calcul des marges pour l'effet "Tuile"
        # Si les cases sont très petites, on réduit les détails pour pas que ça bave
        gap = 1 if cell_size > 4 else 0
        shadow_offset = 2 if cell_size > 6 else 0
        block_size = max(1, cell_size - gap)

        # FONCTION INTERNE POUR DESSINER UNE TUILE 3D
        def draw_tile(x, y, color, shadow_color, is_fire=False):
            rect_x = x * cell_size
            rect_y = y * cell_size
            
            # 1. L'Ombre (décalée en bas à droite)
            if shadow_offset > 0:
                shadow_rect = pygame.Rect(rect_x + shadow_offset, rect_y + shadow_offset, block_size, block_size)
                pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=2)

            # 2. Le bloc principal
            main_rect = pygame.Rect(rect_x, rect_y, block_size, block_size)
            pygame.draw.rect(screen, color, main_rect, border_radius=2) # border_radius fait des coins un peu ronds (joli)

            # 3. Effet spécial pour le feu (coeur jaune)
            if is_fire and block_size > 4:
                center_size = block_size // 2
                offset = (block_size - center_size) // 2
                center_rect = pygame.Rect(rect_x + offset, rect_y + offset, center_size, center_size)
                pygame.draw.rect(screen, COLOR_FIRE_CENTER, center_rect, border_radius=1)

        # DESSIN DES ARBRES
        for (x, y) in self.__alive_trees:
            draw_tile(x, y, COLOR_TREE, COLOR_TREE_SHADOW)

        # DESSIN DU FEU
        for (x, y) in self.__burning_trees:
            draw_tile(x, y, COLOR_FIRE, COLOR_FIRE_SHADOW, is_fire=True)

    ## EVOLUTION (Logique inchangée) ##
    def evolve(self, args):
        new_burning_trees = set()
        new_alive_trees = set()
        new_no_trees = set()

        for (x, y) in self.__no_trees:
            if random.random() < args.tree_probability:
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        for (x, y) in self.__alive_trees:
            if random.random() < args.fire_probability:
                new_burning_trees.add((x, y))
            else:
                new_alive_trees.add((x, y))
        
        for (x, y) in self.__burning_trees:
            new_no_trees.add((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in self.__alive_trees:
                        new_burning_trees.add(neighbor)
                        
        new_alive_trees = new_alive_trees - new_burning_trees
        self.__burning_trees = new_burning_trees
        self.__alive_trees = new_alive_trees
        self.__no_trees = new_no_trees