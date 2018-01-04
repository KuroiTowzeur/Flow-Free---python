"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(name="Flow Free",
      version="1",
      description="Adaptation du jeu mobile Flow Free",
      executables=[Executable("main.py")],
      )
