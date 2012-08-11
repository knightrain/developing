#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pyaudio
import wave
import threading
import time

def wav2ogg(wavefile, oggfile):
    if not os.path.isfile(wavefile):
        print "No such file: " + wavefile
        return
    cmd = "oggenc2 -Q " + wavefile + " -o " + oggfile
    os.system(cmd)

FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024
CHANNELS = 2

class record_worker(threading.Thread):
    record_stop = 0

    def __init__(self, wavfile, record_secs):
        super(record_worker, self).__init__()
        self.wavfile = wavfile
        self.record_secs = record_secs

    def do_record(self):
        p = pyaudio.PyAudio()
    
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = CHUNK)
    
        all = []
    
        for i in range(0, RATE / CHUNK * self.record_secs):
            data = stream.read(CHUNK)
            all.append(data)
            if (self.record_stop == 1) :
                break;
    
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        data = ''.join(all)
        wf = wave.open(self.wavfile, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

    def run(self):
        record_stop = 0
        self.do_record()
    
class Voice():
    def __init__(self):
        pass

    def start_record(self, wavfile, record_secs = 30):
        self.worker = record_worker(wavfile, record_secs)
        self.worker.start()

    def stop_record(self):
        self.worker.record_stop = 1
        self.worker.join()


if __name__ == "__main__":
    v = Voice()
    v.start_record("test.wav")
    time.sleep(7)
    v.stop_record()
    wav2ogg("test.wav", "test.ogg")
    os.remove("test.wav")
