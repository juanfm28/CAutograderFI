#include <stdio.h>
#include <stdlib.h>

struct Node{
	char data;
	struct Node * next;
};

typedef struct Node Node;

struct Nodef{
	float data;
	struct Nodef * next;
};

typedef struct Nodef Nodef;

typedef struct{
	Node * top;
} Stack;

typedef struct {
	Nodef * top;
} Stackf;

//funciones pila
Stack * newStack();
void push(Stack *s, char value);
char pop(Stack *s);
char isEmpty(Stack * s);
Node * newNode(char value);
char charVal(char node);
void recycleStack(Stack * s);

Stackf * newStackf();
void pushf(Stackf *s, float value);
float popf(Stack *s);
Nodef * newNodef(float value);

char * newArray();

//transformacion
char * transformacion(Stack * operaciones, char * posfija, char * infija, Stack * Numeros);
void comparaciones(Stack * operaciones, char * posfija, char * infija, Stack * Numeros, int i, int j, int valInfija);
void comparing(Stack * operaciones, char * posfija, char * infija, Stack * Numeros, int i, int j, int valInfija);

//imprimir
char * printString(Stack *stack, char * posfija);
float calcular(char * posfija);
void printRes(float resultado, char * posfija);

char * stringCondenser(char * string);
