#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct Vector
{
	double x;
	double y;
	double z;
} Vector;

double distance(Vector u, Vector v);
double angle(Vector u,Vector v);
Vector sum(Vector u,Vector v);
double pointProduct(Vector u, Vector v);
double module(Vector u);

int main(int argc, char ** argv)
{
	char *pEnd;
	Vector a;
	Vector b;
	Vector c;

	if (argc < 4)
	{
		puts("Faltan parametros");
		return 1;
	}

	a.x = strtod(argv[2],&pEnd);
	a.y = strtod(pEnd,&pEnd);
	a.z = strtod(pEnd,NULL);

	b.x = strtod(argv[3],&pEnd);
	b.y = strtod(pEnd,&pEnd);
	b.z = strtod(pEnd,NULL);

	if(!strcmp(argv[1],"distancia"))
		printf("Resultado de distancia: %lf\n", distance(a,b));
	else if(!strcmp(argv[1],"angulo"))
		printf("Resultado de angulo: %lf\n", angle(a,b));
	else if(!strcmp(argv[1],"suma"))
	{
		c = sum(a,b);
		printf("Resultado de suma: (%lf,%lf,%lf)", c.x,c.y,c.z);
	}

	return 0;
}

double distance(Vector u, Vector v)
{
	double d;
	d = pow((u.x-v.x),2);
	d += pow((u.y-v.y),2);
	d += pow((u.z-v.z),2);
	d = sqrt(d);
	return d;
}

double angle(Vector u,Vector v)
{
	/*double modU;
	double modV;
	double pointProduct;

	pointProduct = u.x*v.x + u.y*v.y + u.z*v.z;

	modU = u.x*u.x;
	modU += u.y*u.y;
	modU += u.z*u.z;
	modU = sqrt(modU);

	modV = v.x*v.x;
	modV += v.y*v.y;
	modV += v.z*v.z;
	modV = sqrt(modV);

	return acos(pointProduct / (modU * modV)) * 180.0 / 3.14159265;
*/
	return acos(pointProduct(u,v) / (module(u) * module(v))) * 180.0 / 3.14159265;
}

Vector sum(Vector u,Vector v)
{
	Vector w;
	w.x = u.x+v.x;
	w.y = u.y+v.y;
	w.z = u.z+v.z;

	return w;
}

double pointProduct(Vector u, Vector v)
{
	return u.x*v.x + u.y*v.y + u.z*v.z;
}

double module(Vector u)
{
	double mod;
	mod = u.x*u.x;
	mod += u.y*u.y;
	mod += u.z*u.z;
	mod = sqrt(mod);

	return mod;
}
