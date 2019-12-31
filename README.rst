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
   Usage: pyliter [OPTIONS] [INPUT_FILE]
   
     Python syntax highlighting
   
     Renders syntax-highlighted text to PNG file and optional previews the
     render in a window before saving.
   
     If the optional output path is omitted, preview is enabled.
   
   Options:
     -o, --output-file PATH    Creates a PNG with the supplied path.
     -l, --start-line INTEGER  Line number to begin display.  [default: 0]
     -n, --line-count INTEGER  Number of lines to display.  [default: 10]
     -N, --no-line-numbers     Disable line numbers in output.  [default: False]
     -p, --preview             Previews output in window.  [default: False]
     -t, --transparent         Write output PNG with transparency.  [default:
                               False]
     -s, --style-name TEXT     Style to apply to input file.  [default: default]
     -f, --font-name TEXT      Font name.  [default: courier]
     -S, --font-size INTEGER   Font size  [default: 24]
     -L, --list-styles         List available styles and exits.
     --version                 Show the version and exit.
     --help                    Show this message and exit.


Example
-------

.. image:: https://github.com/JnyJny/pyliter/blob/master/examples/screenshot.png
	   :width: 400
	   :alt: Super Awesome PNG Screenshot

 
