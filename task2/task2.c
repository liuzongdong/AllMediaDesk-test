#include <stdio.h>
#include <math.h>

int valid(long int x)
{
	if (x < 10) return 1;
	long int last = x % 10;
	long int next = (x / 10) % 10;
	if (last < next) return 0;
	else return valid(x / 10);
}


void main()
{
	long int input;
	printf("Input: ");
	scanf("%ld", &input);
	if (input > pow(10, 18) || input < 0) {
	    printf("invalid input\n");
	}
	else {
	    long int output = input;
	    while (!valid(output))output--;
	    printf("Output: %ld\n", output);
	}

}

