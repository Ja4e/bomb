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

def restore_oom_killer(pid):
    try:
        oom_adj_path = f"/proc/{pid}/oom_score_adj"
        with open(oom_adj_path, "w") as file:
            file.write("0")
        print(f"Restored OOM killer for process {pid}.")
    except Exception as e:
        print(f"Failed to restore OOM killer: {e}")

try:
    target_pid=os.getpid()
    a = input("Disable OOM (Out-of-memory) Killer? WARNING THIS WILL CAUSE PROBLEM FOR THIS CURRENT SESSION... :").lower()
    if a in ("yes", "y",'1'):
        for i in range(10):
            time.sleep(1)
            a = 10-i
            print(f"Are you sure to proceed the process? Count Down {a}")
        disable_oom_killer(target_pid)
        try:
            run_in_threads()
        except:
            restore_oom_kiler(target_pid)
    else:
        run_in_threads() 
except KeyboardInterrupt:
    print("restoring oom_killer if ")
    print("killed exiting...")
except ValueError:
    print("Invalid PID. Please enter a numeric value.")
finally:
    restore_oom_killer(target_pid)
    print("Program terminated safely.")
