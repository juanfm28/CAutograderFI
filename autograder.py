# -*- coding: utf-8 -*-

#Main script
import argparse
from tester import Tester

parser = argparse.ArgumentParser(description='Select the execution flags')
#-t flag: it indicates the name of the file where the test are written
parser.add_argument('-t','--tests',action='store')
#-p flag: it indicates if there is only one program in the file to test.
parser.add_argument('-p','--program',action='store')
#-d flag: it indicates the directory where the test files are stored
parser.add_argument('-d','--directory',action='store')
#-s flag: it indicates the directory where the source code to evaluate is stored
parser.add_argument('-s','--sourcedir',action='store')
#Bandera -l: indica todas las bibliotecas propias necesarias para el programa. Se asume que están junto con el codigo fuente
parser.add_argument('-l','--libraries',action='store')
#-f flag: it indicates if the grader should show the differences between the desired output and the result output
parser.add_argument('-f','--diff',action='store_true')
#Parsing the options
args = parser.parse_args()

#If there are no test files, nothing can be done
if not args.tests:
    print("A test file is required. Aborting")
    exit()

#By default, it is assumed that the test directory and the source code directory is this script's repository
testDirectory = './'
sourceDirectory = './'
libraries = []
#If there is a different directory in the command options, this is changed
if args.directory:
    testDirectory = args.directory
#If there is a different source code directory in the options, it is changed
if args.sourcedir:
    sourceDirectory = args.sourcedir

#Si se le indicaron librerias, se crea una lista separandolas con las comas como referencia
if args.libraries:
	libraries = args.libraries.split(',')

#The Tester instance is built
tester = Tester(args.tests,sourceDirectory,testDirectory,libraries)
#tester = Tester(args.tests,sourceDirectory,testDirectory)

#If the -f flag is active, the Tester object is informed.
if args.diff:
    tester.toggleDiff()

#If only some programs where indicatedSi se indicaron algunos programas
if args.program:
	#A list of them is obtained, expecting they are separated by ','
    programs = args.program.split(',')
    #For each program in the list, the test is run.
    for program in programs:
        tester.testProgram(program)
#If no individual programs are selected, the program assumes all test must be run in order
else:
    tester.runAllTests()
