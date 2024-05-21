#pip install pyaudio, wave, array 
import pyaudio
import wave
from array import array
import time 

def listen(listening):
    chunk = 1024  
    sample_format = pyaudio.paInt16  
    channels = 1
    fs = 44100  
    filename = "output.wav"
    p1 = pyaudio.PyAudio()  
    stream1 = p1.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    p2 = pyaudio.PyAudio()
    stream2 = p1.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  
    while listening:
        int_compare = array('h', stream2.read(chunk))
        vol = max(int_compare)
        print(vol)
        if vol >= 2000:
            time.sleep(0.5)
            while vol >= 500:
                int_compare = array('h', stream2.read(chunk))
                vol = max(int_compare)
                print(vol)
                data = stream1.read(chunk)
                frames.append(data)
            break
    stream1.stop_stream()
    stream1.close()
    p1.terminate()
    stream2.stop_stream()
    stream2.close()
    p2.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p1.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
