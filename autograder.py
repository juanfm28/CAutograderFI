# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
from tester import Tester

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Archivo de donde vienen las preguntas
parser.add_argument('-t','--tests',action='store')
parser.add_argument('-p','--program',action='store')
parser.add_argument('-d','--directory',action='store')
parser.add_argument('-s','--sourcedir',action='store')
#Parseo de las opciones
args = parser.parse_args()

if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

testDirectory = './'
sourceDirectory = './'

if args.directory:
    testDirectory = args.directory

if args.sourcedir:
    sourceDirectory = args.sourcedir

tester = Tester(args.tests,sourceDirectory,testDirectory)

if args.program: 
    programs = args.program.split(',')
    for program in programs:
        tester.testProgram(program)
else:
    tester.runAllTests()