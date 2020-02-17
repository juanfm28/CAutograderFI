#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct Point
{
	int x;
	int y;
} Point;

void printPoints(Point *arr, int size);
double completeDistance(Point *arr, int size);
double distance(Point *p, Point *q);

int main(int argc, char ** argv)
{
	Point arr[6] = {{2,1},{2,4},{-1,3},{-8,-9},{1,4},{5,17}};
	printPoints(arr,6);
	printf("Distancia total: %.2lf\n",completeDistance(arr,6));

	return 0;
}

void printPoints(Point *arr, int size)
{
	int i;
	for(i = 0 ; i < size ; i++)
		printf("(%d,%d) ",(arr+i)->x, (arr+i)->y);

	printf("\n");
	return;
}
double completeDistance(Point *arr, int size)
{
	double totalDistance = 0.0;
	int i;

	for(i = 0 ; i < size-1 ; i++)
		totalDistance += distance(arr+i,arr+i+1);

	return totalDistance;
}

double distance(Point *p, Point *q)
{
	return sqrt(pow(p->x-q->x,2) + pow(p->y-q->y,2));
}