import sys
import hashlib
first_arg = sys.argv[1]
print hashlib.md5(first_arg.encode()).hexdigest()