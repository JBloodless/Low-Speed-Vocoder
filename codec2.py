import os
import subprocess
from shutil import rmtree

import librosa
import soundfile as sf
import sys
import time

from settings import *


def codec2_w_denoise(out_dir):
    source = sys.path[0]
    if os.path.isdir(out_dir):
        rmtree(out_dir)
    os.makedirs(out_dir)
    filtered = os.listdir('temp')
    for file in filtered:
        subprocess.call([os.path.join(source, "c2enc"), str(codec_speed), os.path.join(source, "temp/{}".format(file)),
                         os.path.join(source, "{}.bit").format(file)])
        subprocess.call([os.path.join(source, "c2dec"), str(codec_speed), os.path.join(source, "{}.bit").format(file),
                         os.path.join(source, out_dir, "{0}_c2_{1}.raw".format(file, codec_speed))])
        time.sleep(0.1)
        raw = sf.read(os.path.join(source, out_dir, "{0}_c2_{1}.raw".format(file, codec_speed)), channels=1,
                      samplerate=sample_rate, subtype='PCM_16')[0]
        sf.write(os.path.join(out_dir, "{0}_c2_{1}.wav".format(file, codec_speed)), raw, samplerate=sample_rate)
        print(file[:-4], 'compressed with mode {}'.format(codec_speed))


def codec2_wo_denoise(in_dir, out_dir):
    source = sys.path[0]
    if os.path.isdir(out_dir):
        rmtree(out_dir)
    os.makedirs(out_dir)
    if os.path.isdir('temp'):
        rmtree('temp')
    os.makedirs('temp')
    audios = os.listdir(in_dir)
    filtered = []
    for audio in audios:
        data = librosa.load(os.path.join(source, in_dir, audio), sr=sample_rate, dtype='float64')[0]
        print('{} loaded'.format(audio))
        sf.write(os.path.join('temp', '{}.raw'.format(audio)),
                 data, samplerate=sample_rate, subtype='PCM_16')
        filtered.append('{}.raw'.format(audio))
    for file in filtered:
        subprocess.call(
            [os.path.join(source, "c2enc"), str(codec_speed), os.path.join(source, 'temp', "{}".format(file)),
             os.path.join(source, "{}.bit").format(file)])
        subprocess.call([os.path.join(source, "c2dec"), str(codec_speed), os.path.join(source, "{}.bit").format(file),
                         os.path.join(source, out_dir, "{0}_c2_{1}.raw".format(file, codec_speed))])
        raw = sf.read(os.path.join(source, out_dir, "{0}_c2_{1}.raw".format(file, codec_speed)), channels=1,
                      samplerate=sample_rate, subtype='PCM_16')[0]
        sf.write(os.path.join(out_dir, "{0}_c2_{1}.wav".format(file, codec_speed)), raw, samplerate=sample_rate)
        print(file[:-4], 'compressed with mode {}'.format(codec_speed))


if __name__ == '__main__':
    # codec2_w_denoise(out_dir)
    codec2_wo_denoise(in_dir, out_dir)

# c2enc 2400 /temp/filtered_heli_v2.wav.raw filtered_heli_v2.bit
# c2dec 2400 filtered_heli_v2.bit output/filtered_heli_v2_c2_2400.raw
