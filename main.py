from fastapi import FastAPI
from models import InputJson
from fastapi.responses import JSONResponse
import os
import subprocess
import time
import uuid
import shutil

app = FastAPI()

def java_compile(file_name, file_path, testcases):
    os.chdir(file_path) 
    # Test Compilation
    process = subprocess.run(
        ["javac", file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Compilation Failure
    if process.returncode != 0:
        return {
            "status": 400,
            "error": "Compilation Error",
            "details": process.stderr
    }

    # Check Test Cases
    results = []
    try:
        for testcase in testcases:
            start = time.time()
            run_process = subprocess.run(
                ["java", "-cp", ".", file_name],
                input=testcase,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            duration = time.time() - start
            results.append({
                "stdout": run_process.stdout.strip(),
                "stderr": run_process.stderr.strip(),
                "exit_code": run_process.returncode,
                "execution_time" : duration,
            })
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
    
    return results

def python_compile(file_name, file_path, testcases):
    os.chdir(file_path)
    results = []
    # Direct Execution 
    for testcase in testcases:
        try:
            start = time.time()
            run_process = subprocess.run (
                ["python3", file_name],
                input=testcase,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )

            duration = time.time() - start

            if (run_process.returncode != 0):
                return {
                    "status": 400,
                    "error": "During Execution Of Python",
                    "details": run_process.stderr.strip(),
                    "return code": run_process.returncode
                }
            
            results.append(
                {
                    "stdout": run_process.stdout.strip(),
                    "stderr": run_process.stderr.strip(),
                    "exit_code": run_process.returncode,
                    "execution_time" : duration,
                }
            )
        
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Execution timed out",
                "exit_code": 124,
            }
        except Exception as e:
            # For Debugging other Errors
            print("Error : ", e)
        
        
        return results

@app.post("/")
def compile(input_json: InputJson):
    language = input_json.language.lower()

    languages = {
        "py"  : { "file_name" : "main.py", "command" : "python"}, 
        "c"   : { "file_name" : "main.c", "command" : "gcc"}, 
        "java": { "file_name" : "Main.java", "command" : "javac"}
    }

    if language not in languages:
        return JSONResponse(
            status_code=400,
            content={"status": 400, "problem": "language not supported"}
        )

    file_name = languages[language]["file_name"]
    job_id = str(uuid.uuid4())
    file_path = f"/tmp/{job_id}"
    os.makedirs(file_path, exist_ok=True)


    with open(f"{file_path}/{file_name}", 'w') as file:
        file.write(input_json.code)
    
    # Default return for supported language 
    responseJson = {"status": 200, "message": "language support will be implemented soon"}

    if (language == "java"):
        responseJson = java_compile(file_name, file_path, input_json.testcases)
    elif (language == "py"):
        responseJson = python_compile(file_name, file_path, input_json.testcases)
    elif (language == "c"):
        responseJson = python_compile(file_name, file_path, input_json.testcases)
    else:
        # Not possible due to previous check
        pass

    # Cleanup 
    shutil.rmtree(file_path)

    return responseJson