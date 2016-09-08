#-*- coding: utf-8 -*-

# standard imports
import os
import re
import zipfile
import sys
import signal
import shutil
import tempfile

# local imports
from wakasha.action import Action
from wakasha.extlib.snowboydetect.snowboydecoder import HotwordDetector


class Wakasha(object):
    '''
    Wakasha class :-)
    '''
    model = 'model.pmdl'
    extract_list = ['common.res', 'model.pmdl']

    def __init__(self):
        self.interrupted = False
        self.tmpdir = tempfile.mkdtemp()
        self.path =  os.path.dirname(os.path.abspath(__file__))
        self.appdir = re.sub('/Contents/Resources(.+)$', '', self.path)
        self.site_packages = re.sub('\.zip/(.+)$', '.zip', self.path)
        #
        self.detector = None
        self.action = Action()

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def configure(self):
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        zf = zipfile.ZipFile(self.site_packages, 'r')
        for fname in  zf.namelist():
            res_fname = re.sub('(.+)/', '', fname)
            if res_fname in self.extract_list:
                with open(os.path.join(self.tmpdir, res_fname), 'wb') as dest:
                    dest.write(zf.read(fname))
            if res_fname in ['com.example.wakasha.plist']:
                plist = os.path.abspath(os.path.expanduser('~/Library/LaunchAgents/com.example.wakasha.plist'))
                if os.path.exists(plist):
                    continue
                with open(plist, 'wb') as dest:
                    dest.write(zf.read(fname))

        self.detector = HotwordDetector(os.path.join(self.tmpdir, self.model),
                                        resource=os.path.join(self.tmpdir, 'common.res'),
                                        sensitivity=0.5)

    def run(self):
        print('Listening... Press Ctrl+C to exit')
        # main loop
        self.detector.start(detected_callback=self.action.run,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.03)
        self.detector.terminate()
        self.cleanup()

    def cleanup(self):
        shutil.rmtree(self.tmpdir)


def main():
    wakasha = Wakasha()
    wakasha.configure()
    wakasha.run()
