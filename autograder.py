# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
from tester import Tester

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Bandera -t: indica el nombre del archivo donde están los tests
parser.add_argument('-t','--tests',action='store')
#Bandera -p: indica si se quiere probar solo algunos de los programas existentes en el archivo
parser.add_argument('-p','--program',action='store')
#Bandera -d: Indica el directorio donde está el archivo de pruebas y otros archivos necesarios para la prueba
parser.add_argument('-d','--directory',action='store')
#Bandera -s: indica el directorio donde está el archivo de codigo fuente por calificar
parser.add_argument('-s','--sourcedir',action='store')
#Parseo de las opciones
args = parser.parse_args()

#Si no se indica un archivo de pruebas, no se puede hacer nada
if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

#Por default, se asumira que el directorio de pruebas y el directorio de codigo fuente es ./
testDirectory = './'
sourceDirectory = './'
#Si se le indico uno diferente, se cambia
if args.directory:
    testDirectory = args.directory
#Si se le indicó uno diferente se cambia
if args.sourcedir:
    sourceDirectory = args.sourcedir

#Se construye el objeto Tester
tester = Tester(args.tests,sourceDirectory,testDirectory)

#Si se indicaron algunos programas
if args.program: 
	#Se saca una lista de ellos, esperando que estén separados por ,
    programs = args.program.split(',')
    #Por cada programa en la lista indicada se prueba ese programa
    for program in programs:
        tester.testProgram(program)
#Si no se indicaron programas, se asume que se quieren ejecutar todas las pruebas
else:
    tester.runAllTests()