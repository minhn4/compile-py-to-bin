'''
Author: Minh Nguyen
Date: Sep 2023

This Python script minifies all .py files recursively.

Run: 
pip3 install python-minifier
python3 minify.py
'''

import os
import time
import python_minifier

from setuptools import Extension, setup
from Cython.Build import cythonize


def minify_code():

    def minify(py_file):
        if not py_file.endswith('.py') or 'venv' in py_file:
            return

        filepath = os.path.splitext(py_file)[0]
        filename = os.path.basename(filepath)

        # Some minified files cannot be compiled to binary due to syntax errors
        ignore = ['admin', 'test_api', 'choices', 'serializers', 'minify']
        if filename in ignore:
            return

        try:
            print(f'Minifying {py_file}')
            # Read the content of the input file
            with open(py_file, 'r') as f:
                original_code = f.read()

            # Minify code
            minified_code = python_minifier.minify(original_code)

            # Write the minified code back to the input file
            with open(py_file, 'w') as f:
                f.write(minified_code)

        except FileNotFoundError:
            print(f'File not found: {py_file}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    # Start minifying
    start_time = time.time()
    current_dir = os.getcwd()

    # Minify code recursively
    for root, _, files in os.walk(current_dir):
        for file in files:
            source_file = os.path.join(root, file)
            minify(source_file)

    print('Execution time: ', round(
        (time.time() - start_time)/60, 2), ' minutes')


if __name__ == '__main__':
    minify_code()
