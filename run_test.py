#!/usr/bin/env python
import env
from unittest import TextTestRunner
from unittest.loader import defaultTestLoader

if __name__ == '__main__':
    suite = defaultTestLoader.discover(start_dir='./tests')
    TextTestRunner(verbosity=2).run(suite)
