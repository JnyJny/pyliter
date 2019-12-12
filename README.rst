pyliter - Python syntax highlighting
===================================

``pyliter`` is a Python 3 command-line tool that generates ANSI
escape code annotated files from python source. 


Features
--------

- syntax highlighting

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
     ANSI escape code annotated source to OUTPUT_FILE. The display attributes
     of various code elements can be styled by supplying a YAML file. Use the
     --dump-style option to view the default style.
   
   Options:
     -s, --style-file PATH
     -S, --dump-style
     --help                 Show this message and exit.

 
