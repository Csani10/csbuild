#include <stdio.h>
#include "mymath.h"

int main()
{
	int x = add(2, 2);
	printf("2 + 2: %d\n", x);
	int y = subtract(x, 1);
	printf("(2 + 2) - 1: %d\n", y);
}
