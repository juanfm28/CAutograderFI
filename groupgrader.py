# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
from tester import Tester
import os

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Archivo de donde vienen las preguntas
parser.add_argument('-t','--tests',action='store')
parser.add_argument('-p','--program',action='store')
parser.add_argument('-d','--directory',action='store')
parser.add_argument('-g','--groupdir',action='store')
#Parseo de las opciones
args = parser.parse_args()

if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

testDirectory = './'
groupDirectory = './'

if args.directory:
    testDirectory = args.directory

if args.groupdir:
    groupDirectory = args.groupdir

else:
	print("Se requiere un directorio del grupo")
	exit()

tester = Tester(args.tests,testDir = testDirectory)

for folder in os.listdir(groupDirectory):
    path = groupDirectory+folder+'/'
    if os.path.isdir(path):
        print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        print("Evaluando a: ",folder)
        tester.setSourceCodeDir(path)
        if args.program: 
            programs = args.program.split(',')
            for program in programs:
                tester.testProgram(program)
        else:
            tester.runAllTests()

