import subprocess
import time
import re

datasets = [
    ("dataset_1.csv", "test1.in", 1, "test1"),
    ("dataset_2.csv", "test2.in", 2, "test2"),
    ("dataset_23.csv", "test23.in", 23, "test23"),
    ("dataset_1353.csv", "test1353.in", 1353, "test1353"),
]

part_datasets = [
    ("dataset_1.csv", "testpart1.in", 1, "testpart1"),
    ("dataset_2.csv", "testpart2.in", 2, "testpart2"),
    ("dataset_23.csv", "testpart23.in", 23, "testpart23"),
    ("dataset_1353.csv", "testpart1353.in", 1353, "testpart1353"),
]

def run_bench(program, stage_arg, dataset, test_in):
    csv_path = f"Dataset_Download/tests/{dataset}"
    in_path = f"Dataset_Download/tests/{test_in}"
    out_file = "bench_out.txt"
    
    with open(in_path, "r") as f_in:
        input_data = f_in.read()

    start = time.perf_counter()
    proc = subprocess.run(
        [f"./{program}.exe", str(stage_arg), csv_path, out_file],
        input=input_data,
        capture_output=True,
        text=True
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    lines = proc.stdout.strip().split("\n")
    b_total, n_total, s_total = 0, 0, 0
    query_count = 0
    for line in lines:
        m = re.search(r"comparisons: b(\d+) n(\d+) s(\d+)", line)
        if m:
            b_total += int(m.group(1))
            n_total += int(m.group(2))
            s_total += int(m.group(3))
            query_count += 1

    avg_b = b_total / query_count if query_count else 0
    avg_n = n_total / query_count if query_count else 0
    avg_s = s_total / query_count if query_count else 0
    return query_count, avg_b, avg_n, avg_s, elapsed_ms

print("=== EXACT MATCH BENCHMARK ===")
print(f"{'Dataset':<16} | {'N':<6} | {'Prog':<6} | {'Queries':<8} | {'Avg b':<10} | {'Avg n':<8} | {'Avg s':<8} | {'Time (ms)':<10}")
print("-" * 85)

for d, t, n, name in datasets:
    # Dict 1
    q1, b1, n1, s1, t1 = run_bench("dict1", 1, d, t)
    print(f"{d:<16} | {n:<6} | {'dict1':<6} | {q1:<8} | {b1:<10.1f} | {n1:<8.1f} | {s1:<8.1f} | {t1:<10.2f}")
    # Dict 2
    q2, b2, n2, s2, t2 = run_bench("dict2", 2, d, t)
    print(f"{d:<16} | {n:<6} | {'dict2':<6} | {q2:<8} | {b2:<10.1f} | {n2:<8.1f} | {s2:<8.1f} | {t2:<10.2f}")
    print("-" * 85)

print("\n=== SPELLCHECKING (PARTIAL MATCH) BENCHMARK ===")
print(f"{'Dataset':<16} | {'N':<6} | {'Prog':<6} | {'Queries':<8} | {'Avg b':<10} | {'Avg n':<8} | {'Avg s':<8} | {'Time (ms)':<10}")
print("-" * 85)

for d, t, n, name in part_datasets:
    # Dict 2 only (dict1 does not support spellcheck)
    q2, b2, n2, s2, t2 = run_bench("dict2", 2, d, t)
    print(f"{d:<16} | {n:<6} | {'dict2':<6} | {q2:<8} | {b2:<10.1f} | {n2:<8.1f} | {s2:<8.1f} | {t2:<10.2f}")
    print("-" * 85)

