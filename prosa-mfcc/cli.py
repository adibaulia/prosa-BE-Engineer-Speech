import extract
import fire


def preproccessing(f: str, fl: int, fs: int, nmb: int):
    """
    Returns MFCC Matrix N x 13
    :param f: path of the file
    :param fl: the frame_length wanted
    :param fs: the frame_shift wanted
    :param nmb: the num_mel_bins wanted
    :return: MFCC Matrix N x 13
    """
    #res = mfcc.mfcc("audio_sample.wav", 2048, 10, 20)
    res = extract.mfcc(f, fl, fs, nmb)
    print("mfcc extracted : ", res)


if __name__ == "__main__":
    fire.Fire({
        "mfcc": preproccessing
    })
