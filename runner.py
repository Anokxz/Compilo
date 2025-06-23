import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_testcase(command: str, testcase: str) -> dict :
    
    try:  
        start = time.time()
        run_process = subprocess.run(
            command.split(),
            input=testcase,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        duration = time.time() - start
        return {
            "stdout": run_process.stdout.strip(),
            "stderr": run_process.stderr.strip(),
            "exit_code": run_process.returncode,
            "execution_time" : duration,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "exit_code": 124,
        }
    # For Debugging 
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Type of error: {type(e)}")
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
        }

def run_all_testcases(command: str, testcases: list) -> list :

    worker_count = len(testcases)
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(
            executor.map(
                lambda tc: run_testcase(command, tc), testcases
            )
        )
    
    return results