from riposte import Riposte
from bs4 import BeautifulSoup
import requests
import sys
import re
import os

BANNER = """
 _     _       _                
| |   (_)_ __ | | ___ __  _   _ 
| |   | | '_ \| |/ / '_ \| | | |
| |___| | | | |   <| |_) | |_| |
|_____|_|_| |_|_|\_\ .__/ \__, |
                   |_|    |___/ 

                   Made by Konradas Bunikis
                   Please do not use this tool for malicious purposes.
"""

repl = Riposte('Linkpy > ', banner=BANNER)

class Application:
    def __init__(self):
        self.target = None

app = Application()

@repl.command('set')
def set_command(variable: str, value: str):
    if variable == 'TARGET':
        app.target = value
        repl.success('Set TARGET to %s' % app.target)

@repl.command('run')
def run_command():
    if app.target is not None:
        repl.info('Fetching %s' % app.target)
        response = requests.get(app.target)
        if response.status_code == 200:
            repl.info('Searching for links...')
            soup = BeautifulSoup(response.content, features='html.parser')
            # <a> http
            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                repl.success('Found: %s' % link['href'])
        else:
            repl.error('Failed to fetch %s' % app.target)
    else:
        repl.error('TARGET is None. Please set the TARGET. Use: set TARGET <argument>')

repl.run()
