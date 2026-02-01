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
        print("Lancement du mode GRAPHIQUE 3D. (ECHAP pour quitter)")
        
        pygame.init()
        
        # On vise une grande fenêtre pour bien voir les détails
        TARGET_WINDOW_SIZE = 900 
        cell_size = TARGET_WINDOW_SIZE // args.grid_size
        
        # Ajustement : On veut au moins 10 pixels par case pour voir l'effet 3D
        if cell_size < 10:
            print("ATTENTION: Grille trop dense, l'effet 3D sera désactivé.")
        
        real_window_size = cell_size * args.grid_size 
        
        screen = pygame.display.set_mode((real_window_size, real_window_size))
        pygame.display.set_caption(f"Forest Fire Sim 3D - {args.grid_size}x{args.grid_size}")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            grid.evolve(args)
            grid.draw(screen, cell_size)
            pygame.display.flip()
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

def main() -> None:
    parser = argparse.ArgumentParser(description="Simulation of a forest fire")
    parser.add_argument('-t', '--nbtrees', type=int, default=100)
    parser.add_argument('-s', '--start-grid-output', type=str, default='start_grid.txt')
    parser.add_argument('-o', '--output', type=str, default='final_grid.txt')
    parser.add_argument('-f', '--fire-probability', type=float, default=0.001)
    parser.add_argument('-p', '--tree-probability', type=float, default=0.05)
    
    # J'ai réduit la taille par défaut de la grille à 30 pour que les tuiles soient GROSSES et belles
    parser.add_argument('-N', '--grid-size', type=int, default=30, help='Taille de la grille')
    
    parser.add_argument('-n', '--nb-steps', type=int, default=50)
    parser.add_argument('-x', '--gui', action='store_true', help='Activer mode graphique')
    parser.add_argument('--fps', type=int, default=10, help='Vitesse') # Ralenti un peu pour admirer
    
    args = parser.parse_args()
    start_simulation(args)

if __name__ == "__main__":
    main()