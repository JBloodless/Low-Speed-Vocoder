from pesq import pesq
import numpy as np
import librosa
import soundfile as sf
import os
from settings import *
from matplotlib import pyplot as plt
from SpecSub import OnSpecSubstract


def mixing(in_audio, noise, snr):
    source = librosa.load(in_audio, sr=8000)[0]
    noise = librosa.load(noise, sr=8000)[0]
    source = source[:len(noise)]
    As = np.mean(source)
    An = np.mean(noise[:])
    k = As / (An * (10 ** (snr / 20)))
    mix = source + k * noise
    sf.write('snr_pesq_eval/{}.wav'.format(snr), mix, samplerate=8000)


def pesq_eval(in_audio, clean_in, snr):
    noised = librosa.load(in_audio, sr=8000)[0]
    clean = librosa.load(clean_in, sr=8000)[0]
    clean = clean[:len(noised)]
    # print(pesq(8000, clean, noised, 'nb'))
    denoised = OnSpecSubstract(noised, frame_size, n_frames=noise_frames, bias=4)
    clean = clean[(4 * frame_size - frame_size // 2):]
    # print(len(denoised)-len(clean))
    sf.write('snr_pesq_eval/denoised_{0}_frame_size{1}_noise_frames{2}.wav'.format(snr, frame_size, noise_frames),
             denoised, samplerate=8000)
    sf.write('snr_pesq_eval/clean_crop.wav', clean, samplerate=8000)
    print(pesq(8000, clean, denoised, 'nb'))
    # plt.subplot(2,1,1)
    # plt.plot(clean[4063:])
    # plt.subplot(2,1,2)
    # plt.plot(denoised)
    # plt.show()


if __name__ == '__main__':
    for i in range(-20, 10):
        # mixing('snr_pesq_eval/cleanv2.wav', 'snr_pesq_eval/helicopter4.wav', i)
        pesq_eval('snr_pesq_eval/{}.wav'.format(i), 'snr_pesq_eval/cleanv2.wav', i)
