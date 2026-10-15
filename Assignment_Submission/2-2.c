./dict2 2 tests/dataset_1.csv output.txt < tests/testpart1.in > output.stdout.out
./dict2 2 tests/dataset_2.csv output.txt < tests/testpart2.in > output.stdout.out
./dict2 2 tests/dataset_23.csv output.txt < tests/testpart23.in > output.stdout.out
./dict2 2 tests/dataset_1353.csv output.txt < tests/testpart1353.in > output.stdout.out
valgrind ./dict2 2 tests/dataset_1353.csv output.out < tests/test1353.in > output.stdout.out