import time
import subprocess

def compile_code(command: str) -> dict :
    # Test Compilation
    start = time.time() 
    process = subprocess.run(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    duration = time.time() - start
    
    result = {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "duration" : duration,
            "return_code": process.returncode,
    }

    # Compilation Failure
    if process.returncode != 0 :
        result["status"] = "Compilation Error"
    else :
        result["status"] = "Compilation Success"
    
    return result
