# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
from tester import Tester
import os

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Archivo de donde vienen las preguntas
parser.add_argument('-t','--tests',action='store')
#Bandera -p: indica si se quiere probar solo algunos de los programas existentes en el archivo
parser.add_argument('-p','--program',action='store')
#Bandera -d: Indica el directorio donde está el archivo de pruebas y otros archivos necesarios para la prueba
parser.add_argument('-d','--directory',action='store')
#Bandera -d: indica el directorio donde están todos los directorios de cada persona/equipo por calificar
parser.add_argument('-g','--groupdir',action='store')
#Bandera -l: indica todas las bibliotecas propias necesarias para el programa. Se asume que están junto con el codigo fuente
#parser.add_argument('-l','--libraries',action='store')
#Parseo de las opciones
args = parser.parse_args()

#Si no se indica un archivo de pruebas, no se puede hacer nada
if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

#Por default, se asumira que el directorio de pruebas es ./
testDirectory = './'

#Si se le indico uno diferente, se cambia
if args.directory:
    testDirectory = args.directory

#Si se le indico uno diferente, se cambia
if args.groupdir:
    groupDirectory = args.groupdir

#Si no se indica el directorio del grupo, tampoco se puede hacer nada con este programa
else:
	print("Se requiere un directorio del grupo")
	exit()

#Si se le indicaron librerias, se crea una lista separandolas con las comas como referencia
#if args.libraries:
#    libraries = args.libraries.split(',')

#Se construye el objeto Tester
#tester = Tester(args.tests,testDir = testDirectory,libraries = libraries)
tester = Tester(args.tests,testDir = testDirectory)

#Por cada directorio en el directorio del grupo
for folder in os.listdir(groupDirectory):
    #Se construye el path del directorio del equipo por calificar
    path = groupDirectory+folder+'/'
    #Se verifica que dicho path sea realmente un directorio
    if os.path.isdir(path):
        #Separador e indicación de a quien se está evaluando
        print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        print("Evaluando a: ",folder)
        #Al objeto tester se le indica que el codigo fuente que tiene que evaluar esta en el path del directorio del equipo
        tester.setSourceCodeDir(path)
        #Si se indicaron algunos programas
        if args.program: 
            #Se saca una lista de ellos, esperando que estén separados por ,
            programs = args.program.split(',')
            
            #Se prueba cada programa 
            for program in programs:
                tester.testProgram(program)
        #Si no se indicaron programas se asume que se quieren correr todas las pruebas.
        else:
            tester.runAllTests()

