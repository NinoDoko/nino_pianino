from setuptools import setup
import os
import subprocess
import argparse

def main():
    required_packages = ['fluidsynth', 'lame']
    for package in required_packages: 
        subprocess.call(['apt-get', 'install', package])

    if os.environ.get('GET_SOUNDFONT'): 
        subprocess.call(['mkdir', 'soundfonts'])
        subprocess.call(['wget', 'ftp://sourceforge.nchc.org.tw/a/an/androidframe/soundfonts/FluidR3_GM.sf2'])
        subprocess.call(['mv', 'FluidR3_GM.sf2', 'soundfonts'])

    setup(
        name = 'ninopianino',
        packages = ['ninopianino'],
        version = '0.1.8', 
        description = 'Programmable music generator. ', 
        author = 'Nikola Dokoski', 
        author_email = 'ninodokoskiot@hotmail.com', 
        url = 'https://github.com/NinoDoko/nino_pianino', 
        download_url = 'https://github.com/NinoDoko/nino_pianino/tarball/0.1',
        scripts = ['ninopianino/pianize'],
        install_requires = [
            'pyhaikunator',
            'midiutil',
            ]
        )


main()
