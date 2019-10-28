#coding:utf-8
import wave
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg

def spectrogram(sound):
    samples = sound.readframes(sound.getnframes())
    data = np.frombuffer(samples,dtype="int16")

    sampling_rate = sound.getframerate()
    NFFT = 44#フレームの大きさ
    OVERLAP = (NFFT / 2) #窓をずらした時のフレームの重なり
    frame_length = sound.getnframes() #wavフレームの全フレーム数
    total_time = float(frame_length) / sampling_rate
    time_unit = 1 / float(sampling_rate) #1サンプルの長さ(秒)

    #FFTのフレームの時間決め
    start = (NFFT / 2) * time_unit
    stop = total_time
    step = (NFFT - OVERLAP) * time_unit
    time_ruler = np.arange(start, stop, step)

    window = np.hamming(NFFT)

    spec = np.zeros([len(time_ruler), 1 + (NFFT / 2)])
    pos = 0

    for fft_index in range(len(time_ruler)):
        #フレームの切り出し
        frame = data[pos:pos+NFFT]
        if(len(frame) == NFFT):
            #FFTして周波数成分を求める
            windowed = window * frame
            fft_result = np.fft.rfft(windowed)
            fft_data = np.abs(fft_result)
            #specへ格納
            for i in range(len(spec[fft_index])):
                spec[fft_index][-i-1] = fft_data[i]
            #窓をずらして次のフレームへ
            pos += (NFFT - OVERLAP)
    return spec/np.max(spec)#正規化して返す

def time(sound):
    sampling_rate = sound.getframerate()
    NFFT = 44#フレームの大きさ
    OVERLAP = (NFFT / 2) #窓をずらした時のフレームの重なり
    frame_length = sound.getnframes() #wavフレームの全フレーム数
    total_time = float(frame_length) / sampling_rate
    time_unit = 1 / float(sampling_rate) #1サンプルの長さ(秒)

    #FFTのフレームの時間決め
    start = (NFFT / 2) * time_unit
    stop = total_time
    step = (NFFT - OVERLAP) * time_unit
    time_ruler = np.arange(start, stop, step)
    return time_ruler

def ssd(spec, t_spec):
    W,H = spec.shape
    w,h = t_spec.shape

    ssd = np.zeros(W-w)

    for x in range(W-w):
        ssd[x] = np.sum((spec[x:x+w,] - t_spec)**2)
    min = ssd[0]
    pos = 0
    for i in range(1,len(ssd)):
        if(ssd[i]<min):
            min = ssd[i]
            pos = i
    return pos

# sound = wave.open('sound/timing_5kHz/fruits_08.wav', "rb")
# print(sound.getnchannels())
# r_spec = spectrogram(sound)#応答信号のスペクトログラム
# sound.close()
# timing = wave.open('sound/timing_5kHz/noise_07.wav', "rb")
# timing_spec = spectrogram(timing)#タイミング音のスペクトログラム
# timing.close()
#
# template = wave.open('sound/timing_5kHz/5kHz.wav', "rb")
# t_spec = spectrogram(template)#入力信号のスペクトログラム
# template.close()

sound = wave.open('sound/timing_5kHz/fruits_08.wav', "rb")
print(sound.getnchannels())
r_spec = spectrogram(sound)#応答信号のスペクトログラム
sound.close()
timing = wave.open('sound/timing_5kHz/noise_07.wav', "rb")
timing_spec = spectrogram(timing)#タイミング音のスペクトログラム
timing.close()

template = wave.open('5kHz.wav', "rb")
t_spec = spectrogram(template)#入力信号のスペクトログラム
template.close()


time = time(sound)
r_pos = ssd(r_spec, t_spec)
t_pos = ssd(timing_spec, t_spec)


print(time[r_pos])
print(time[t_pos])
print(time[r_pos] - time[t_pos]) #反響音の伝播時間の遅れを出力
