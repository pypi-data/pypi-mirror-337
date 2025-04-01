# -*- coding: utf-8 -*-
"""
This module provides a thin wrapper around the wave library allowing us to
easily create and manipulate wav files.

@author: C. Andrews, A. Vaccari

Update: 2024-10-18 - Included the allowedchanges=0 option in pygame.mixer.init()
                     to solve an issue with double speed in Windows.
Update: 2024-03-26 - Updated to use pygame (simpleaudio is no longer maintained)
Update: 2022-04-20 - Added ValueError exception when trying to play an empty sound
Update: 2019-11-03 - Added support for sharps: capital letters will produce sharps
Update: 2019-04-02 - Added support for len(), removed extraneous functions
Update: 2016-08-23 - Changed play to use system tools
Update: 2016-08-22 - Converted to use __getitem__ and __setitem__

"""

import wave
import array
import pygame


# These two constants are the maximum and minimum values allowed for our samples
MAXVALUE = 32677 
MINVALUE = -32768 


class Sound:
    """
    This class is a container that holds one 'sound'. It provides an interface
    mirroring the wave library that hides some of the details such as setting the
    framerate and the sample width, as well as the interactions with the array
    library which allows us to build the sound before writing it out to a file on
    disk.
    """

    def __init__(self, framerate=44100):
        """
        Initialize the sound with a data store for our samples and a default
        sample rate of 44kHz
        """
        self.data = array.array('h')
        self.numchannels = 1
        self.framerate = framerate
        pygame.mixer.init(frequency=self.framerate, size=-16, channels=self.numchannels, allowedchanges=0)



    def __getitem__(self, index):
        """
        Get the sample at location index.
        """
        return self.data[index]

    def __len__(self):
        """
        Support the len() function.
        """
        return len(self.data)


    def __setitem__(self, index, value):
        """
        Set the value of a particular sample.
        """
        self.data[index] = value

    def append(self, sample):
        """
        Append one sample on to the end of the sound.
        """
        self.data.append(sample)

    def save(self, filename):
        """
        Save the sound as 'filename' into the current working directory.

        Under the hood, this is the point when the wav file is actually created
        and the samples are written into it.
        """
        snd = wave.open(filename, 'wb')
        # nchannels, sampwidth, framerate, nframes, comptype, compname
        snd.setparams((self.numchannels, 2, self.framerate, len(self.data), 'NONE', 'not compressed'))
        snd.writeframes(self.data.tobytes())
        snd.close()

    def play(self):
        """
        Play the sound.
        """
        # Check if the data is empty. If it is, the backend would
        # crash with an obscure message.
        if len(self.data) == 0:
            raise ValueError("Sound data empty. The sound should contain at least one sample")
        sound = pygame.mixer.Sound(self.data)
        sound.play()



def new(framerate=44100):
    """
    A convenience function for creating a new Sound object.
    """
    return Sound(framerate=framerate)


def open(filename):
    """
    Open a wave file located in 'filename' (which is assumed to be in
    the working directory, or an absolute path).
    """
    soundObj = Sound()

    snd = wave.open(filename, 'rb')
    soundObj.numchannels = snd.getnchannels()
    soundObj.framerate = snd.getframerate()
    soundObj.data.frombytes(snd.readframes(snd.getnframes()))

    snd.close()
    return soundObj

def get_frequency(note):
    """
    A quick converter for getting notes of various frequencies. This covers the
    piano keyboard.
    The sharp version of a, c, d, f, and g can be obtained using capital letters.
    """
    d = {'a':27.5,'b':30.8677,'c':32.7032,'d':36.7081,'e':41.2035,'f':43.6536,'g':48.995,
         'A':29.1353,'C':34.6479,'D':38.8909,'F':46.2493,'G':51.913}
    frequency = d[note[0]]
    octave = int(note[1])
    if note[0] > 'b':
        octave -= 1
    frequency *= 2**octave
    return frequency
