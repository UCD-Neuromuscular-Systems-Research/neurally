import sys
from scipy.io import wavfile

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_audio.py <wav_file>")
        sys.exit(1)
    wav_path = sys.argv[1]
    fs, data = wavfile.read(wav_path)
    print(f"Sample rate: {fs}, Data shape: {data.shape}")

if __name__ == "__main__":
    main()