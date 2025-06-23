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
    
    # Compilation Failure
    if process.returncode != 0 :
        return {
            "status": 400,
            "error": "Compilation Error",
            "details": process.stderr,
            "return_code": process.returncode,
    }

    else :
        return {
            "status" : 200,
            "details": process.stdout,
            "return_code" : process.returncode,
            "duration" : duration,
        }
