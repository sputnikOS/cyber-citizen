import distutils.core
import setup
import p2exe

setup(options = {'p2exe': {'bundle_files': 1, 'compressed': True}},windows = [{'script': "logger.py"}],zipfile = None)