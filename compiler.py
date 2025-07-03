import time
import subprocess
from models import CompilerResult

def compile_code(command: str) -> CompilerResult:
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
    
    return result
