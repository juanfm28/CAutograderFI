# CAutograderFI
Autoevaluador para programas escolares de C. Programado en python 3.5.

Únicamente funciona con gcc, por lo tanto, se recomienda unicamente su uso en Linux y MacOS X con gcc instalado.

# Diseño
TODO

# Instrucciones de uso
La ejecución básica del programa se realiza con el comando

```sh
python3 autograder.py
```
Existen 3 opciones:
```sh
 -t [file].test
```
 Indica el archivo donde se encuentran las pruebas para el comando. Esta es la única opción obligatoria.
```sh
 -p [name]
```
 Indica exactamente que programa del archivo de pruebas se quiere probar. Debe indicarse sin ninguna extensión
```sh
 -d [directory] 
```
 Indica un directorio externo donde se encuentran los archivos fuente y los archivos necesarios para la ejecución. Debe terminar en '/'
