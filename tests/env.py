import sys, os
path = os.path.dirname(__file__)
abs_path = os.path.abspath(path)
rel_path = os.path.dirname(abs_path)
sys.path.insert(0, rel_path + '/lib')
sys.path.insert(0, rel_path + '/app')
sys.path.insert(0, rel_path)
print abs_path
print rel_path



