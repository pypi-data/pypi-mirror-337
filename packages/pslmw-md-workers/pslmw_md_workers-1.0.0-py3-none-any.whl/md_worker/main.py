# -*- coding: utf-8 -*-
import os
import argparse

from pslmw_md_toc_files_plus import MdTOCFilesPlus

def set_default_value(value, ruta_base, default='default'):
    normal_path = os.path.basename(os.path.normpath(ruta_base))
    dir_path = os.path.normpath(ruta_base).replace(normal_path, "")
    new_path = dir_path + normal_path + default
    if value is not None:
        value = value[0] if value else new_path
    return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar TOC para archivos Markdown.")

    # Args obligatorio :str
    parser.add_argument(
        "input_dir",
        type=str,
        help="Ruta del directorio de entrada."
    )

    # Args opcional :boolean
    parser.add_argument(
        "-t",
        "--toc",
        action="store_true",
        help="Generar TOC del directorio de entrada."
             "Si le pasamos una ruta. Genera una copia de todos los ficheros y trabaja sobre este directorio.\n"
             "No copiará los directorios archivos ignorados."
    )
    parser.add_argument(
        "-tf",
        "--toc_files",
        action="store_true",
        help="Generar TOC por cada fichero markdown que encuentra dentro de la ruta de entrada."
    )
    parser.add_argument(
        "-rtf",
        "--rm_toc_files",
        action="store_true",
        help="Elimina TOC por cada fichero markdown que encuentra dentro de la ruta de entrada."
    )
    parser.add_argument(
        "-ts",
        "--toc_sort",
        action="store_true",
        help="Ordena los ficheros '.md' con cabecera '...(order:asc|desc)...'."
    )

    # Args opcions :list
    parser.add_argument(
        "-i",
        "--ignore",
        nargs='*',
        default=[],
        help="Lista de directorios (Sin ruta absoluta) a ignorar (separados por espacios)."
    )

    # Args opcional :(None/list).
    # Estos argumentos pueden:
    #   No ester definidos.
    #   Declararse vacios: en cual caso se le assignará un valor por defecto a posteriori.
    #   Declararse con un valor: Este vendra en formato lista, en ese caso solo usaremos el primer elemento.
    parser.add_argument(
        "-dp",
        "--destination_path",
        type=str,
        nargs='*',
        default=None,
        help="Genera una copia de todos los ficheros a la ruta destino especificada o por defector '_output' y trabaja sobre este directorio."
    )
    parser.add_argument(
        "--html",
        type=str,
        nargs='*',
        default=None,
        help="Genera una copia de todos los ficheros a la ruta destino especificada o por defector '_html' y trabaja sobre este directorio.\n"
             "Convierte los archivos .md en ficheros HTML indicando."
    )
    parser.add_argument(
        "-c",
        "--copy",
        type=str,
        nargs='*',
        default=None,
        help="Genera una copia de todos los ficheros a la ruta destino especificada o por defector '_copy'.\n"
             "No copiará los directorios archivos ignorados."
    )

    args = parser.parse_args()

    # Obtenemos los directorios raíz [OBLIGATORIO]
    input_dir = args.input_dir

    # Set los posibles argumentos que pueden no estar, estar vacios o llegar con un parametro (List) obteniendo su primer valor
    copy = set_default_value(args.copy,
                             ruta_base=input_dir,
                             default='_copy')
    destination_path = set_default_value(args.destination_path,
                                   ruta_base=input_dir,
                                   default='_output')
    html = set_default_value(args.html,
                             ruta_base=input_dir,
                             default='_html')

    # Obtenemos los parametros para las acciones a realizar. Campos boleanos
    toc = args.toc # Directorios o archivos a ignorar
    ignore = args.ignore # Directorios o archivos a ignorar
    toc_files = args.toc_files # Genera el TOC en cada archivo .md
    rm_toc_files = args.rm_toc_files # Eleminar el TOC en cada archivo .md
    toc_sort = args.toc_sort # Ordena el contenido del los archivos .md con cabecera `...(order:asc|desc)...`

    generador = MdTOCFilesPlus(input_dir)

    # Make copy.
    if copy:
        make_copy = MdTOCFilesPlus(input_dir, destination_path=copy, ignore=ignore)

    if toc_sort:
        pass

    if toc:
        # Generamos el TOC sobre la ruta base o sobre la ruta output si este parametro se ha proporcionado.
        generador.set_ignore(ignore=ignore)
        generador.set_destination_path(destination_path)
        generador.create_toc()

    if toc_files or rm_toc_files:
        if not toc:
            generador.set_ignore(ignore=ignore)
            generador.set_destination_path(destination_path)

        # Si se quiere realizar un TOC en cada uno de los ficheros .md
        generador.set_toc_files(toc_files)
        generador.set_rm_toc_files(rm_toc_files)
        generador.process_markdown_files()
