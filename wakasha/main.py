import os
import re
import zipfile
import sys
import signal
import shutil
import tempfile

from wakasha.extlib.snowboydetect.snowboydecoder import HotwordDetector, play_audio_file


interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = 'model.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def main():
    tmpdir = tempfile.mkdtemp()
    path =  os.path.dirname(os.path.abspath(__file__))
    appdir = re.sub('/Contents/Resources(.+)$', '', path)
    site_packages = re.sub('\.zip/(.+)$', '.zip', path)
    zf = zipfile.ZipFile(site_packages, 'r')
    extract_list = ['common.res', 'model.pmdl', 'ding.wav']
    for fname in  zf.namelist():
        res_fname = re.sub('(.+)/', '', fname)
        if res_fname in extract_list:
            with open(os.path.join(tmpdir, res_fname), 'wb') as dest:
                dest.write(zf.read(fname))

    detector = HotwordDetector(os.path.join(tmpdir, model), resource=os.path.join(tmpdir, 'common.res'),
                               sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')

    cb = lambda: play_audio_file(os.path.join(tmpdir, 'ding.wav'))
    # main loop
    detector.start(detected_callback=cb,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

    detector.terminate()
    shutil.rmtree(tmpdir)
