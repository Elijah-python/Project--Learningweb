#!C:\Users\Administrator\PycharmProjects\learningweb\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'flasker==0.1.45','console_scripts','flasker'
__requires__ = 'flasker==0.1.45'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('flasker==0.1.45', 'console_scripts', 'flasker')()
    )
