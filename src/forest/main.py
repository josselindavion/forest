## IMPORTATIONS ##
import argparse
import sys

## IMPORTATIONS INTERNES ##
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
        print("Lancement du mode GRAPHIQUE. (ECHAP pour quitter)")
        
        pygame.init()
        
        # Configuration fenêtre
        WINDOW_SIZE = 900 # Un peu plus grand pour profiter des graphismes
        cell_size = WINDOW_SIZE // args.grid_size
        real_window_size = cell_size * args.grid_size 
        
        screen = pygame.display.set_mode((real_window_size, real_window_size))
        pygame.display.set_caption(f"Forest Fire Sim - {args.grid_size}x{args.grid_size}")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Gestion des inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Logique
            grid.evolve(args)
            
            # Affichage
            grid.draw(screen, cell_size)
            pygame.display.flip()
            
            # FPS
            clock.tick(args.fps)
            
        pygame.quit()
        print("Simulation graphique terminée.")

    ## MODE TEXTE ##
    else:
        print(f"Lancement simulation textuelle ({args.nb_steps} étapes)...")
        for i in range(args.nb_steps):
            grid.evolve(args)
            if i % 10 == 0:
                print(f"Étape {i}/{args.nb_steps}")
                
    grid.save_to_file(args.output)
    print(f"Sauvegarde finale : {args.output}")


## FONCTION PRINCIPALE ##
def main() -> None:
    parser = argparse.ArgumentParser(description="Simulation of a forest fire")

    parser.add_argument('-t', '--nbtrees', type=int, default=100, help='Start trees.')
    parser.add_argument('-s', '--start-grid-output', type=str, default='start_grid.txt')
    parser.add_argument('-o', '--output', type=str, default='final_grid.txt')
    parser.add_argument('-f', '--fire-probability', type=float, default=0.01)
    parser.add_argument('-p', '--tree-probability', type=float, default=0.05)
    parser.add_argument('-N', '--grid-size', type=int, default=50) # Mis à 50 par défaut pour bien voir les cases
    parser.add_argument('-n', '--nb-steps', type=int, default=50)
    parser.add_argument('-x', '--gui', action='store_true', help='Enable GUI.')
    parser.add_argument('--fps', type=int, default=15, help='GUI speed.')
    
    args = parser.parse_args()
    start_simulation(args)
