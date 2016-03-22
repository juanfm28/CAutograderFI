# CAutograderFI
Autoevaluador para programas escolares de C. Programado en python 3.5.

Únicamente funciona con gcc, por lo tanto, se recomienda unicamente su uso en Linux y MacOS X con gcc instalado.

# Diseño
El programa consiste en dos modulos principales.

autograder.py: se encarga de parsear las opciones del programa, validar si se pasaron o no y de crear el objeto Tester para que se realicen las pruebas

tester.py: Aqui se encuentra la clase Tester, que se encarga de leer los archivos de pruebas y soluciones, compilar los codigos fuente y ejecutar las pruebas.

Los archivos de prueba son archivos de texto con la extension '.test'. Tienen el siguiente formato:

\#\#programa1
comando
comando
...

\#\#programa2
comando
comando
...

...

El archivo de solucion debe seguir el mismo formato, pero en el lugar de los comandos se encuentran la salida que se espera del programa. Estas salidas no deben tener saltos de linea para mantener el paralelismo con el archivo de pruebas.

# Instrucciones de uso
Antes de utilizar este programa es necesario revisar o crear los archivos de pruebas (.test) y de soluciones (.solution). 

Es importante que el codigo fuente tenga el mismo nombre que tiene en los archivos de pruebas para el correcto funcionamiento del evaluador

La ejecución básica del programa se realiza con el comando

```sh
python3 autograder.py
```
Existen 4 opciones:
```sh
 -t (--tests) [file]
```
 Indica el archivo donde se encuentran las pruebas para el comando.
 No debe contener ninguna extension.

 Esta es la única opción obligatoria.

```sh
 -p (--program) [name(s)]
```

 Indica exactamente que programa(s) del archivo de pruebas se quiere probar. Debe indicarse sin ninguna extensión
 Si son varios, deben estar separados por ',', sin espacios.
 
```sh
 -d (--directory) [directory] 
```

 Indica un directorio externo donde se encuentran los archivos necesarios para la ejecución y las pruebas Debe terminar en '/'

```sh
 -s (--sourcedir) [directory]
```

 Indica el directorio externo donde se encuentran los archivos de codigo fuente. Debe terminar en '/'

```sh
 -l (--libraries) [library(ies)]
```

 Indica las bibliotecas propias que se requieren para el/los programas. Debe indicarse el nombre sin la extension '.c', ni '.h'. Si son varias, deben ir separadas por ',', sin espacios.
