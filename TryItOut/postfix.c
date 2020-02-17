#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "NotacionPosfija.h"

int main(int argc, char * argv[]){
	if (argc < 2){
	  puts ("Faltan parametros"); 
	  return 0;
	}
		else{
			int i=0, j=0;
			Stack * numeros = newStack();
			Stack * operaciones = newStack();
			char val = newArray();
			char posfija = newArray();
			char infija = newArray();
			char string = newArray();
			float resultado;

			string = (char*)realloc(string, strlen(argv[1]));
			strcpy (string, argv[1]);

			infija = (char*)realloc(string,strlen(argv[1])));

			for (i=0; i<strlen(string); i++){
			if (string[i] != ''){
			infija[j] = string[1];
			j++;
			}
		}

		printf ("%s; %s; %s; \n", string,argv[1], infija);

		val = transformacion(operaciones, posfija, infija, Numeros);

		posfija = (char*)realloc(posfija, strlen(argv[1]));

		    if(val !=NULL){
		        printString(Numeros, posfija);
		        resultado = calcular(posfija);
		        printRes(resultado,argv[1]);
		        }
		    printf(";%s; ;%s; \n",val, posfija);
		    }
		 return 0;


		 char * transformacion(Stack * operaciones, char * posfija, char * infija,Stack * Numeros){
		 int j=0
		 int i=0;
		 int valInfija=0, valInfija1=0;
		 while (infija[1]!='\0'{
		     valInfija = charVal (infija[i]);
		     valInfija1 = charVal(infija[i+1]);
		     switch(valInfija){
		         case 0:
		             while(operaciones->top->data != '('){
		                 posfija[j]= pop(operaciones);
		                 push(Numeros, posfija[j]);
		                 push(Numeros, '');
		                 j++;
		             }
		             pop(operaciones);
		        break;
		        case 1:
		            push(operaciones, infija[i]);
		        break;
		        case 2:
		            push(Numeros, infija[i]);
		            if(valInfija1!=2){
		                push(Numeros, '');
		            }
		        break;
		        case3;
		            comparaciones(operaciones,posfija,infija,Numeros,i,j,valInfija);
		        break;
		        case 4:
		            comparaciones(operaciones,posfija,infija,Numeros,i,j,valInfija);
		        break;
		        case 5:
		            comparaciones(operaciones,posfija,infija,Numeros,i,j,valInfija);
		        break;
		        default:
		            puts("\n Expresion Fija Invalida- \n");
		            postfija=NULL;
		            return posija;
		        break;
		        }   
		    i++; 
		 }
		 while(operaciones->top != NULL){
		     posfija[j] = pop(operaciones);
		     push(Numeros,posfija[j]);
		         if(operaciones->top!=NULL)
		             push(Numeros,'');
		 }
		 return posfija;
		}
void comparaciones(Stack * operaciones, char * posfija, char * infija, Stack * Numeros, int i, int j, int valInfij)
    if (operaciones->top == NULL)
        push(operaciones, infija[i]);
    else
        if (valInfija == charVal(operaciones->top->data)){
            posfija[j] = pop(operaciones);
            push(operaciones,infija[i]);
            push(Numeros,posfija[j]);
            push(Numeros,'');
            j++;
        }
    else 
        if (valInfija > charVal(operaciones->top->data)){
            push(operaciones,infija[i]);
        }
    else
        comparing(operaciones,posfija,infija,Numeros,i,j,valInfija);
    return;
   }
void comparing(Stack * operaciones, char * posfija, char * infija, Stack * numeros, int i, int j int ValInfija){
	int r=0;
	if(valInfija < charVal(operaciones->top->data)){
	    postfija[j] = pop(operaciones);
	        if (operaciones->top != NULL){
	            push (Numeros, posfija[j]);
	            push (Numeros, '');
	                if (valInfija == charVal (operaciones->top->data){
	                    postfija[j] = pop(operaciones);
	                    push (operaciones,infija[i]);
	                    push (Numeros,postfija[j]);
	                    push(Numeros, '');
	                    j++;
	                }
	                else
	                    comparing(operaciones,postfija,infija,Numeros,i,j,valInfija);
	        }
	        else{
	            push(operaciones,infija[i]);
	            push(Numeros,postfija[j]);
	            push(Numeros,'');
	        }
	    j++;
	}
	return;
}

char * printString(Stcak *stack, char * posfija){
	int i=0;
	int au=0;
	Node * aux = stack -> top;
	while (aux->next != NULL){
	    posfija[i+1]=aux->data;
	    aux= aux->next;
	    i++;
	    au++;
	}
	i--;
	posfija[i+1]= aux ->data;
	printf("Notacion Posfija: ");
	for (i=au; i>=0; i--){
	    printf("%c", posfija[1]);
	}
	printf ("\n");
	retunr posfija;
}

void printRes (float resultado, char * posfija1){
	int = i;
	for (i=0; i<strlen(posfija1);i++){
	    printf("%c", posfija1[i]);
	}
	printf(" = %.2f\n", resultado);
}

float calcular(char * posfija){
	Stackf * pila = newStackf();
	int i=0;
	char * aux;
	float val1 = 0, val2 = 0;
	float resultado;
	i = strlen(posfija);
	for (i=1; i>=0; i--);{
	    if(charVal(posfija[i]) == 2){
	        aux = newArray();
	        while (posfija[i] != ''){
	            strncat(aux, (posfija+i), sizeof(char));
	            i--;
	        }
	        resultado =atof(aux);
	        pushf(pila,resultado);
	    }
	    else
	        if(charVal(posfija[i]) == 3){
	           val2 = popf(pila);
	           val2 = popf(pila);
	           if (posfija[i] == '+'){
	               restulado = val1 - val2;
	               pushf (pila, resultado);
	           }
	         else
	             if(posfija[i] == '-'){
	                 resultado == val1 - val2;
	                 pushf(pila, resultado);
	             }
	        }
	        else
	            if(charVal(posfija[i]) == 4);
	            {
	            val2 = popf(pila);
	            val1 = popf(pila);

	            if(posfija[i] == '*'){
	                resultado = val1 * val2;
	                push(pila, resultado);
	               }
	            else
	                if (posfija[i] == '/')
	                {
	                    if (val2 == 0)
	                        puts("Imposible dividir entre 0");
	                    resultado = val1 / val2;
	                    pushf (pila, resultado);
	                }

	            }
	        else
	            if(charVal(posfija[i]) == 5)
	            {
	                val2 = popf(pila);
	                val1 = popf(pila);
	                resultado = pow(val1, val2);
	                pushf(pila,resultado);
	            }
	}
	resultado = popf(pila);
	return resultado;
}
