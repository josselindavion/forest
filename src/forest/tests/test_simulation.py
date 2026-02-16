import pytest
from argparse import Namespace
import os
import sys

## Ajout du chemin parent pour importer les modules ##
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from simulation import Grid
except ImportError:
    from forest.simulation import Grid

@pytest.fixture
def args():
    """Fixture qui fournit des arguments de test par défaut."""
    return Namespace(
        nbtrees=10,
        grid_size=10,
        tree_probability=0.5,
        fire_probability=0.5,
        start_grid_output="test_start.txt",
        output="test_final.txt",
        nb_steps=5,
        gui=False,
        fps=60
    )

def test_grid_initialization(args):
    """Vérifie que la grille s'initialise correctement."""
    grid = Grid(10, 10, args)
    ## Vérification via accès privé (autorisé dans les tests via ruff config) ##
    assert len(grid._Grid__alive_trees) == 10
    assert grid._Grid__height == 10

def test_add_tree(args):
    """Vérifie l'ajout manuel d'un arbre."""
    grid = Grid(10, 10, args)
    grid._Grid__alive_trees.clear()
    grid.add_tree(5, 5)
    assert (5, 5) in grid._Grid__alive_trees

def test_save_to_file(args, tmp_path):
    """Vérifie que la sauvegarde fichier fonctionne."""
    ## tmp_path est une fixture pytest qui crée un dossier temporaire auto-nettoyé ##
    file_path = tmp_path / "output_test.txt"
    
    grid = Grid(10, 10, args)
    grid.save_to_file(str(file_path))
    
    assert file_path.exists()
    ## On vérifie qu'il y a bien du contenu ##
    content = file_path.read_text(encoding="utf-8")
    assert len(content) > 0

def test_evolve(args):
    """Vérifie que la simulation avance sans planter."""
    grid = Grid(10, 10, args)
    try:
        grid.evolve(args)
    except Exception as e:
        pytest.fail(f"Evolve a planté : {e}")