import os
import numpy as np
import scipy
from scipy.io import wavfile
import scipy.fftpack as fft
from scipy.signal import get_window
import librosa


def mfcc(path, frame_length, frame_shift, num_mel_bins, sample_rate=16000):
    audio, sample_rate = librosa.load(path, sr=sample_rate)
    print("Audio Path: " + path)
    print("Sample rate: {0}Hz".format(sample_rate))
    print("Audio duration: {0}s".format(len(audio) / sample_rate))

    print("frame_length: {0}".format(frame_length))
    print("frame_shift: {0}ms".format(frame_shift))
    print("num_mel_bins: {0}".format(num_mel_bins))

    audio = normalize_audio(audio)

    audio_framed = frame_audio(
        audio, FFT_size=frame_length, hop_size=frame_shift, sample_rate=sample_rate)
    print("Framed audio shape: {0}".format(audio_framed.shape))

    # convert to frequency domain (from time domain) using hamming window
    window = get_window("hann", frame_length, fftbins=True)
    audio_win = audio_framed * window
    audio_winT = np.transpose(audio_win)

    audio_fft = np.empty(
        (int(1 + frame_length // 2), audio_winT.shape[1]), dtype=np.complex64, order='F')

    for n in range(audio_fft.shape[1]):
        audio_fft[:, n] = fft.fft(audio_winT[:, n], axis=0)[
            :audio_fft.shape[0]]

    audio_fft = np.transpose(audio_fft)

    # calculate signal power
    audio_power = np.square(np.abs(audio_fft))
    freq_min = 0

    freq_high = sample_rate / 2

    filter_points, mel_freqs = get_filter_points(
        freq_min, freq_high, num_mel_bins, frame_length, sample_rate=sample_rate)
    filters = get_filters(filter_points, frame_length)
    enorm = 2.0 / (mel_freqs[2:num_mel_bins+2] - mel_freqs[:num_mel_bins])
    filters *= enorm[:, np.newaxis]

    # filter the signal
    audio_filtered = np.dot(filters, np.transpose(audio_power))
    audio_log = 10.0 * np.log10(audio_filtered)

    dct_filter_num = 13
    dct_filters = dct(dct_filter_num, num_mel_bins)

    cepstral_coefficents = np.dot(dct_filters, audio_log)
    cepstral_coefficents.shape
    return cepstral_coefficents


# generate the Cepstral Coefficents
def dct(dct_filter_num, filter_len):
    basis = np.empty((dct_filter_num, filter_len))
    basis[0, :] = 1.0 / np.sqrt(filter_len)

    samples = np.arange(1, 2 * filter_len, 2) * np.pi / (2.0 * filter_len)

    for i in range(1, dct_filter_num):
        basis[i, :] = np.cos(i * samples) * np.sqrt(2.0 / filter_len)

    return basis


# normalize_audio is used to normalize audio low pass filter (LPF) based on Nyquist zone
def normalize_audio(audio):
    audio = audio / np.max(np.abs(audio))
    return audio


# frame_audio divide by frame size FFT (Fast Fourier transform) with hop_size(frame_shift)
def frame_audio(audio, FFT_size=2048, hop_size=10, sample_rate=44100):
    # hop_size in ms

    audio = np.pad(audio, int(FFT_size / 2), mode='reflect')
    frame_len = np.round(sample_rate * hop_size / 1000).astype(int)
    frame_num = int((len(audio) - FFT_size) / frame_len) + 1
    frames = np.zeros((frame_num, FFT_size))

    for n in range(frame_num):
        frames[n] = audio[n*frame_len:n*frame_len+FFT_size]

    return frames


# compute filter points
def freq_to_mel(freq):
    return 2595.0 * np.log10(1.0 + freq / 700.0)


def met_to_freq(mels):
    return 700.0 * (10.0**(mels / 2595.0) - 1.0)


def get_filter_points(fmin, fmax, mel_filter_num, FFT_size, sample_rate=44100):
    fmin_mel = freq_to_mel(fmin)
    fmax_mel = freq_to_mel(fmax)

    print("MEL min: {0}".format(fmin_mel))
    print("MEL max: {0}".format(fmax_mel))

    mels = np.linspace(fmin_mel, fmax_mel, num=mel_filter_num+2)
    freqs = met_to_freq(mels)

    return np.floor((FFT_size + 1) / sample_rate * freqs).astype(int), freqs

# construct the filterbank


def get_filters(filter_points, FFT_size):
    filters = np.zeros((len(filter_points)-2, int(FFT_size/2+1)))

    for n in range(len(filter_points)-2):
        filters[n, filter_points[n]: filter_points[n + 1]
                ] = np.linspace(0, 1, filter_points[n + 1] - filter_points[n])
        filters[n, filter_points[n + 1]: filter_points[n + 2]
                ] = np.linspace(1, 0, filter_points[n + 2] - filter_points[n + 1])

    return filters
