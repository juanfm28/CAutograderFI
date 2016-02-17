# -*- coding: utf-8 -*-

#Modulo de asserts
from os.path import isfile
from subprocess import Popen,PIPE

def runAllTests(testFile):
    programNames = getProgramNames(testFile)
    for program in programNames:
    	compileSource(program+".c")
    	testProgram(testFile,program)

def testProgram(testFile,programName):
    print("Evaluando: ",programName)
    cmds = getTestsByProgram(testFile,programName)
    solutions = getSolutionsByProgram(testFile,programName)
    possiblePoints = len(cmds)
    pointsObtained = 0
    for cmd,solution in zip(cmds,solutions):
        output = runCommand(cmd).rstrip().lstrip().replace("\x00","").replace('\n','')
        editedOutput = [value for value in output.split(' ') if value != '']
        editedSolution = [value for value in solution.split(' ') if value != '']
        if editedOutput == editedSolution:
            print(cmd,": ",output," Correcto")
            pointsObtained += 1
        else:
            print(cmd,": \n",output," \nIncorrecto. El resultado esperado era: \n",solution)
    print("\nCalificacion de ",programName, ": ",pointsObtained,'/',possiblePoints)
    print("****************************")
    return (pointsObtained*1.0)/(possiblePoints*1.0)

def runCommand(cmd='echo "Hola mundo"'):
    proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if err:
        print("Ocurrio un error o warning: ")
        return err.decode('ascii')
    else:
        return out.decode('ascii')

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

def getTestsByProgram(testFile,programName):
    flag = False
    cmd = []
    try:
        test = open(testFile,'r')
    except FileNotFoundError:
        print("Archivo de pruebas no encontrado: ",testFile)

    for line in test:
        line = line.replace('\n','');
        if line.startswith('##'):
            if flag: break
            program = line.replace('##','')
            if program == programName:
                flag = True
        elif line != '' and flag:
            cmd.append(line)
    test.close()
    if not cmd:
        print("Error: No existe el programa: ",programName)
    return cmd

def getSolutionsByProgram(testFile,programName):
    flag = False
    solutions = []
    try:
        test = open(testFile.replace(".test",".solution"),'r')
    except FileNotFoundError:
        print("Archivo de soluciones no encontrado: ",testFile)

    for line in test:
        line = line.replace('\n','');
        if line.startswith('##'):
            if flag: break
            program = line.replace('##','')
            if program == programName:
                flag = True
        elif line != '' and flag:
            solutions.append(line)
    test.close()
    if not solutions:
        print("Error: No existe ese programa en el archivo de solucion",programName)
    return solutions

def compileSource(sourcefile):
    """Funcion que se encarga de ejecutar el compilador gcc sobre un archivo fuente"""
    if not isfile(sourcefile):
        print("Codigo fuente no encontrado: ",sourcefile)
    else:
        cmd = 'gcc -o '+sourcefile.replace('.c','.x')+' '+sourcefile
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if proc.returncode == 0:
            print("Programa compilado con exito: ",sourcefile)
        else:
            print("Falló la compilación del programa: "+sourcefile+"\nErrores: ")
            print(err.rstrip().decode('utf-8'))
    return True