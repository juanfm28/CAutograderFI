# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
import tester

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Archivo de donde vienen las preguntas
parser.add_argument('-t','--tests',action='store')
parser.add_argument('-p','--program',action='store')
parser.add_argument('-d','--directory',action='store')
#Parseo de las opciones
args = parser.parse_args()

if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

testDirectory = './'

if args.directory:
    testDirectory = args.directory

testFile = testDirectory+args.tests

if args.program: 
    programs = args.program.split(',')
    for program in programs:
        tester.testProgram(testFile,program)
else:
    tester.runAllTests(testFile)