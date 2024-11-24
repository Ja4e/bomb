import sys
import concurrent.futures
import os
import time
from shutil import which
sys.setrecursionlimit(10**7)

def infinite_recursion(n):
    return infinite_recursion(n + 1)

def run_in_threads():
    num_threads = os.cpu_count()
    print(f"Detected {num_threads} threads available on the CPU.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(infinite_recursion, 0) for _ in range(num_threads)]
        concurrent.futures.wait(futures)

def disable_oom_killer(pid):
    try:
        oom_adj_path = f"/proc/{pid}/oom_score_adj"
        with open(oom_adj_path, "w") as file:
            file.write("-1000")
        print(f"Disabled OOM killer for process {pid}.")
        if which("powerprofilesctl") is not None:
            os.system("powerprofilesctl set performance")
            print("Sucessfully set performance mode")
        if which("tlp") is not None:
            os.system("tlp set manual")
            print("Sucessfully set to Manual TLP")
        if which("tuned-adm") is not None:
            os.system("tuned-adm profile throughput-performance")
            print("TuneD set to performance")
    except PermissionError:
        print("Permission denied. Run the script with elevated privileges.")
    except FileNotFoundError:
        print(f"Process {pid} does not exist.")
    except ValueError as e:
        print(f"Error writing to OOM score adjustment file: {e}")
try:
    a = input("Disable OOM (Out-of-memory) Killer? WARNING THIS WILL CAUSE PROBLEM FOR THIS CURRENT SESSION... :").lower()
    if a in ("yes", "y",'1'):
        for i in range(10):
            time.sleep(1)
            a = 10-i
            print(f"Are you sure to proceed the process? Count Down {a}")
        target_pid=os.getpid()
        disable_oom_killer(target_pid)
        run_in_threads()
    else:
        run_in_threads() 
except KeyboardInterrupt:
    print("killed exiting...")
except ValueError:
    print("Invalid PID. Please enter a numeric value.")
