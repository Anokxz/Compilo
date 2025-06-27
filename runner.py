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
            "stdout": run_process.stdout,
            "stderr": run_process.stderr,
            "return_code": run_process.returncode,
            "execution_time" : duration,
        }
    except subprocess.TimeoutExpired as processError:
        return {
            "stdout": processError.stdout or "",
            "stderr": "ExecutionTimeOut",
            "execution_time": processError.timeout,
            "return_code": 124,
        }
    # For Debugging 
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Type of error: {type(e)}")
        return {
            "stdout": run_process.stdout,
            "stderr": str(e),
            "return_code": -2,
        }

def run_all_testcases(command: str, testcases: list) -> list :
    max_thread_count = 50
    worker_count = len(testcases)
    
    # Test Case Limit
    if (worker_count > max_thread_count):
        return [{
            "stdout": "",
            """
                This is acutally not a Standard Error,
                It's Just Simple this way :) - Anokxz

            """
            "stderr": f"Number of testcase limit should be less than {max_thread_count}",
            "return_code": -1,
        }]

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(
            executor.map(
                lambda tc: run_testcase(command, tc), testcases
            )
        )
    
    return results