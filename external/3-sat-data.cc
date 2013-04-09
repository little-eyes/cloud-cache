/*
 * This module is used to generate the 3-SAT 
 * input data. The data format shows in the
 * following:
 * n, m, [...]
 * - n is the number of variables.
 * - m is the number of variables in expression.
 * - then follows the expression list, separated
 * by comma.
 *
 * The output will be 3-sat.in which is actually
 * a CSV file. 
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>

using namespace std;


int main (int argc, char *argv[]) {
	int NumberOfCases = 1000000;
	if (argc == 3 && strcmp(argv[1], "-n") == 0)
		NumberOfCases = atoi(argv[2]);
	FILE *fp = fopen("3-sat.in", "w");
	srand(time(NULL));
	for (int i = 0; i < NumberOfCases; ++i) {
		int NumberOfVariables = rand() % 20 + 1;
		int NumberOfExpressions = 3 * (rand() % 30 + 1);
		fprintf(fp, "%d,%d", NumberOfVariables, NumberOfExpressions);
		for (int j = 0; j < NumberOfExpressions; ++j) {
			int x = (rand() % 100000) % NumberOfVariables + 1;
			if (rand() % 100 >= 50) x = -x;
			fprintf(fp, ",%d", x);
		}
		fprintf(fp, "\n");
		if (i % (NumberOfCases/100+1) == 0) 
			printf("[%d\%] finished.\n", i/(NumberOfCases/100+1));
	}
	fclose(fp);
	return 0;
}
