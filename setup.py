from setuptools import setup

APP = ['src/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True, # Hides the Dock icon
    },
    'packages': ['rumps', 'pynput', 'pyperclip'],
}

setup(
    app=APP,
    name='MergeCopy',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
