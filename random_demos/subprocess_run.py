import subprocess

result = subprocess.run("git status", shell=True)

print(f"result: {result}")
print(f"return code: {result.returncode}")

result = subprocess.run("gite status", shell=True)

print(f"result: {result}")
print(f"return code: {result.returncode}")