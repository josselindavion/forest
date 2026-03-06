"""Module gérant la logique de la grille et des entités de la simulation."""

# IMPORTATIONS NECESSAIRES
import random
import logging
# AJOUT POUR LE TYPAGE
from typing import Set, Tuple, Dict, Any
from argparse import Namespace

import pygame

# Récupération du logger du module
logger = logging.getLogger(__name__)

# --- NOUVELLES CLASSES POUR L'ISSUE 14 ---

class Block:
    """Classe de base pour dessiner une case en 3D."""
    def __init__(self, x: int, y: int, cell_size: int, palette: Dict[str, Any]) -> None:
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.palette = palette
        self.gap = max(1, cell_size // 10)
        self.block_size = cell_size - self.gap
        self.simple_mode = self.block_size < 4

    def draw(self, screen: Any) -> None:
        """Dessine le bloc sur l'écran."""
        px = self.x * self.cell_size + (self.gap // 2)
        py = self.y * self.cell_size + (self.gap // 2)
        rect = pygame.Rect(px, py, self.block_size, self.block_size)

        if self.simple_mode:
            pygame.draw.rect(screen, self.palette['face'], rect)
            return

        # 1. OMBRE PORTÉE
        shadow_offset = max(2, self.block_size // 5)
        shadow_rect = pygame.Rect(px + shadow_offset//2, py + shadow_offset//2, self.block_size, self.block_size)
        pygame.draw.rect(screen, (15, 10, 10), shadow_rect, border_radius=3)

        # 2. FACE PRINCIPALE
        pygame.draw.rect(screen, self.palette['face'], rect, border_radius=3)

        # 3. RELIEF HAUT
        highlight_rect = pygame.Rect(px, py, self.block_size, self.block_size // 4)
        pygame.draw.rect(screen, self.palette['light'], highlight_rect, border_top_left_radius=3, border_top_right_radius=3)

        # 4. RELIEF BAS
        shadow_bottom_rect = pygame.Rect(px, py + self.block_size - (self.block_size // 4), self.block_size, self.block_size // 4)
        pygame.draw.rect(screen, self.palette['dark'], shadow_bottom_rect, border_bottom_left_radius=3, border_bottom_right_radius=3)

class TreeBlock(Block):
    """Bloc représentant un arbre."""
    TREE_PALETTES = [
        {'face': (34, 139, 34), 'light': (60, 179, 60), 'dark': (20, 80, 20)},
        {'face': (46, 139, 87), 'light': (70, 180, 110), 'dark': (25, 80, 50)},
        {'face': (0, 128, 0),   'light': (50, 160, 50),  'dark': (0, 70, 0)}
    ]

    def __init__(self, x: int, y: int, cell_size: int, shade_index: int) -> None:
        super().__init__(x, y, cell_size, self.TREE_PALETTES[shade_index])

class FireBlock(Block):
    """Bloc représentant un feu avec son cœur jaune."""
    FIRE_PALETTE = {'face': (255, 69, 0), 'light': (255, 140, 0), 'dark': (139, 0, 0)}
    FIRE_CORE = (255, 255, 0)

    def __init__(self, x: int, y: int, cell_size: int) -> None:
        super().__init__(x, y, cell_size, self.FIRE_PALETTE)

    def draw(self, screen: Any) -> None:
        """Dessine le bloc en feu."""
        # On dessine la base du bloc d'abord
        super().draw(screen)
        # Puis on ajoute le cœur de feu spécifique
        if not self.simple_mode:
            px = self.x * self.cell_size + (self.gap // 2)
            py = self.y * self.cell_size + (self.gap // 2)
            core_size = self.block_size // 2
            offset = (self.block_size - core_size) // 2
            core_rect = pygame.Rect(px + offset, py + offset, core_size, core_size)
            pygame.draw.rect(screen, self.FIRE_CORE, core_rect, border_radius=2)

# --- FIN DES NOUVELLES CLASSES ---

# CLASSE DE LA GRILLE PRINCIPALE
class Grid:
    """
    Classe gérant la grille de simulation, les arbres et le feu.
    """

    def __init__(self, height: int, width: int, args: Namespace) -> None:
        """
        Initialise la grille.

        Args:
            height (int): Hauteur.
            width (int): Largeur.
            args (Namespace): Arguments du programme.
        """
        self.__burning_trees: Set[Tuple[int, int]] = set()
        self.__alive_trees: Set[Tuple[int, int]] = set()
        self.__no_trees: Set[Tuple[int, int]] = set()
        self.__height: int = height
        self.__width: int = width
        
        # Dictionnaire pour stocker une variation de couleur par arbre
        self.__tree_shades: Dict[Tuple[int, int], int] = {} 
        
        # Initialisation de la grille
        tree_number = args.nbtrees
        while len(self.__alive_trees) < tree_number:
            x = random.randint(0, width - 1)  # noqa: S311
            y = random.randint(0, height - 1)  # noqa: S311
            self.add_tree(x, y)
        
        logger.debug(f"Grille initialisée : {width}x{height} avec {len(self.__alive_trees)} arbres.")
        
        # Remplir le set des cases vides
        for y in range(height):
            for x in range(width):
                if (x, y) not in self.__alive_trees:
                    self.__no_trees.add((x, y))

    def add_tree(self, x: int, y: int) -> None:
        """
        Ajoute un arbre à la position x, y.
        """
        self.__alive_trees.add((x, y))
        # On assigne une nuance de vert aléatoire à cet arbre (entre 0 et 3)
        self.__tree_shades[(x, y)] = random.randint(0, 2)  # noqa: S311

    def save_to_file(self, filename: str) -> None:
        """
        Sauvegarde la grille dans un fichier texte.
        """
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

    # --- RENDU GRAPHIQUE 3D REFACTORISÉ ---
    def draw(self, screen: Any, cell_size: int) -> None:
        """
        Dessine la grille sur l'écran en utilisant les classes Block.
        """
        BG_COLOR = (30, 25, 25) # Sol très foncé
        screen.fill(BG_COLOR)

        # DESSIN ARBRES
        for (x, y) in self.__alive_trees:
            shade_index = self.__tree_shades.get((x, y), 0)
            tree = TreeBlock(x, y, cell_size, shade_index)
            tree.draw(screen)

        # DESSIN FEU
        for (x, y) in self.__burning_trees:
            fire = FireBlock(x, y, cell_size)
            fire.draw(screen)

    # EVOLUTION (Logique standard)
    def evolve(self, args: Namespace) -> None:
        """
        Calcule l'étape suivante.
        """
        new_burning_trees = set()
        new_alive_trees = set()
        new_no_trees = set()

        # Pousse
        for (x, y) in self.__no_trees:
            if random.random() < args.tree_probability:  # noqa: S311
                self.add_tree(x, y) # On utilise add_tree pour donner une couleur
                new_alive_trees.add((x, y))
            else:
                new_no_trees.add((x, y))
        
        # Feu spontané
        for (x, y) in self.__alive_trees:
            if random.random() < args.fire_probability:  # noqa: S311
                new_burning_trees.add((x, y))
            else:
                new_alive_trees.add((x, y))
        
        # Propagation
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
                        
        # Nettoyage
        new_alive_trees = new_alive_trees - new_burning_trees
        
        # Mise à jour des sets
        self.__burning_trees = new_burning_trees
        self.__alive_trees = new_alive_trees
        self.__no_trees = new_no_trees
        
        # IMPORTANT : Mettre à jour le dictionnaire des couleurs
        # On garde les couleurs des arbres survivants, on jette les autres
        new_shades = {}
        for pos in new_alive_trees:
            if pos in self.__tree_shades:
                new_shades[pos] = self.__tree_shades[pos]
            else:
                # Au cas où un arbre apparait sans couleur (ne devrait pas arriver avec add_tree)
                new_shades[pos] = random.randint(0, 2)  # noqa: S311
        self.__tree_shades = new_shades