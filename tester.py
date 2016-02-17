# -*- coding: utf-8 -*-

#Modulo de asserts
from os.path import isfile
from subprocess import Popen,PIPE

def runAllTest(testFile):
    programNames = getProgramNames(testFile)
    for program in programNames:
    	compileSource(program+".c")
    	pass

def getProgramNames(testFile):
    names = []
    try:
        test = open(testFile,'r')
    except FileNotFoundError:
        print("Archivo de pruebas no encontrado: ",testFile)

    for line in test:
        line = line.replace('\n','');
        if line != "" and line.startswith('##'):
            names.append(line.replace('##',''))
    test.close()
    return names

def compileSource(sourcefile):
    """Funcion que se encarga de ejecutar el compilador gcc sobre un archivo fuente"""
    if not isfile(sourcefile):
        print("Codigo fuente no encontrado: ",sourcefile)
    else:
        cmd = 'gcc -o '+sourcefile.replace('.c','')+' '+sourcefile
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if proc.returncode == 0:
            print("Programa compilado con exito: ",sourcefile)
        else:
            print("Falló la compilación del programa: "+sourcefile+"\nErrores: ")
            print(err.rstrip().decode('utf-8'))
    return True