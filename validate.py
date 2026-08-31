import compileall
import subprocess
import sys

print("[1/2] Compiling Python sources...")
if not compileall.compile_dir(".", quiet=1):
    raise SystemExit("Python compile validation failed.")

print("[2/2] Running local unit tests...")
result = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
)
raise SystemExit(result.returncode)
