from setuptools import setup

APP = ['main.py']
DATA_FILES = [('assets', [
    'assets/cover.jpg',
    'assets/disk.png',
    'assets/pause.png',
    'assets/play.png',
    'assets/stop.png'
])]
OPTIONS = {
    'argv_emulation': True
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
