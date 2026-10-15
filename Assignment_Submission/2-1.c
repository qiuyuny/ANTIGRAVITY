make -B dict2

./dict2 2 tests/dataset_1.csv output.txt < tests/test1.in > output.stdout.out
./dict2 2 tests/dataset_2.csv output.txt < tests/test2.in > output.stdout.out
./dict2 2 tests/dataset_23.csv output.txt < tests/test23.in > output.stdout.out
./dict2 2 tests/dataset_1353.csv output.txt < tests/test1353.in > output.stdout.out

