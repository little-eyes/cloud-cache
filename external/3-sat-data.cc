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
#include <ctime>

using namespace std;

const int NUM_CASES = 1000000;


int main () {
	FILE *fp = fopen("3-sat.in", "w");
	srand(time(NULL));
	for (int i = 0; i < NUM_CASES; ++i) {
		int n = rand() % 20 + 1;
		int m = 3 * (rand() % 30 + 1);
		fprintf(fp, "%d,%d", n, m);
		for (int j = 0; j < m; ++j) {
			int x = (rand() % 100000) % n + 1;
			if (rand() % 100 >= 50) x = -x;
			fprintf(fp, ",%d", x);
		}
		fprintf(fp, "\n");
		if (i % 10000 == 0) printf("[%d\%] finished.\n", i/10000);
	}
	fclose(fp);
	return 0;
}

