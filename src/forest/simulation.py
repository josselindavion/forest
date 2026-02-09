## IMPORTATIONS NECESSAIRES ##
import random
import pygame
import logging

## Récupération du logger du module ##
logger = logging.getLogger(__name__)

## CLASSE DE LA GRILLE PRINCIPALE ##
class Grid:

    def __init__(self, height, width, args):
        self.__burning_trees = set()
        self.__alive_trees = set()
        self.__no_trees = set()
        self.__height = height
        self.__width = width
        
        ## Dictionnaire pour stocker une variation de couleur par arbre (pour que ce soit moins monotone) ##
        self.__tree_shades = {} 
        
        ## Initialisation de la grille ##
        tree_number = args.nbtrees
        while len(self.__alive_trees) < tree_number:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.add_tree(x, y)
        
        logger.debug(f"Grille initialisée : {width}x{height} avec {len(self.__alive_trees)} arbres.")
        
        ## Remplir le set des cases vides ##
        for y in range(height):
            for x in range(width):
                if (x, y) not in self.__alive_trees:
                    self.__no_trees.add((x, y))

    def add_tree(self, x, y):
        self.__alive_trees.add((x, y))
        ## On assigne une nuance de vert aléatoire à cet arbre (entre 0 et 3) ##
        self.__tree_shades[(x, y)] = random.randint(0, 2)

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
        logger.debug(f"Fichier {filename} généré.")

    ## --- RENDU GRAPHIQUE 3D --- ##
    def draw(self, screen, cell_size):
        ## CONFIGURATION DES COULEURS ##
        BG_COLOR = (30, 25, 25) ## Sol très foncé ##
        
        ## Nuances d'arbres (Top, Face, Ombre) ##
        ## On définit 3 types d'arbres pour varier la forêt ##
        TREE_PALETTES = [
            {'face': (34, 139, 34), 'light': (60, 179, 60), 'dark': (20, 80, 20)},  ## Forest Green ##
            {'face': (46, 139, 87), 'light': (70, 180, 110), 'dark': (25, 80, 50)}, ## Sea Green ##
            {'face': (0, 128, 0),   'light': (50, 160, 50),  'dark': (0, 70, 0)}    ## Dark Green ##
        ]

        ## Couleurs du Feu (Jaune au centre, Rouge autour) ##
        FIRE_FACE = (255, 69, 0)   ## Rouge orange ##
        FIRE_LIGHT = (255, 140, 0) ## Orange clair ##
        FIRE_DARK = (139, 0, 0)    ## Rouge sang ##
        FIRE_CORE = (255, 255, 0)  ## Jaune pur ##
        
        screen.fill(BG_COLOR)

        ## Paramètres de "Tuile" ##
        ## On force un gap d'au moins 1 ou 2 pixels ##
        gap = max(1, cell_size // 10) 
        block_size = cell_size - gap
        
        ## Si la case est trop petite (<4px), on dessine juste des carrés simples pour la perf ##
        simple_mode = block_size < 4

        def draw_3d_block(x, y, palette, is_fire=False):
            ## Coordonnées pixel ##
            px = x * cell_size + (gap // 2)
            py = y * cell_size + (gap // 2)
            
            rect = pygame.Rect(px, py, block_size, block_size)

            if simple_mode:
                pygame.draw.rect(screen, palette['face'], rect)
                return

            ## 1. OMBRE PORTÉE (Décalage en bas à droite sur le sol) ##
            ## On dessine un rectangle noir transparent (simulé par une couleur sombre du sol) ##
            shadow_offset = max(2, block_size // 5)
            shadow_rect = pygame.Rect(px + shadow_offset//2, py + shadow_offset//2, block_size, block_size)
            pygame.draw.rect(screen, (15, 10, 10), shadow_rect, border_radius=3)

            ## 2. FACE PRINCIPALE (Le corps du bloc) ##
            pygame.draw.rect(screen, palette['face'], rect, border_radius=3)

            ## 3. RELIEF (Bevel) - Effet lumière en haut/gauche ##
            ## On dessine une ligne ou un rect partiel pour simuler la lumière ##
            highlight_rect = pygame.Rect(px, py, block_size, block_size // 4) ## Bandeau haut ##
            pygame.draw.rect(screen, palette['light'], highlight_rect, border_top_left_radius=3, border_top_right_radius=3)

            ## 4. RELIEF (Bevel) - Effet ombre en bas ##
            shadow_bottom_rect = pygame.Rect(px, py + block_size - (block_size // 4), block_size, block_size // 4)
            pygame.draw.rect(screen, palette['dark'], shadow_bottom_rect, border_bottom_left_radius=3, border_bottom_right_radius=3)

            ## 5. COEUR DU FEU (Animation simple) ##
            if is_fire:
                core_size = block_size // 2
                offset = (block_size - core_size) // 2
                core_rect = pygame.Rect(px + offset, py + offset, core_size, core_size)
                pygame.draw.rect(screen, FIRE_CORE, core_rect, border_radius=2)

        ## DESSIN ARBRES ##
        for (x, y) in self.__alive_trees:
            ## On récupère la nuance attribuée à cet arbre ##
            shade_index = self.__tree_shades.get((x, y), 0)
            draw_3d_block(x, y, TREE_PALETTES[shade_index])

        ## DESSIN FEU ##
        fire_palette = {'face': FIRE_FACE, 'light': FIRE_LIGHT, 'dark': FIRE_DARK}
        for (x, y) in self.__burning_trees:
            draw_3d_block(x, y, fire_palette, is_fire=True)

    ## EVOLUTION (Logique standard) ##
    def evolve(self, args):
        new_burning_trees = set()
        new_alive_trees = set()
        new_no_trees = set()

        ## Pousse ##
        for (x, y) in self.__no_trees:
            if random.random() < args.tree_probability:
                self.add_tree(x, y) ## On utilise add_tree pour donner une couleur ##
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        ## Feu spontané ##
        for (x, y) in self.__alive_trees:
            if random.random() < args.fire_probability:
                new_burning_trees.add((x, y))
            else:
                new_alive_trees.add((x, y))
        
        ## Propagation ##
        for (x, y) in self.__burning_trees:
            new_no_trees.add((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in self.__alive_trees:
                        new_burning_trees.add(neighbor)
        
        if len(new_burning_trees) > 0:
            logger.debug(f"Evolution : {len(new_burning_trees)} arbres en feu.")
                        
        ## Nettoyage ##
        new_alive_trees = new_alive_trees - new_burning_trees
        
        ## Mise à jour des sets ##
        self.__burning_trees = new_burning_trees
        self.__alive_trees = new_alive_trees
        self.__no_trees = new_no_trees
        
        ## IMPORTANT : Mettre à jour le dictionnaire des couleurs ##
        ## On garde les couleurs des arbres survivants, on jette les autres ##
        new_shades = {}
        for pos in new_alive_trees:
            if pos in self.__tree_shades:
                new_shades[pos] = self.__tree_shades[pos]
            else:
                ## Au cas où un arbre apparait sans couleur (ne devrait pas arriver avec add_tree) ##
                new_shades[pos] = random.randint(0, 2)
        self.__tree_shades = new_shades