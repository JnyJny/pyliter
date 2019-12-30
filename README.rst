pyliter - Python syntax highlighting
====================================

``pyliter`` is a Python 3 command-line tool that generates PNG files
from python source. 


Features
--------

- syntax highlighting
- PNG files
- preview mode
- OpenGL rendering using pyglet

Install
-------

::

   $ pip install pyliter


::

   $ pip install git+https://github.com/JnyJny/pyliter


Usage
-----

::

   $ pyliter --help

   Usage: pyliter [OPTIONS] [INPUT_FILE] [OUTPUT_FILE]
   
     Python syntax highlighting
   
     Performs Python syntax highlighting on code found in INPUT_FILE and writes
     color annotated text in PNG format to OUTPUT_FILE.
   
   Options:
     -l, --start-line INTEGER  line to begin displaying
     -n, --line-count INTEGER  number of lines to display
     -p, --preview
     -t, --transparent
     -s, --style-name TEXT
     --list-styles
     --version                 Show the version and exit.
     --help                    Show this message and exit.
      


Example
-------

.. image:: https://github.com/JnyJny/pyliter/blob/master/examples/screenshot.png
	   :width: 400
	   :alt: Super Awesome PNG Screenshot

 
