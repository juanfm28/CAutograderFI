# CAutograderFI
Automatic evaluator for school assignments written in C. Written in Python 3.5
Created originally for the Data Structures and Algorithms I course for Engineering students, taught at Universidad Nacional Autonoma de Mexico.

The grader uses gcc as a compiler, hence it is recommended its use in Linux and MacOS X with gcc installed.

# Design
The program consists in two principal modules:

autograder.py: it is in charge of parsing the execution flags, validate if they are valid or not and create the Tester object to perform the tests.

tester.py: Here is the main class, who is in charge of reading the test and solution files, compile the source code of the assignments and execute the tests.

The test programs are plain text files with the extension '.test'. They present the following format:

\#\#program1
command
command
...

\#\#program2
command
command
...

...

The solution file must follow the same format but instead of commands each line contains the output result expected from the program. This output must not contain new lines to mantain the parallelism with the test file.

Sample files are provided with the project

# Use manual
Before using this program is necessary to check and/or create the respective test files (.test) and solution(.solution)
Antes de utilizar este programa es necesario revisar o crear los archivos de pruebas (.test) y de soluciones (.solution).

It is important that the source code has the same name of both .test and .solution files for the evaluator right performance

The basic execution of the program goes as follows

```sh
python3 autograder.py
```
There are 3 possible execution options:
```sh
 -t (--tests) [file]
```
 Gives the path to the test file. It must not contain any extension.
 This is the only mandatory option.

```sh
 -p (--program) [name(s)]
```

 Indicates exactly which programs from the test file the user wants to use. They must be named without any extension. If there are many, they must be separated by ',', no spaces

```sh
 -d (--directory) [directory]
```

 Signals an external directory where the necessary files for execution and test are located. It must end in '/'

```sh
 -s (--sourcedir) [directory]
```

 Signals the external directory where the source code files to evaluate are located. It must end in '/'
