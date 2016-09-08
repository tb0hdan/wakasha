import subprocess

class Action(object):
    def __init__(self):
        pass

    def run(self):
        subprocess.call(['open', 'https://www.google.com.ua/search?safe=off&site=&tbm=isch&q=maine+coon'])
