import os

path = 'P:\\programming\\projects\\college hub\\files\\1\\CSE\\1\\BEE'

if os.access(path, os.R_OK):
    # The script has read permission, so it's safe to access the directory
    files = [f for f in os.scandir(path) if f.is_file() or f.is_dir()]
    #...
else:
    print("Permission denied: ", path)