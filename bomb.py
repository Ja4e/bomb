import sys
import concurrent.futures
import os
sys.setrecursionlimit(10**7)

def infinite_recursion(n):
    return infinite_recursion(n + 1)

def run_in_threads():
    num_threads = os.cpu_count()
    print(f"Detected {num_threads} threads available on the CPU.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(infinite_recursion, 0) for _ in range(num_threads)]
        concurrent.futures.wait(futures)
run_in_threads()
