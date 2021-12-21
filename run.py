import os
from shutil import rmtree

import librosa
import soundfile as sf
import sys

from SpecSub import OnSpecSubstract
from codec2 import codec2_w_denoise, codec2_wo_denoise
from settings import *

if __name__ == '__main__':
    if denoising:

        # denoising
        sounds_to_denoise = os.listdir(in_dir)
        if os.path.isdir('temp'):
            rmtree('temp')
        os.makedirs('temp')
        for file in sounds_to_denoise:
            data = librosa.load(os.path.join(in_dir, file), sr=sample_rate, dtype='float64')[0]
            # print('{} loaded'.format(file))
            sf.write(os.path.join('temp', 'filtered_{}.raw'.format(file)),
                     OnSpecSubstract(data, frame_size, n_frames=noise_frames, bias=4), samplerate=sample_rate,
                     subtype='PCM_16')
            print('{} denoised'.format(file))

        # compressing
        codec2_w_denoise(out_dir)
    else:

        # compressing
        codec2_wo_denoise(in_dir, out_dir)

    rmtree('temp')
    allfiles = os.listdir(sys.path[0])
    raw_out = os.listdir(out_dir)
    for file in allfiles:
        if file.endswith('.bit'):
            os.remove(file)
    for file in raw_out:
        if file.endswith('.raw'):
            os.remove(os.path.join(out_dir, file))
