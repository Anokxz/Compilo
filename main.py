from fastapi import FastAPI
from models import InputJson, OutputJson
from fastapi.responses import JSONResponse
import os
import subprocess
import time
import uuid
import shutil
import sys

# Import compile function from compiler.py
import compiler 
# Import runner function for running testcases
import runner

app = FastAPI()

# Valid Languages
languages = {
    "py"  : { "file_name" : "main.py", "run_command" : "python3"}, 
    "c"   : { "file_name" : "main.c", "compile_command" : "gcc", "run_command": ""}, 
    "java": { "file_name" : "Main.java", "compile_command" : "javac", "run_command": "java -cp"}
}


@app.post("/", response_model=OutputJson)
def main(input_json: InputJson, first_run: bool = True) -> dict:
    language = input_json.language.lower()

    if language not in languages:
        return {
                "status": "language not supported",
                "compilation":  {},
                "testcases" : []
        }
    
    random_folder = str(uuid.uuid4())
    file_path = f"/tmp/{random_folder}"
    os.makedirs(file_path, exist_ok=True)

    file_name = languages[language]["file_name"]
    with open(f"{file_path}/{file_name}", 'w') as file:
        file.write(input_json.code)
    
    full_path = os.path.join(file_path, file_name)
    if (language == "java"):
        compile_command = f"javac {full_path}"
        compile_result = compiler.compile_code(compile_command)

        #Checking for Compiling Error
        if compile_result["return_code"] != 0:
            return compile_result
        
        class_name = class_name = os.path.splitext(file_name)[0]
        run_command = f"java -cp {file_path} {class_name}"     
    elif (language == "py"):
        compile_result = {}
        run_command = f"python3 {full_path}"
        run_testcases_result = runner.run_all_testcases(run_command, input_json.testcases)
    elif (language == "c"):
        executable = f"{file_path}/{os.path.splitext(file_name)[0]}"
        compile_command = f"gcc {full_path} -o {executable}"
        compile_result = compiler.compile_code(compile_command)

        #Checking for Compiling Error
        if compile_result["return_code"] != 0:
            return {
                    "status" : "Compiler Error",
                    "compilation":  compile_result,
                    "testcases" : []
            }

        run_command = f"{executable}"
        run_testcases_result = runner.run_all_testcases(run_command, input_json.testcases)
    else:
        # Not possible due to previous check
        pass

    # Check the result for TimeLimit or Error
    for result in run_testcases_result:
        if (result["return_code"] != 0):
            ''' *** Expermental Feature ***
            This may cause infinite recurison 
            If there is error handling of ModuleNotFoundError of user_code
            Restrict User of Error Handling or
            Using first_run flag to stop with one try or
            Let me know if there is better way [ Happy to Learn : ) ]
            '''
            #Checking for Python ModuleNotFoundError
            if first_run and "ModuleNotFoundError" in result["stderr"]:
                module_name = result["stderr"].split()[-1][1:-1] # Little Magic to get the module
                install_process = subprocess.run(
                    f"pip install {module_name}".split(), # f"{sys.executable} -m pip install {module_name}".split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                return main(input_json, first_run=False)

    # Cleanup 
    shutil.rmtree(file_path)
    
    return {
            "status" : "Success",
            "compilation" : compile_result,
            "testcases" : run_testcases_result
    }
