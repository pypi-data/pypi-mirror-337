from setuptools import setup
from pathlib import Path
longDescription = (Path(__file__).parent / "README.md").read_text()

setup(
    name='portsManager',
    version='0.1.3',
    packages=['pManager', 'pManager.modules', 'pManager.dataModels'],
    url='https://github.com/Qwantman/pManager',
    license='GPL-3.0',
    author='Qwantman',
    author_email='svr0116@gmail.com',
    description='Library to work with .qpmgr files',
    long_description=longDescription,
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    programming_language='python3'
)
