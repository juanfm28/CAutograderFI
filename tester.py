# -*- coding: utf-8 -*-

#Modulo de asserts
from os.path import isfile
from subprocess import Popen,PIPE
from os import remove as rm

class Tester:
    """Clase que controla todos los procesos de prueba"""
    def __init__(self, testFile,sourceCodeDir = './',testDir = './'):
        """Constructor de la clase Tester

        testFile -- Archivo donde estan contenidas las pruebas a pasar
        sourceCodeDir -- Directorio donde estan contenidos los codigos fuente default='./'
        testDir -- Directorio donde estan contenidos los archivos necesarios para las pruebas default='./'
        """
        testFileCore = testFile
        self.sourceCodeDir = sourceCodeDir
        self.testDir = testDir
        self.testFile = self.testDir+testFileCore+'.test'
        self.solutionFile = self.testDir+testFileCore+'.solution'
        self.programNames = self.getProgramNames()

    def setSourceCodeDir(self,sourceCodeDir):
        self.sourceCodeDir = sourceCodeDir

    def runAllTests(self):
        for program in self.programNames:
            self.testProgram(program)

    def testProgram(self,programName):
        print("Evaluando: ",programName)
        success = self.compileSource(programName)
        if not success:
            return
        cmds = self.getTestsByProgram(programName)
        solutions = self.getSolutionsByProgram(programName)
        possiblePoints = len(cmds)
        pointsObtained = 0
        for cmd,solution in zip(cmds,solutions):
            try:
                raw_output = Tester.runCommand(cmd)
            except UnicodeDecodeError:
                print('Salida no reconocible')
                return 0.0
            output = raw_output.rstrip().lstrip().replace("\x00","").replace('\n','').replace('\t',' ')
            editedOutput = [value for value in output.split(' ') if value != '']
            editedSolution = [value for value in solution.split(' ') if value != '']
            #print(editedOutput)
            #print(editedSolution)
            if editedOutput == editedSolution:
                print(cmd,": ",raw_output," Correcto")
                pointsObtained += 1
            else:
                print(cmd,": \n",raw_output," \nIncorrecto. El resultado esperado era: \n",solution)
        print("\nPasados en",programName, ": ",pointsObtained,'/',possiblePoints)
        print("****************************")
        try:
            rm(self.testDir+programName+'.x')
        except FileNotFoundError:
            pass
        return (pointsObtained*1.0)/(possiblePoints*1.0)

    def runCommand(cmd='echo "Hola mundo"'):
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if err:
            print("Ocurrio un error o warning: ")
            return err.decode('utf-8')
        else:
            return out.decode('utf-8')

    def getProgramNames(self):
        names = []
        try:
            test = open(self.testFile,'r')
        except FileNotFoundError:
            print("Archivo de pruebas no encontrado: ",self.testFile)

        for line in test:
            line = line.replace('\n','');
            if line != "" and line.startswith('##'):
                names.append(line.replace('##',''))
        test.close()
        return names

    def getTestsByProgram(self,programName):
        flag = False
        cmd = []
        try:
            test = open(self.testFile,'r')
        except FileNotFoundError:
            print("Archivo de pruebas no encontrado: ",self.testFile)

        for line in test:
            line = line.replace('\n','');
            if line.startswith('##'):
                if flag: break
                program = line.replace('##','')
                if program == programName:
                    flag = True
            elif line != '' and flag:
                line = line.replace('< ','< '+self.testDir)
                cmd.append(self.testDir+line)
        test.close()
        if not cmd:
            print("Error: No existe el programa: ",programName)
        return cmd

    def getSolutionsByProgram(self,programName):
        flag = False
        solutions = []
        try:
            test = open(self.solutionFile,'r')
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

    def compileSource(self,sourcefile):
        """Funcion que se encarga de ejecutar el compilador gcc sobre un archivo fuente"""
        sourceCode = self.sourceCodeDir+sourcefile+'.c'
        exeDestination = self.testDir + sourcefile +'.x'
        if not isfile(sourceCode):
            print("Codigo fuente no encontrado: ",sourceCode)
            return False
        else:
            cmd = 'gcc -o '+exeDestination+' '+sourceCode
            proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            if proc.returncode == 0:
                print("Programa compilado con exito: ",sourcefile)
            else:
                print("Falló la compilación del programa: "+sourcefile+"\nErrores: ")
                print(err.rstrip().decode('utf-8'))
                return False
        return True