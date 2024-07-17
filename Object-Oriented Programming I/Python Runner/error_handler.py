import sys
import runpy

try:
    runpy.run_path('main.py')
except EOFError as eof_error:
    pass
except Exception as e:
    sys.stderr.write(str(e) + '\n')
