## IMPORTATIONS ##
import argparse
import sys

## IMPORTATIONS INTERNES ##
# Note: assure-toi que l'import fonctionne selon ton dossier. 
# Si tes fichiers sont côte à côte, utilise : from simulation import Grid
try:
    from .simulation import Grid
except ImportError:
    from simulation import Grid 

def start_simulation(args):
    grid = Grid(args.grid_size, args.grid_size, args)
    grid.save_to_file(args.start_grid_output)
    
    print("État initial sauvegardé.")

    ## MODE GRAPHIQUE ##
    if args.gui:
        import pygame
        print("Lancement du mode GRAPHIQUE. Appuyez sur ECHAP ou fermez la fenêtre pour quitter.")
        
        ## Initialisation Pygame ##
        pygame.init()
        
        ## Calcul de la taille de la fenêtre ##
        WINDOW_SIZE = 800
        cell_size = WINDOW_SIZE // args.grid_size
        ## On recalcule la taille réelle pour éviter les pixels coupés ##
        real_window_size = cell_size * args.grid_size 
        
        screen = pygame.display.set_mode((real_window_size, real_window_size))
        pygame.display.set_caption("Simulation Feu de Forêt")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            ## Boucle principale ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            

            grid.evolve(args)
            
            ## Affichage ##
            grid.draw(screen, cell_size)
            pygame.display.flip()
            
            ## Limitation de la vitesse ##
            clock.tick(args.fps)
            
        pygame.quit()
        print("Simulation graphique terminée.")

    ## MODE TEXTE ##
    else:
        print(f"Lancement de la simulation textuelle pour {args.nb_steps} étapes...")
        for i in range(args.nb_steps):
            grid.evolve(args)
            ## Barre de progression simple ##
            if i % 10 == 0:
                print(f"Étape {i}/{args.nb_steps}")
                
    grid.save_to_file(args.output)
    print(f"Sauvegarde du résultat final dans : {args.output}")


## FONCTION PRINCIPALE ##
def main() -> None:
    
    ## Création du parser ##
    parser = argparse.ArgumentParser(description="Simulation of a forest fire")

    ## Ajouts des arguments ##
    parser.add_argument('-t', '--nbtrees', type=int, default=100,
                        help='Number of random trees at start.')
    parser.add_argument('-s', '--start-grid-output', type=str, default='start_grid.txt',
                        help='Output file for starting grid.')
    parser.add_argument('-o', '--output', type=str, default='final_grid.txt',
                        help='Output file for final grid.')
    parser.add_argument('-f', '--fire-probability', type=float, default=0.01,
                        help='Probability a tree ignites alone.')
    parser.add_argument('-p', '--tree-probability', type=float, default=0.05,
                        help='Probability an empty space grows a tree.')
    parser.add_argument('-N', '--grid-size', type=int, default=100,
                        help='Side length of the square grid.')
    parser.add_argument('-n', '--nb-steps', type=int, default=50,
                        help='Number of steps (text mode only).')
    
    ## L'argument qui active le mode graphique ##
    parser.add_argument('-x', '--gui', action='store_true',
                        help='Enable graphical display.')
    parser.add_argument('--fps', type=int, default=10,
                        help='Frames per second for GUI.')
    
    ## Récupération des arguments ##
    args = parser.parse_args()

    ## Lancement de la simulation ##
    start_simulation(args)

if __name__ == "__main__":
    main()