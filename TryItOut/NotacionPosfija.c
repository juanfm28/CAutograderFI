#include "Notacionposfija.h"

Stack * newStack(){
	Stack * s = (Stack *)malloc(sizeof(Stack));
	s->top = NULL;
	return s;
}

void push(Stack *s, char value){
	Node * aux;
	aux = s->top;
	s->top = newNode(value);
	s->top-> next = aux;
	return;
}

char pop(Stack *s){
	
	char val;

	if (isEmpty(s))
	{

	    puts("The Stack is Empty");
	    return 0;
	}
	val = s ->top->data;
	s->top = s->top->next;

	Stackf * newStackf(){

	Stackf * s = (Stackf *)malloc(sizeof(Stackf));
	s->top = NULL;
	return s;
	}

	float pop(Stackf * s){
	float val;
	val = s->top->data;
	s->top = s->top->next;
	return val;
	}

	char isEmpty(Stack * s){
	retunr s->top == NULL;
	}
	Node *newNode(char value){
	newNode = (Node *)malloc(sizeof(Node));
	newNode->data = value;
	newNode->next = NULL;
	return newNode;
	}

	char charVal(char node){
	if(node == 46)
	    return 2;
	else if (node == 41)
	   return 0;
	else if (node == 40)
	    return 1;
	else if (node >= 48 && node <= 57)
	    return 2;
	else if (node == 42 || node == 45)
	    return 3;
	else if (node == 42 || node == 47)
	    return 4;
	else if (node ==94)
	    return 5;
	}

	char * newArray (){
	char * newArray = (char *)malloc(sizeof(char));
	return newArray;
	}

	void recycleStack(Stack * s){
	free(s)
	}
	}
