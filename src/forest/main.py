## IMPORTATIONS ##
import argparse

## IMPORTATIONS INTERNES ##
from simulation import start_simulation

## FONCTION PRINCIPALE ##
def main() -> None:
    
    ## Création du parser ##
    parser = argparse.ArgumentParser(description="Simulation of a forest fire")

    ## Ajouts des arguments ##
    parser.add_argument('-t', '--nbtrees', type=int, default=100,
                        help='The number of random trees to randomly generate at start. Default value: 100.')
    parser.add_argument('-s', '--start-grid-output', type=str, default='start_grid.txt',
                        help='The file in which to write the starting grid. Default value: start_grid.txt.')
    parser.add_argument('-o', '--output', type=str, default='final_grid.txt',
                        help='The file in which to write the final grid. Default value: final_grid.txt.')
    parser.add_argument('-f', '--fire-probability', type=float, default=0.05,
                        help='A value between 0.0 and 1.0 representing the probability a tree has to ignite alone.')
    parser.add_argument('-p', '--tree-probability', type=float, default=0.3,
                        help='A value between 0.0 and 1.0 representing the probability a empty space has to be filled with a tree.')
    parser.add_argument('-N', '--grid-size', type=int, default=50,
                        help='The side’s length of the square grid.')
    parser.add_argument('-n', '--nb-steps', type=int, default=10,
                        help='The number of steps to run. This value must be set to a value > 0 when GUI is disabled.')
    parser.add_argument('-x', '--gui', action='store_true',
                        help='Enable graphical display. In that case the -n option is not used.')
    parser.add_argument('--fps', type=int, default=30,
                        help='The number of frame per seconds for the GUI.')
    
    ## Récupération des arguments ##
    args = parser.parse_args()

    ## Lancement de la simulation ##
    start_simulation(args)