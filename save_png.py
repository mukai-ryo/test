#coding:utf-8
import wave
import numpy as np
import matplotlib.pyplot as plt

def high_pass_filter(sound_data, sampling_rate):
    fft = np.fft.fft(sound_data)
    freq = np.fft.fftfreq(len(sound_data), 1.0/sampling_rate)
    fft[(freq < 100)] = 0
    ift = np.fft.ifft(fft) * len(sound_data)
    return ift

sound = wave.open('apple_practice_data/heating/heat/5kHz/apple1/apple_43.wav', "rb")
samples = sound.readframes(sound.getnframes())
data = np.frombuffer(samples,dtype="int16")
if(sound.getnchannels()==2):#stereoの場合
    #stereo分割
    trans = data[0::2]#left_data
    original = data[1::2]#right_data

sampling_rate = sound.getframerate()
sound.close()

t_sound = wave.open('apple_practice_data/template_5kHZ.wav', "rb")
samples = t_sound.readframes(t_sound.getnframes())
template = np.frombuffer(samples,dtype="int16")
t_sound.close()

trans_cut = high_pass_filter(trans, sampling_rate)

print(len(trans))
print(len(trans_cut))

plt.plot(trans_cut)
plt.show()
