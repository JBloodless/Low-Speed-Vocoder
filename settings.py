"""
    absolute or relative path to directory with input files and where denoised will be stored
"""
in_dir = 'input'
out_dir = 'output'

"""
    on/off denoising
"""
denoising = True

"""
    parameters of denoising and codec. Keep in mind that time dimension of frame depends on sample rate AND frame size
"""
sample_rate = 8000
frame_size = 1024
noise_frames = 4

codec_speed = 1600
