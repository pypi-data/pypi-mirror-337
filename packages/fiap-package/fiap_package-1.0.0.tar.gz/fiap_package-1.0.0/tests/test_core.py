import pytest
import sys
import os

# Adiciona o caminho do projeto à lista de caminhos para importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from cursofiap.core import hello_world

def test_hello_world():
    assert hello_world() == "Hello, world!"
