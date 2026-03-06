"""Tests pour le module de simulation (Grid)."""

from argparse import Namespace

import pytest

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
        fps=60,
    )


def test_grid_initialization(args):
    """Vérifie que la grille s'initialise correctement."""
    grid_height = 10
    grid_width = 10
    expected_trees = 10
    
    grid = Grid(grid_height, grid_width, args)
    
    # Vérification via accès privé (autorisé dans les tests via ruff config)
    assert len(grid._Grid__alive_trees) == expected_trees
    assert grid._Grid__height == grid_height


def test_add_tree(args):
    """Vérifie l'ajout manuel d'un arbre."""
    grid = Grid(10, 10, args)
    grid._Grid__alive_trees.clear()
    
    test_x = 5
    test_y = 5
    grid.add_tree(test_x, test_y)
    
    assert (test_x, test_y) in grid._Grid__alive_trees


def test_save_to_file(args, tmp_path):
    """Vérifie que la sauvegarde fichier fonctionne."""
    # tmp_path est une fixture pytest qui crée un dossier temporaire auto-nettoyé
    file_path = tmp_path / "output_test.txt"

    grid = Grid(10, 10, args)
    grid.save_to_file(str(file_path))

    assert file_path.exists()
    # On vérifie qu'il y a bien du contenu
    content = file_path.read_text(encoding="utf-8")
    assert len(content) > 0


def test_evolve(args):
    """Vérifie que la simulation avance sans planter."""
    grid = Grid(10, 10, args)
    # Si evolve lève une erreur, pytest fera échouer le test automatiquement
    grid.evolve(args)