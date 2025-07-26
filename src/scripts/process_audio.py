import numpy as np
import sys
from scipy.io import wavfile

def loadFile(file_path):
    filename = file_path.stem
    try:
        fs, data = wavfile.read(file_path)
        data = data.astype(np.float32) / 32768.0

    except Exception as e:
        print(f"Error loading {filename} from {file_path}: {e}")
        return None, None
    return filename, (data,fs)


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_audio.py <wav_file>")
        sys.exit(1)
    wav_path = sys.argv[1]
    fs, data = wavfile.read(wav_path)
    print(f"Sample rate: {fs}, Data shape: {data.shape}")

if __name__ == "__main__":
    main()