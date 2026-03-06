"""Module principal pour lancer la simulation de feu de forêt."""

# IMPORTATIONS
import argparse
import logging
from argparse import Namespace

import pygame

# IMPORTATIONS INTERNES
from .simulation import Grid


# CONFIGURATION DU LOGGING
def setup_logging(*, verbose: bool = False) -> None:
    """Configure le logging."""
    # On récupère le logger racine
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Format : Date - Nom du module - Niveau - Message
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Handler Console : On affiche INFO ou DEBUG selon l'option
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Handler Fichier : On enregistre TOUT (DEBUG)
    file_handler = logging.FileHandler("simulation.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Logger nommé explicitement pour le script principal
logger = logging.getLogger("MAIN")


def start_simulation(args: Namespace) -> None:
    """Lance la simulation."""
    grid = Grid(args.grid_size, args.grid_size, args)
    grid.save_to_file(args.start_grid_output)

    logger.info("État initial sauvegardé.")

    # MODE GRAPHIQUE
    if args.gui:
        logger.info("Lancement du mode GRAPHIQUE 3D. (ECHAP pour quitter)")

        pygame.init()

        # On vise une grande fenêtre pour bien voir les détails
        target_window_size = 900
        cell_size = target_window_size // args.grid_size

        # Ajustement : On veut au moins 10 pixels par case pour voir l'effet 3D
        min_cell_size_for_3d = 10
        if cell_size < min_cell_size_for_3d:
            logger.warning("ATTENTION: Grille trop dense, l'effet 3D sera désactivé.")

        real_window_size = cell_size * args.grid_size

        screen = pygame.display.set_mode((real_window_size, real_window_size))
        pygame.display.set_caption(f"Forest Fire Sim 3D - {args.grid_size}x{args.grid_size}")

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            grid.evolve(args)
            grid.draw(screen, cell_size)
            pygame.display.flip()
            clock.tick(args.fps)

        pygame.quit()
        logger.info("Simulation graphique terminée.")

    # MODE TEXTE
    else:
        logger.info("Lancement simulation textuelle (%d étapes)...", args.nb_steps)
        for i in range(args.nb_steps):
            grid.evolve(args)
            if i % 10 == 0:
                logger.info("Étape %d/%d", i, args.nb_steps)

    grid.save_to_file(args.output)
    logger.info("Sauvegarde finale : %s", args.output)


def main() -> None:
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Simulation of a forest fire")
    parser.add_argument("-t", "--nbtrees", type=int, default=100)
    parser.add_argument("-s", "--start-grid-output", type=str, default="start_grid.txt")
    parser.add_argument("-o", "--output", type=str, default="final_grid.txt")
    parser.add_argument("-f", "--fire-probability", type=float, default=0.001)
    parser.add_argument("-p", "--tree-probability", type=float, default=0.05)

    parser.add_argument("-N", "--grid-size", type=int, default=30, help="Taille de la grille")

    parser.add_argument("-n", "--nb-steps", type=int, default=50)
    parser.add_argument("-x", "--gui", action="store_true", help="Activer mode graphique")
    parser.add_argument("--fps", type=int, default=10, help="Vitesse")

    # NOUVEAU : Ajout de l'argument verbose
    parser.add_argument("-v", "--verbose", action="store_true", help="Activer les logs détaillés (DEBUG)")

    args = parser.parse_args()

    # Initialisation du logging avec le paramètre verbose (obligatoire en mot-clé maintenant)
    setup_logging(verbose=args.verbose)

    start_simulation(args)