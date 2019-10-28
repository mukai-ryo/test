#coding:utf-8
import wave
import numpy as np
import matplotlib.pyplot as plt

def spectrogram(sound_data, sampling_rate, window_size, overlap):

    frame_length = len(sound_data) #wavフレームの全フレーム数
    step = int(frame_length / (window_size - overlap)) #分割数
    step_size = window_size - overlap #1分割のサイズ

    spectrogram = []

    for count in range(step-1):
        piv = count * step_size
        wave_cal = sound_data[piv:piv+window_size] * np.hamming(window_size)
        spec = np.abs(np.fft.fft(wave_cal, window_size))[:int(window_size/2) ]
        spectrogram.append(spec)

    spectrogram = np.array(spectrogram)
    return spectrogram/np.max(spectrogram)#正規化して返す

def start_pos_search(spec, t_spec):
    W = len(original_spec)
    w = len(template_spec)

    ssd = np.zeros(W-w)

    for x in range(W-w):
        ssd[x] = np.sum((spec[x:x+w] - t_spec)**2)

    start_pos = ssd.argmin()
    return start_pos


#ファイル展開
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

original_spec = spectrogram(original, sampling_rate, 256, 128)
template_spec = spectrogram(template, sampling_rate, 256, 128)


# template matching
start_pos = start_pos_search(original_spec, template_spec)
print(start_pos)
