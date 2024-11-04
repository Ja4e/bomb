import sys  
import concurrent.futures  
import os
import math  

sys.setrecursionlimit(10**7)

def infinite_recursion(n):
    return infinite_recursion(n + 1)

def Memorybomb(n):   
    return infinite_recursion(n)

def Memory_launcher():  
    num_threads = os.cpu_count()  
    print(f"Running memory-intensive recursion on {num_threads} threads.")  
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:  
        futures = [executor.submit(Memorybomb, 0) for _ in range(num_threads)]  
        concurrent.futures.wait(futures)  

def CPUbomb():  
    result = 0.0  
    while True:
        for i in range(1, 100000):  
            result += math.sin(i) ** 2 + math.cos(i) ** 2  
        result = 0.0  

def CPU_launcher():  
    num_threads = os.cpu_count()  
    print(f"Running CPU load on {num_threads} threads.")  
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:  
        futures = [executor.submit(CPUbomb) for _ in range(num_threads)]  
        concurrent.futures.wait(futures)  

if __name__ == "__main__":  
    with concurrent.futures.ThreadPoolExecutor() as executor:  
        executor.submit(Memory_launcher)  
        executor.submit(CPU_launcher)  

