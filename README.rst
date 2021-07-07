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
   Usage: pyliter [OPTIONS] COMMAND [ARGS]...
   
   Python syntax highlighting
   
   Options:
     --install-completion  Install completion for the current shell.
     --show-completion     Show completion for the current shell, to copy it or
                           customize the installation.
   
     --help                Show this message and exit.
   
   Commands:
     list    List builtin text styles.
     render  Renders syntax-highlighted text to PNG file or displayed in a...

::

   $ pyliter render --help
   Usage: pyliter render [OPTIONS] INPUT_FILE
   
   Renders syntax-highlighted text to PNG file or displayed in a window.
   
   If the optional output path is omitted, preview is enabled automatically.
   
   Arguments:
     INPUT_FILE  [required]
   
   Options:
     -o, --output PATH
     -s, --start-line INTEGER  [default: 0]
     -L, --line-count INTEGER  [default: 10]
     -N, --no-line-numbers     [default: False]
     -p, --preview             [default: False]
     -t, --transparent         [default: False]
     --style-name TEXT         [default: default]
     --font-name TEXT          [default: courier]
     --font-size INTEGER       [default: 24]
     --help                    Show this message and exit.

Example
-------

.. image:: https://github.com/JnyJny/pyliter/blob/master/examples/screenshot.png
	   :width: 400
	   :alt: Super Awesome PNG Screenshot

 
