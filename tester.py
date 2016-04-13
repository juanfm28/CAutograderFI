# -*- coding: utf-8 -*-

#Modulo de asserts
from os.path import isfile
from subprocess import Popen,PIPE
from os import remove as rm
import signal

class Tester:
    """Clase que controla todos los procesos de prueba"""
    def __init__(self, testFile,sourceCodeDir = './',testDir = './',libraries=None):
        """Constructor de la clase Tester

        testFile -- Archivo donde estan contenidas las pruebas a pasar
        sourceCodeDir -- Directorio donde estan contenidos los codigos fuente, default='./'
        testDir -- Directorio donde estan contenidos los archivos necesarios para las pruebas, default='./'
        libraries -- Lista de las bibliotecas necesarias
        """
        #Nombre del archivo de pruebas a usar sin extensión
        testFileCore = testFile
        #Atributo de instancia sourceCodeDir: Directorio de los codigos fuente
        self.sourceCodeDir = sourceCodeDir
        #Atributo de instancia testDir: Directorio del archivo de pruebas
        self.testDir = testDir
        #Atributo de instancia testFile: Path completo del archivo de pruebas
        self.testFile = self.testDir+testFileCore+'.test'
        #Atributo de instancia solutionFile: Path completo del archivo de soluciones 
        self.solutionFile = self.testDir+testFileCore+'.solution'
        #Atributo de instancia programNames: Lista con todos los nombres de los programas que se probaran
        self.programNames = self.getProgramNames()
        #Atributo de instancia needsLib: Bandera que me indica si es necesario agregar liberias
        #Atributo de instancia libs: Lista de las librerias necesarias
        if libraries: 
            self.needsLib = True
            self.libs = libraries
        else: self.needsLib = False

    def setSourceCodeDir(self,sourceCodeDir):
        """Setter del atributo de instancia sourceCodeDir"""
        self.sourceCodeDir = sourceCodeDir

    def runAllTests(self):
        """Función que ejecuta todos los test existentes"""
        #Por cada programa en la lista ejecuta la funcion que prueba un programa
        for program in self.programNames:
            self.testProgram(program)

    def testProgram(self,programName):
        """Función que evalua un programa
           Argumentos:
           programName: Nombre del programa a evaluar. Debe existir tanto en el archivo de pruebas, como en el de soluciones"""
        #Indicador al usuario de que programa se está probando
        print("Evaluando: ",programName)
        #Se compila el programa usando la función y se guarda su retorno para saber si fue exitosa la compilación
        success = self.compileSource(programName)
        #Si no pudo compilarse, regresa
        if not success:
            return
        #Se obtiene una lista con las pruebas que se ejecutaran por cada programa en forma de comandos.
        cmds = self.getTestsByProgram(programName)
        #Se obtiene una lista con las soluciones esperadas de cada prueba por programa.
        solutions = self.getSolutionsByProgram(programName)
        #Variable para el numero de pruebas de este programa
        possiblePoints = len(cmds)
        #Variable para los puntos obtenidos 
        pointsObtained = 0
        #Se juntan cada prueba con su solución para realizarlas
        #El comando de la prueba se encuentra en cmd y la salida esperada se encuentra en solution
        for cmd,solution in zip(cmds,solutions):
            #Se intenta ejecutar la prueba actual ejecutando el comando en cmd
            try:
                raw_output = Tester.runCommand(cmd)
            #Es posible que al ejecutar el comando no pueda leer el resultado, lo cual arroja esta excepción
            except UnicodeDecodeError:
                #Si no es posible leer la salida del comando ejecutado, se informa y se regresa 0
                print("\n",'Salida no reconocible')
                return 0.0
            #Si el resultado de la prueba corresponde a lo esperado de acuerdo a las condiciones establecidas...
            if Tester.assertOutput(raw_output,solution):
                #Imprime tanto la prueba como su resultado e informa que es correcto
                print(cmd,": \n",raw_output," Correcto","\n")
                #Se suma un punto a los obtenidos
                pointsObtained += 1
            #Si no es lo suficientemente parecida
            else:
                #Imprime tanto el comando, como su resultado y el resultado esperado
                print("\n",cmd,": \n",raw_output," \n\nIncorrecto. El resultado esperado era: \n",solution,"\n")
        #Cuando se terminen de ejecutar las pruebas, se informa cuantos se pasaron en este programa
        print("\nPasados en",programName, ": ",pointsObtained,'/',possiblePoints)
        #Separador de programa
        print("********************************************************")
        #Para mantener limpio el directorio, el ejecutable generado se elimina
        try:
            rm(self.testDir+programName+'.x')
        except FileNotFoundError:
            pass
        #Al final de la ejecución de las pruebas, se pretende regresar la calificación de quien fue revisado
        #TODO: Recibir este dato en algún lado
        return (pointsObtained*1.0)/(possiblePoints*1.0)

    def assertOutput(raw_output,solution):
        """Funcion que determina si el resultado es lo suficientemente parecido al esperado como para ser admitido
            Argumentos:
            raw_output: Resultado generado por el programa
            solution: Solución esperada de la prueba"""
        #La salida directa del comando se formatea de la siguiente forma
        #Se pasa todo a minusculas, se quitan los espacios antes y despues,
        # se remplazan los caracteres especiales \n \t y \x00 por espacios
        output = raw_output.lower().rstrip().lstrip().replace("\x00","").replace('\n',' ').replace('\t',' ')
        #posteriormente se convierte en una lista con split y se eliminan todos los espacios encontrados, para que se tomen en cuenta
        #solo las palabras validas y su orden
        editedOutput = [value for value in output.split(' ') if value != '']
        #Para la solucion esperada, solo se cambian los saltos de línea, se convierte en una lista y de esa lista se eliminan las cadenas vacias
        #correspondientes a donde habia un espacio en la impresión 
        editedSolution = [value for value in solution.lower().replace('\n',' ').split(' ') if value != '']
        #print(editedOutput)
        #print(editedSolution)
        #Se compararn ambas listas y se regresa el resultado de dicha comparación
        return editedSolution == editedOutput


    def runCommand(cmd='echo "Hola mundo"'):
        """Funcion que ejecuta un comando
        Argumentos
        cmd: Comando a ejecutar. Default: echo "Hola mundo"
        """
        #Se abre un subproceso que ejecute el comando
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        #Obtenemos la salida estandar y la salida de error del subproceso
        out, err = proc.communicate()
        #Si existen errores o warnings al ejecutar el comando se informa
        if proc.returncode == -11:
            print("Ocurrio una violación de segmento!!") 

        if err: #!= b'\n':
            print("Ocurrio un error o warning: ")
            #Se regresa el resultado de la salida estandar de errores, decifrado como si fuera utf-8
            return err.decode('utf-8')
        else:
            #Si no existen errores, se regresa el resultado de la salida estandar, decifrado como texto utf-8
            return out.decode('utf-8')

    def getProgramNames(self):
        """Función que obtiene todos los programas existentes en un archivo de prueba"""
        #Inicia con una lista de nombres vacia
        names = []
        #Se intenta abrir el archivo de pruebas. Este se obtiene del atributo de instancia. Se abre como de solo lectura
        try:
            test = open(self.testFile,'r')
        #Si no es posible encontrar el archivo, se informa y se regresa la lista vacía 
        except FileNotFoundError:
            print("Archivo de pruebas no encontrado: ",self.testFile)
            return names
        #Por cada linea en el archivo
        for line in test:
            #Se desprecian las lineas vacias (que solo tienen un |n)
            line = line.replace('\n','');
            #Si la linea no es una de estas vacias e inicia con ## eso significa que es el nombre de un programa
            if line != "" and line.startswith('##'):
                #Se agrega el nombre del programa, quitandole los ## del inicio
                names.append(line.replace('##',''))
        #Finalmente se cierra el archivo
        test.close()
        #Se regresa la lista de nombres
        return names

    def getTestsByProgram(self,programName):
        """Función que obtiene todos los test que se realizaran para un programa, contenidos en el archivo de tests
           Argumentos:
           programName: Nombre del programa del cual quiero obtener los tests"""
        #La ejecucion requerira una bandera, que me dice que ya se estaban extrayendo los test del programa que queria
        flag = False
        #Se inicia con una lista de comandos vacia
        cmd = []
        #Se intenta abrir el archivo de pruebas. Este se obtiene del atributo de instancia. Se abre como de solo lectura
        try:
            test = open(self.testFile,'r')
        #Si no es posible encontrar el archivo, se informa y se regresa la lista vacía 
        except FileNotFoundError:
            print("Archivo de pruebas no encontrado: ",self.testFile)

        #Por cada linea en el archivo
        for line in test:
            #Se desprecian las lineas vacias (que solo tienen un |n)
            line = line.replace('\n','');
            #Si la linea no es una de estas vacias e inicia con ## eso significa que es el nombre de un programa
            if line.startswith('##'):
                #Si ya estaba sacando los tests, encontrar otro nombre de programa significa que ya acabé
                if flag: break
                #Si no elimina los ## para obtener el nombre puro
                program = line.replace('##','')
                #Si el programa que encontré es el que buscaba, levanta la bandera
                if program == programName:
                    flag = True
            #Si no es un nombre de programa (iniciado con ##) y la bandera ya esta arriba, significa que es un test
            elif line != '' and flag:
                #Requiere cierto formato
                #Cuando en un comando se encuentre un < eso quiere decir que necesita una redireccion de entrada,
                #a este simbolo se le agrega el directorio de pruebas, porque se espera que ahí esté el archivo necesario
                #Cuando existe un ! quiere decir que ese argumento a main es un archivo, y se le agrega el directorio de las pruebas
                #pues se asume que ese archivo que se le va a pasar al programa esta en el directorio de las pruebas
                line = line.replace('< ','< '+self.testDir).replace('!',self.testDir)
                #A la lista de comandos se agrega la linea leída, pero antes se le anexa el directorio de las pruebas, porque ahi se espera
                #que se construya el ejecutable cuando se compile con este mismo evaluador
                cmd.append(self.testDir+line)
        #Se cierra el archivo
        test.close()
        #Si la lista termina vacia, se informa que no existe el programa
        if not cmd:
            print("Error: No existe el programa: ",programName)
        #De cualquier modo, se regresa la lista
        return cmd

    def getSolutionsByProgram(self,programName):
        """Función que obtiene todos las soluciones esperadas para cada test del programa, contenidos en el archivo de soluciones
           Argumentos:
           programName: Nombre del programa del cual quiero obtener las soluciones esperadas"""
        #La ejecucion requerira una bandera, que me dice que ya se estaban extrayendo las soluciones del programa que queria
        flag = False
        #Se inicia con una lista de soluciones vacia
        solutions = []
        #Se intenta abrir el archivo de soluciones. Este se obtiene del atributo de instancia. Se abre como de solo lectura
        try:
            test = open(self.solutionFile,'r')
        #Si no es posible encontrar el archivo, se informa y se regresa la lista vacía 
        except FileNotFoundError:
            print("Archivo de soluciones no encontrado: ",testFile)

        #Por cada linea en el archivo
        for line in test:
            #Se desprecian las lineas vacias (que solo tienen un |n)
            line = line.replace('\n','');
            #Si la linea no es una de estas vacias e inicia con ## eso significa que es el nombre de un programa
            if line.startswith('##'):
                #Si ya estaba sacando las soluciones, encontrar otro nombre de programa significa que ya acabé
                if flag: break
                #Si no elimina los ## para obtener el nombre puro
                program = line.replace('##','')
                #Si el programa que encontré es el que buscaba, levanta la bandera
                if program == programName:
                    flag = True
            #Si no es un nombre de programa (iniciado con ##) y la bandera ya esta arriba, significa que es una solucion
            elif line != '' and flag:
                #Se agrega a la lista sustituyendo un salto de linea simulado por uno real
                solutions.append(line.replace("\\n","\n"))
        #Se cierra el archivo
        test.close()
        #Si el archivo de soluciones terminó vacío, el programa no existía y se informa
        if not solutions:
            print("Error: No existe ese programa en el archivo de solucion",programName)
        #De cualquier forma se regresa el archivo de soluciones
        return solutions

    def compileSource(self,sourcefile):
        """Funcion que se encarga de ejecutar el compilador gcc sobre un archivo fuente"""
        sourceCode = ""
        if self.needsLib:
            for lib in self.libs:
                sourceCode += self.sourceCodeDir+lib+'.c'+' '
        sourceCode += self.sourceCodeDir+sourcefile+'.c'
        exeDestination = self.testDir + sourcefile +'.x'
        for code in sourceCode.split(' '):
            if not isfile(code):
                print("Codigo fuente no encontrado: ", code)
                return False
        cmd = 'gcc -o '+exeDestination+' '+sourceCode
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if proc.returncode == 0:
            print("Programa compilado con exito: ",sourcefile)
            if err:
                print("Advertencias: ",err.rstrip().decode('utf-8'))
        else:
            print("Falló la compilación del programa: "+sourcefile+"\nErrores: ")
            print(err.rstrip().decode('utf-8'))
            return False
        return True