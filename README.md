# 🛠️ Simple Compiler 

A lightweight code execution API for compiling and running code in a secure, sandboxed environment.

| Language | Support |
|----------|---------|
| ☕ Java   | ✅       |
| 🐍 Python | ✅      |
| 💻 C      | ✅       |

## How to run
```
git clone https://github.com/Anokxz/Compilo.git
cd Compilo
docker build -t compiler .
docker run --rm -p 8000:8000 compiler
```

Access the API docs : http://localhost:8000/docs

## Futhur Ideas
1. [ ] Handling Expected output, standard input in FastAPI
2. [ ] Job Queue
3. [ ] Logging Process
4. [ ] Response Status Code Implementation
5. [X] MultiThreading of testcase execution