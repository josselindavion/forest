import sys
import pytest
from forest.main import main

def test_main_execution(monkeypatch, tmp_path):
    """
    Teste l'exécution complète du programme (main) en simulant des arguments.
    Cela permet de couvrir main.py et le parsing d'arguments.
    """
    ## On crée des chemins de fichiers temporaires pour ne pas polluer ##
    output_start = tmp_path / "start.txt"
    output_final = tmp_path / "final.txt"

    ## On simule les arguments de la ligne de commande (sys.argv) ##
    ## On met nb-steps à 1 pour que ça aille vite ##
    test_args = [
        "forest", 
        "--grid-size", "10", 
        "--nbtrees", "5", 
        "--nb-steps", "1",
        "--start-grid-output", str(output_start),
        "--output", str(output_final)
    ]
    
    ## Monkeypatch remplace sys.argv le temps du test ##
    monkeypatch.setattr(sys, "argv", test_args)

    ## On lance le main, qui va lire nos faux arguments ##
    try:
        main()
    except SystemExit:
        ## argparse peut lever SystemExit, mais ici on attend que ça finisse normalement ##
        pass

    ## Vérifications ##
    assert output_start.exists()
    assert output_final.exists()