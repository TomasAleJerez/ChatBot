import os
import sys

# 1. AÑADE la carpeta raíz del proyecto al PATH, asumiendo que 'docs/' 
#    está un nivel por debajo de la raíz:
sys.path.insert(0, os.path.abspath('D:/curso python/iita py/ChatBot'))

project = 'ChatBot Inteligente'
author = 'Tomas Ale Jerez'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

language = 'es'
html_theme = 'alabaster'

print("\n--- DEBUG: Ruta configurada en sys.path ---")
print("Ruta absoluta:", os.path.abspath('../..'))
print("¿Existe el directorio 'ChatBot' aquí?:", os.path.exists(os.path.join(os.path.abspath('D:/curso python/iita py/ChatBot'), 'ChatBot')))

