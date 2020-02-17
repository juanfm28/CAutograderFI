# -*- coding: utf-8 -*-

#Test module
from os.path import isfile
from subprocess import Popen,PIPE
from os import remove as rm
import signal

class Tester:
    """Class that controls all the test processes"""
    def __init__(self, testFile,sourceCodeDir = './',testDir = './',libraries=None):
        """Tester class builder

        testFile -- file where the tests are storedArchivo donde estan contenidas las pruebas a pasar
        sourceCodeDir -- Directory where the source code is stored, default='./'
        testDir -- Directory where the test files are stored, default='./'
        """
        #Name of the test file to use without extension.
        testFileCore = testFile
        #Instance attribute: Directory of the source code files
        self.sourceCodeDir = sourceCodeDir
        #instance attribute: Directory of the test files
        self.testDir = testDir
        #instance attribute: Full path to the test file
        self.testFile = self.testDir+testFileCore+'.test'
        #instance attribute: Full path to the solution file
        self.solutionFile = self.testDir+testFileCore+'.solution'
        #instance attribute: List with the name of all programs to test
        self.programNames = self.getProgramNames()
        self.showDiff = False
        #Atributo de instancia libs: Lista de las librerias necesarias
        if libraries:
            self.needsLib = True
            self.libs = libraries
        else: self.needsLib = False


    def setSourceCodeDir(self,sourceCodeDir):
        """Setter for the instance attribute sourceCodeDir"""
        self.sourceCodeDir = sourceCodeDir

    def toggleDiff(self):
        """Toggle for showing the difference in results"""
        self.showDiff = not self.showDiff

    def runAllTests(self):
        """Function that automatically runs all the programs in the file"""
        #For each program in the list execute the function that test a program.
        for program in self.programNames:
            self.testProgram(program)

    def testProgram(self,programName):
        """Function that evaluates a whole program

           Parameters:
           programName: Name of the program to evaluate. It must exist both in the test and the solution files"""
        #It informs the user which program is being evaluated
        print("Evaluating: ",programName.split('%')[0])
        #The program is compiled used the custom function and the output is stored to know if the compilation was succesful.
        success = self.compileSource(programName)
        #If the program did not compile, the function stops and returns.
        if not success:
            return
        #Get a list with the test to perform per program in the form of commands.
        cmds = self.getTestsByProgram(programName)
        #Get a list of the expected outputs for each test for each program.
        solutions = self.getSolutionsByProgram(programName)
        #Variable for the total number of tests in this program to evaluate
        possiblePoints = len(cmds)
        #Variable that will store the points earned
        pointsObtained = 0
        #Each test is zipped with its solution to iterate over them
        #The current test command is in cmd and the expected output in solution
        for cmd,solution in zip(cmds,solutions):
            #The script tries to execute the current test using the command in the variable cmd
            try:
                raw_output = Tester.runCommand(cmd)
            #It is possible that the output is unreadable, which triggers this exception
            except UnicodeDecodeError:
                #If it was not possible, it is informed to the user and the function ends with 0.
                print("\n",'Non-readable output')
                return 0.0
            #if the result of the test corresponds with the expected output...
            if Tester.assertOutput(raw_output,solution):
                #Print both the test and its result and informs the user this was correct
                print(cmd,": \n",raw_output," Correct","\n")
                #One point is added to the grading
                pointsObtained += 1
            #if the output is not similar enough...
            else:
                #Print both the test and its result, along with the expected output
                print("\n",cmd,": \n",raw_output," \n\nIncorrect. The expected output was: \n",solution,"\n")
                #If this was activated, the exact differences in the outputs are shown
                if self.showDiff: Tester.showDifferences(raw_output,solution)
        #When the tests are completed, the script informs how many tests were passed in this program
        print("\nCorrect in",programName.split('%')[0], ": ",pointsObtained,'/',possiblePoints)
        #This print a separator for the next program to be easy to recognize
        print("********************************************************")
        #To keep the directory clean, the executables are eliminated
        try:
            rm(self.testDir+programName.split('%')[0]+'.x')
        except FileNotFoundError:
            pass
        #In the end, the grade is returned back to this function's caller
        #TODO: Recibir este dato en algún lado
        return (pointsObtained*1.0)/(possiblePoints*1.0)

    def assertOutput(raw_output,solution):
        """Function that asserts if the result is similar enough to the expected output to be admissible.
            Arguments:
            raw_output: result output
            solution: expected output for the test"""
        #The raw output received is formatted in the following way:
        #Everything is passed to lowercase, and whitespace is trimmed
        #Special characters such as \n \t and \x00 are replaced by one white space character
        output = raw_output.lower().rstrip().lstrip().replace("\x00","").replace('\n',' ').replace('\t',' ')
        #Next, it is converted in a list using split and all the spaces are eliminated, in an attempt for tokenize the output, so only the tokens and their orden matter
        editedOutput = [value for value in output.split(' ') if value != '']
        #For the expected output only the new lines are replaced, the strings becomes a list and all empty tokens are eliminated
        editedSolution = [value for value in solution.lower().replace('\n',' ').split(' ') if value != '']
        #Both lists are compared and the result is sent back
        return editedSolution == editedOutput

    def showDifferences(raw_output,solution):
        """Function that prints the differences between the expected output and the result output from the evaluation"""
        print("Differences: ")
        i = 1
        for lineO,lineS in zip(raw_output.split('\n'),solution.split('\n')):
            if lineO.strip() != lineS.strip():
                print(i,": ",lineS," ---> ",lineO)
            i += 1


    def runCommand(cmd='echo "Hello world"'):
        """Wrapper function to execute commands.
        Arguments
        cmd: Command to execute. Default: echo "Hellow world"
        """
        #A background process is opened to execute the program
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        #The standard output and error output from the subprocess is captured
        out, err = proc.communicate()
        #IF there are errors or warnings, this is informed to the user
        if proc.returncode == -11:
            print("Segment violation!!")

        if err: #!= b'\n':
            print("Error or Warning: ")
            #The standard error output is prined in utf-8
            return err.decode('utf-8')
        else:
            #If there are no errors, the result is read from the standard output in utf-8
            return out.decode('utf-8')

    def getProgramNames(self):
        """Function that parses all the programs existing in a test file"""
        #Starting with an empty string list
        names = []
        #It tries to open the test file. The path is obtained from the instance attribute. It is opened read-only to maintain the data
        try:
            test = open(self.testFile,'r')
        #If it is not possible to find the file, this is informed to the user and the empty list is sent back
        except FileNotFoundError:
            print("Test file not found: ",self.testFile)
            return names
        #For each line in the file
        for line in test:
            #The empty lines are eliminated. (They only have a new line character)
            line = line.replace('\n','');
            #If the line is not empty, and it starts with ##, this means this is the name of a program and the start of its tests
            if line != "" and line.startswith('##'):
                #The name of the program is added
                names.append(line.replace('##',''))
        #The file is closed
        test.close()
        #The list of names is returned
        return names

    def getTestsByProgram(self,programName):
        """Function that fetches all the tests intended for one program, contained in the test file.
           Arguments:
           programName: Name of the program I want to obtain the tests from."""
        #The execution requires a flag, this tells me that the test from this program were already being fetched.
        flag = False
        #It starts with an empty list
        cmd = []
        #An attempt to open the test file is made. The path is obtained from the instance attribute. It is opened read-only to maintain the data
        try:
            test = open(self.testFile,'r')
        #If it is not possible to find the file, this is informed to the user and the empty list is sent back
        except FileNotFoundError:
            print("Test file not found: ",self.testFile)

        #For each line in the file
        for line in test:
            #The empty lines are discarded (they only have a \n)
            line = line.replace('\n','');
            #If the line is not empty and starts with ## it is the name of a program and the start of its tests
            if line.startswith('##'):
                #if I was already processing a program, finding another name means that I finished with this program, so it will break out of the loop.
                if flag: break
                #if I hadn't start this process before, the ## are replaced to obtain the name of the program
                program = line.replace('##','')
                #If the program found is the one I was looking for, the flag goes up
                if program == programName:
                    flag = True
            #If its not a program name but the flag is up, it is part of the programs test
            elif line != '' and flag:
                #This test requires a certain format.
                #When a < is found in a command this means that the standard input must be redirected to a file. To this symbol, the script ads the test directory, because it is assumed that the target file is there.
                #When a ! is found, this means that this argument is a file, so the test directory replaces the !. This, again, because it is assumed that file is in the test directory.
                line = line.replace('< ','< '+self.testDir).replace('!',self.testDir)
                #To the command line we add the read line, but the test directory is again added at the beginning of the command cause it is assumed that the executable will be there after this script compiles it.
                cmd.append(self.testDir+line)
        #The file is closed
        test.close()
        #If the list is empty, then it is informed to the user that such program does not exist in the file
        if not cmd:
            print("Error: Program does not exist: ",programName)
        #In any case, the list is returned to the caller
        return cmd

    def getSolutionsByProgram(self,programName):
        """Function that fetches all the expected solutions for every test in the program, contained in the solution file (.solution)
           Arguments:
           programName: Name of the program for which I want to obtain the expected solutions"""
        #The execution will require a flag that tells me that I am already in the process of extracting solutions
        flag = False
        #Start with an empty list
        solutions = []
        #Try to open the solution fine. This is read from the instance attribute. It is opened as read-only
        try:
            test = open(self.solutionFile,'r')
        #If the file is not found, inform the user and return the empty list
        except FileNotFoundError:
            print("Solution file not found: ",testFile)

        #For each line in the file
        for line in test:
            #Empty lines are discarded (those with only an \n)
            line = line.replace('\n','');
            #If the line is not an empty line and it starts with ##, that means it is the name of a program.
            if line.startswith('##'):
                #If the flag signals that the process of fetching solutions had already started, this means I found the end of the solution list for this program, so the loop breaks
                if flag: break
                #If the process hasn't started, then the ## are eliminated to extract the name of the program
                program = line.replace('##','')
                #If this is the program I am looking for, the flags signals I'm starting the fetching process.
                if program == programName.split('%')[0]:
                    flag = True
            #If this is not a program name (starting with ##) and the flag is up, then it means it is a solution from a test.
            elif line != '' and flag:
                #Thus it is added to the solution list, replacing every simulated new line with a real new line.
                solutions.append(line.replace("\\n","\n"))
        #The file is closed
        test.close()
        #If the solution list did not exist for that program, then it is informed to the user
        if not solutions:
            print("Error: The program does not exist in the solution file.",programName.split('%')[0])
        #In any case, the solution list is returned
        return solutions

    def compileSource(self,sourcefile):
        """Function that handles the compilation of the source code using gcc."""
        #The source code variable starts empty
        sourceCode = ""
        #The source file is split in its many components
        src = sourcefile.split('%')
        if self.needsLib:
            for lib in self.libs:
                sourceCode += self.sourceCodeDir+lib+'.c'+' '
        #For every file in the list, the extension '.c' is added
        for f in src:
            sourceCode += ' '+self.sourceCodeDir+f+'.c'
        #The destination path is set adding a .x to identify
        exeDestination = self.testDir + sourcefile.split('%')[0] +'.x'
        #For each filename in source code after splitting it by whitespaces
        for code in sourceCode.strip().split(' '):
            #if that name is not found or is not a file, it is informed to the user and it returns false.
            if not isfile(code):
                print("Source code not found: ", code)
                return False
        #The compliation command is built
        cmd = 'gcc -o '+exeDestination+' '+sourceCode
        #The subproccess to run the compilation command is opened
        proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        #the process is executed and its output read
        out, err = proc.communicate()
        #if the process is succesful, the compilation was successful
        if proc.returncode == 0:
            print("Succesful compilation of program: ",sourcefile.split('%')[0])
            #Even then, there might be warnings to inform
            if err:
                print("Warnings: ",err.rstrip().decode('utf-8'))
        #If the compilation fails, the errors are notified
        else:
            print("The compiliation of the program failed: "+sourcefile+"\nErrors: ")
            print(err.rstrip().decode('utf-8'))
            return False
        return True
