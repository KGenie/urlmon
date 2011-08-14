import sys, os
path = os.path.dirname(__file__)
abs_path = os.path.abspath(path)
sys.path.insert(0, abs_path + '/lib')
sys.path.insert(0, abs_path + '/app')
sys.path.insert(0, abs_path)
