'''
Author: Minh Nguyen
Date: Sep 2023

This Python script minifies all .py files and compiles them to binary files (.so) recursively.
All .c and compiled .py files will be deleted automatically upon compilation.

Run: 
pip3 install cython python-minifier
python3 compile_to_binary.py build_ext --inplace
'''

import os
import time
import python_minifier

from setuptools import Extension, setup
from Cython.Build import cythonize


def compile_to_binary():

    def minify_code(py_file):
        if not py_file.endswith('.py') or 'venv' in py_file:
            return

        filepath = os.path.splitext(py_file)[0]
        filename = os.path.basename(filepath)

        # Some minified files cannot be compiled to binary due to syntax errors
        ignore = ['admin', 'test_api', 'choices', 'serializers']
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

    def compile_to_so(py_file):
        if not py_file.endswith('.py') or 'venv' in py_file:
            return

        filepath = os.path.splitext(py_file)[0]
        filename = os.path.basename(filepath)

        # Some files should not be compiled to binary
        ignore = ['compile', '__init__', 'main', 'manage',
                  'routes', 'models', 'admin_urls', 'client_urls']
        if filename[0].isdigit() or filename in ignore:
            return

        try:
            # Create a .pyx file from the .py file
            pyx_file = filepath + '.pyx'
            os.rename(py_file, pyx_file)

            # Make sure the output binary file will be in the same dir as its original .pyx file
            relative_path = os.path.relpath(pyx_file, '.')
            module_name = os.path.splitext(
                relative_path.replace(os.sep, '.'))[0]

            # Use Cython to convert .pyx to .c and then compile to .so
            setup(
                ext_modules=cythonize(
                    [Extension(module_name, [pyx_file])], language_level=3),
            )

        except FileNotFoundError:
            print(f'File not found: {py_file}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    # Start compilation
    start_time = time.time()
    current_dir = os.getcwd()

    # Minify and compile code recursively
    for root, _, files in os.walk(current_dir):
        for file in files:
            source_file = os.path.join(root, file)
            minify_code(source_file)
            compile_to_so(source_file)

    # Remove .c and .pyx files recursively
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.pyx') or any(substr in file for substr in ['compile_to_binary', 'migrate_to_vault', 'minify']):
                source_file = os.path.join(root, file)
                os.remove(source_file)

    print('Execution time: ', round(
        (time.time() - start_time)/60, 2), ' minutes')


if __name__ == '__main__':
    compile_to_binary()
