# -*- coding: utf-8 -*-

#Programa principal que realiza el testing de un programa
import argparse
import tester

parser = argparse.ArgumentParser(description='Selecciona las opciones de entrada')
#Archivo de donde vienen las preguntas
parser.add_argument('-t','--tests',action='store')
#Parseo de las opciones
args = parser.parse_args()

if not args.tests:
    print("Se requiere un archivo de pruebas")
    exit()

testFile = args.tests

tester.runAllTests(testFile)