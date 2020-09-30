# Coding Task MFCC

Repo ini dibuat untuk menyelesaikan task dari Prosa diposisi Backend Engineer Speech. Namun, task ini belum selesai sepenuhnya dan menggunakan beberapa library yang sudah ada. seperti proses Hamming window menggunakan ```scipy.signal```.

# How To Use

Jalankan di terminal 
```
  python3 cli.py mfcc -f audio_sample.wav -fl 2048 -fs 10 -nmb 20
```
-f : /path/to/file <br>
-fl : frame_length <br>
-fs : frame_shift <br>
-nmb : num_mel_bins 

Lalu akan muncul hasil mfcc di terminal.

Silahkan gunakan ```python3 cli.py mfcc --help``` untuk bantuan
# Referensi
- Kaggle [MFCC theory and implementation](https://www.kaggle.com/ilyamich/mfcc-implementation-and-tutorial)
- Youtube [Understanding audio data for deep learning](https://www.youtube.com/watch?v=m3XbqfIij_Y)
- Youtube [Preprocessing audio data for Deep Learning](https://www.youtube.com/watch?v=Oa_d-zaUti8)
- practicalcryptography [Mel Frequency Cepstral Coefficient (MFCC) tutorial](http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)