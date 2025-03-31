# -*- coding: utf-8 -*-
import os
import shutil
import subprocess

MAIN = "md_worker/main.py"
INPUT_DIR = os.path.dirname(__file__) + "/test_default"

def rmtree(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {e.strerror}")

def rmfile(file_path):
    try:
        os.remove(file_path)
        print(f"File \'{file_path}\' deleted successfully.")
    except FileNotFoundError:
        print(f"File \'{file_path}\' not found.")
    except PermissionError:
        print(f"Permission denied to delete the file \'{file_path}\'.")
    except Exception as e:
        print(f"Error occurred while deleting the file: {e}")

def test_sin_argumentos():
    """Ejecuta el script sin argumentos. No se hace nada."""
    subprocess.run(["python3", MAIN, INPUT_DIR], capture_output=True, text=True)
    assert os.path.exists(INPUT_DIR)
    assert not os.path.exists(INPUT_DIR + "/TOC.md")

def test_copy():
    """Ejecuta el script con --copy con valores. Debe crear una copia del directorio de entrada al directorio de salida, ignorando los directorios y ficheros por defecto."""
    dir_path = "/tmp/copy_TOC"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--copy", dir_path], capture_output=True, text=True)
        assert os.path.exists(dir_path)
        assert not os.path.exists(dir_path + "md_worker/TOC.md")
        assert not os.path.exists(dir_path + "/log.log")
    finally:
        rmtree(dir_path)

def test_copy_default():
    """Ejecuta el script con --copy sin valores. Debe crear una copia del directorio de entrada al directorio de salida por defecto, ignorando los directorios y ficheros por defecto."""
    dir_path = INPUT_DIR + "_copy"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--copy"], capture_output=True, text=True)
        assert os.path.exists(dir_path)
        assert not os.path.exists(dir_path + "md_worker/TOC.md")
        assert not os.path.exists(dir_path + "/log.log")
    finally:
        rmtree(dir_path)

def test_copy_file():
    """Ejecuta el script con --copy con un valor de fichero, esperando un error."""
    result = subprocess.run(["python3", MAIN, INPUT_DIR + "/wiki.md", "--copy"], capture_output=True, text=True)
    assert "error" in result.stderr.lower()

def test_toc():
    """Ejecuta el script con --toc. Debe de generar el fichero TOC.md en la ruta base."""
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--toc"], capture_output=True, text=True)
        assert os.path.isfile(INPUT_DIR + "/TOC.md")
    finally:
        rmfile(INPUT_DIR+"/TOC.md")

def test_toc_path_file():
    """"Ejecuta el script con --toc de un fichero. esperando un error."""
    result = subprocess.run(["python3", MAIN, INPUT_DIR + "wiki.md", "--toc"], capture_output=True, text=True)
    assert not os.path.isfile(INPUT_DIR + "/TOC.md")
    assert "error" in result.stderr.lower()

def test_toc_output():
    """Ejecuta el script con --destination_path con un valor. Debe crear una copia del directorio de entrada al directorio de salida, ignorando los directorios y ficheros por defecto.
    Debe de genearar el fichero TOC.md a la ruta de salida"""
    destination_path = "/tmp/tests_destination_path"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--toc", "--destination_path", destination_path], capture_output=True, text=True)
        assert os.path.isfile(destination_path + "/TOC.md")
    finally:
        rmtree(destination_path)

def test_toc_output_default():
    """Ejecuta el script con --destination_path sin valor. Debe crear una copia del directorio de entrada al directorio de salida por defecto, ignorando los directorios y ficheros por defecto.
    Debe de genearar el fichero TOC.md a la ruta de salida"""
    destination_path = INPUT_DIR + "_output"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--toc", "--destination_path"], capture_output=True, text=True)
        assert os.path.isfile(destination_path + "/TOC.md")
    finally:
        rmtree(destination_path)

def test_toc_output_ignore():
    """Ejecuta el script con --ignaorar sin un valor. Debe crear una copia del directorio de entrada al directorio de salida, ignorando los directorios y ficheros por defecto.
    Debe de genearar el fichero TOC.md a la ruta de salida"""
    destination_path = "/tmp/test_destination_path_files"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--toc", "--destination_path", destination_path, "--ignore"], capture_output=True, text=True)
        assert not os.path.exists(destination_path + "/.ignore_log.log")
        assert os.path.exists(destination_path + "/TOC.md")
    finally:
        rmtree(destination_path)

def test_toc_output_ignore_lista():
    """Ejecuta el script con --ignore con una lista de valores. Debe crear una copia del directorio de entrada al directorio de salida, ignorando los directorios y ficheros por defecto más los indicados.
    Debe de genearar el fichero TOC.md a la ruta de salida"""
    destination_path = "/tmp/test_destination_path_files"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--toc", "--destination_path", destination_path, "--ignore"] + ["guies", "wiki.md"], capture_output=True, text=True)
        assert os.path.exists(destination_path + "/TOC.md")
        assert not os.path.exists(destination_path + "/guies")
        assert not os.path.isfile(destination_path + "/wiki.md")
    finally:
        rmtree(destination_path)

def test_toc_file_output():
    """Ejecuta el script con --toc_files. Debe de recorrer todos los ficheros '.md' y generar el TOC dentro de cada uno de ellos, si ya existe lo sobre escribe."""
    destination_path = "/tmp/test_destination_path_files"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--destination_path", destination_path, "--toc_files"], capture_output=True, text=True)
        assert not os.path.isfile(INPUT_DIR + "/TOC.md")
        assert os.path.isfile(destination_path + "/wiki.md")
        with open(destination_path + "/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert True
    finally:
        rmtree(destination_path)

def test_toc_file_output_default():
    """Ejecuta el script con --toc_files. Debe de recorrer todos los ficheros '.md' y generar el TOC dentro de cada uno de ellos, si ya existe lo sobre escribe."""
    destination_path_files = INPUT_DIR + "_output"
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "--destination_path", "--toc_files"], capture_output=True, text=True)
        assert not os.path.isfile(INPUT_DIR + "/TOC.md")
        assert os.path.isfile(destination_path_files + "/wiki.md")
        with open(destination_path_files + "/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC FIN -->':
                    assert True
    finally:
        rmtree(destination_path_files)

def test_rm_toc_file_from_file():
    """Ejecuta el script con --rm_toc_files. Debe de recorrer todos los ficheros '.md' y eleminar el TOC dentro de cada uno de ellos."""
    with open(INPUT_DIR + "/wiki.md") as archivo:
        for line in archivo:
            if line == '<!-- TOC START -->':
                assert True
    subprocess.run(["python3", MAIN, INPUT_DIR, "--rm_toc_files"], capture_output=True, text=True)
    assert not os.path.isfile(INPUT_DIR + "/TOC.md")
    with open(INPUT_DIR + "/wiki.md") as archivo:
        for line in archivo:
            if line == '<!-- TOC START -->':
                assert False

def test_toc_file():
    """Ejecuta el script con --toc_files. Debe de recorrer todos los ficheros '.md' y generar el TOC dentro de cada uno de ellos, si ya existe lo sobre escribe."""
    subprocess.run(["python3", MAIN, INPUT_DIR, "--toc_files"], capture_output=True, text=True)
    assert not os.path.isfile(INPUT_DIR + "/TOC.md")
    with open(INPUT_DIR + "/wiki.md") as archivo:
        for line in archivo:
            if line == '<!-- TOC START -->':
                assert True

def test_rm_toc_file_destination_path():
    """Ejecuta el script con --rm_toc_files. Debe de recorrer todos los ficheros '.md' y eleminar el TOC dentro de cada uno de ellos."""
    destination_path = INPUT_DIR + "_output"
    try:
        assert not os.path.isfile(destination_path + "/TOC.md")
        with open(INPUT_DIR + "/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert True
        subprocess.run(["python3", MAIN, INPUT_DIR, "--destination_path", destination_path, "-rtf"], capture_output=True, text=True)
        assert not os.path.isfile(destination_path + "/TOC.md")
        with open(destination_path + "/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert False
        with open(INPUT_DIR + "/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert True
    finally:
        rmtree(destination_path)

def test_rm_toc_file_destination_path_file():
    """Ejecuta el script con --rm_toc_files. Debe de recorrer todos los ficheros '.md' y eleminar el TOC dentro de cada uno de ellos."""
    try:
        subprocess.run(["python3", MAIN, INPUT_DIR, "-c"], capture_output=True, text=True)
        with open(INPUT_DIR + "_copy/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert True
        subprocess.run(["python3", MAIN, INPUT_DIR + "_copy/wiki.md", "-rtf"], capture_output=True, text=True)
        with open(INPUT_DIR + "_copy/wiki.md") as archivo:
            for line in archivo:
                if line == '<!-- TOC START -->':
                    assert False
    finally:
        rmtree(INPUT_DIR + "_copy")

# TODO : SORT
# def test_sort_files_dir():
#     """Ejecuta el script con --sort. Debe de recorrer todos los ficheros '.md' en busca de la cabecera de 'ordern' y ordenar el TOC por niveles según este indicado."""
#     subprocess.run(["python3", MAIN, INPUT_DIR, "--sort"], capture_output=True, text=True)
#     rmtree(INPUT_DIR)
#     subprocess.run(["python3", MAIN, INPUT_DIR + "_base", "-c", INPUT_DIR], capture_output=True, text=True)
#
# def test_sort_files_dir_defautl():
#     """Ejecuta el script con --sort. Debe de recorrer todos los ficheros '.md' del directorio --output y buscar enla cabecera el 'ordern' y ordenar el TOC por niveles según este indicado."""
#     subprocess.run(["python3", MAIN, INPUT_DIR, "-o", "--sort"], capture_output=True, text=True)
#     rmtree(INPUT_DIR + "_output")
#
# def test_sort_file():
#     """Ejecuta el script con --sort. Debe de busca en el fichero '.md' la cabecera de 'ordern' y ordenar el TOC por niveles según este indicado."""
#     path_file = INPUT_DIR + "wiki.md"
#     subprocess.run(["python3", MAIN, path_file, "--hmtl"], capture_output=True, text=True)
#     rmfile(path_file)

# TODO : HTML
# def check_md_html(path_dir):
#     have_toc, have_ul_li_link, have_h1_internal_link = False, False, False
#     with open(path_dir + "/wiki.html") as archivo:
#         for line in archivo:
#             if line == '<!-- TOC START -->':
#                 have_toc = True
#             if line == '<li><a href="#wiki">WIKI</a></li>':
#                 have_ul_li_link = True
#             if line == '<h1 id="wiki">WIKI</h1>':
#                 have_h1_internal_link = True
#     assert have_toc and have_ul_li_link and have_h1_internal_link
#
# def test_md_html_dir():
#     path_dir = INPUT_DIR + "_md_html"
#     """Ejecuta el script con --html. Debe hacer una copia del contenido en la ruta especificada y recorrer todos los ficheros '.md' y convertir el contenido a html."""
#     subprocess.run(["python3", MAIN, INPUT_DIR, "--html", path_dir], capture_output=True, text=True)
#     assert os.path.isdir(path_dir)
#     assert os.path.isfile(path_dir + "/wiki.html")
#     check_md_html(path_dir)
#     rmtree(path_dir)
#
# def test_md_html_dir_default():
#     """Ejecuta el script con --html. Debe hacer una copia del directorio con un nombre por defecto y recorrer todos los ficheros '.md' y convertir el contenido a html."""
#     path_dir = INPUT_DIR + "_html"
#     subprocess.run(["python3", MAIN, INPUT_DIR, "--html"], capture_output=True, text=True)
#     assert os.path.isdir(path_dir)
#     assert os.path.isfile(path_dir + "/wiki.html")
#     check_md_html(path_dir)
#     rmtree(path_dir)

# def test_md_html_toc_files_output():
#     """Ejecuta el script con --html. Debe hacer una copia del directorio con un nombre por defecto y recorrer todos los ficheros '.md' y convertir el contenido a html."""
#     path_dir = INPUT_DIR + "_html"
#     subprocess.run(["python3", MAIN, INPUT_DIR, "--html", "-o", "-tf"], capture_output=True, text=True)
#     assert os.path.isdir(path_dir)
#     assert os.path.isfile(path_dir + "/wiki.html")
#     check_md_html(path_dir)
#     rmtree(path_dir)

# def test_md_html_file():
#     """Ejecuta el script con --html. Debe hacer una copia del fichero '.md' en una ruta por defecto y convertir el contenido a html."""
#     path_file = INPUT_DIR + "/wiki.md"
#     result = subprocess.run(["python3", MAIN, path_file, "--html"], capture_output=True, text=True)
#     assert "error" in result.stderr.lower()
