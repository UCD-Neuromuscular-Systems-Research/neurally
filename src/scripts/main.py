import os
import sys
import json
from pathlib import Path
import time
import csv

sys.path.append(str(Path(__file__).parent / "HD"))

# Import HD scripts
import HD.audioProcessingHDLongitudinal as audio_processing

def validate_audio_file(file_path):
    """Audio file validation"""
    
    if not os.path.exists(file_path):
        return False, f"Audio file not found: {file_path}"

    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"

    file_extension = Path(file_path).suffix.lower()
    valid_extensions = ['.wav']

    if file_extension not in valid_extensions:
        return False, f"Invalid file format: {file_extension}. Only .wav files are supported."

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return False, f"Audio file is empty: {file_path}"

    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)
            if len(header) < 12:
                return False, f"File too small to be a valid WAV file: {file_path}"

            if header[:4] != b'RIFF':
                return False, f"File is not a valid WAV file: {file_path}"

    except Exception as e:
        return False, f"Cannot read audio file: {file_path}"

    return True, "File is valid"


def process_audio(file_path, test_type):
    """Process single audio file for specific test type (SV, SR, PR)"""
    try:
        # Input validation
        is_valid, message = validate_audio_file(file_path)
        if not is_valid:
            return {"error": message}

        if test_type not in ["SV", "SR", "PR"]:
            return {"error": f"Invalid test type: {test_type}. Must be SV, SR, or PR."}

        # Set up paths for single file processing
        current_dir = Path(__file__).parent
        output_dir = current_dir / "output"/test_type
        output_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        if test_type == 'SV':
            result = process_sv_single(file_path, output_dir)
        elif test_type == 'SR':
            result = process_sr_single(file_path, output_dir)
        elif test_type == 'PR':
            result = process_pr_single(file_path, output_dir)

        end_time = time.time()
        elapsed = end_time - start_time
        result["elapsed_seconds"] = elapsed

        return result
    
    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}

def process_sv_single(file_path, output_dir):
    """Process single Sustained Vowel file"""

    try:
        temp_dir = output_dir / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        temp_file = temp_dir / f"SV_{Path(file_path).name}"
        shutil.copy2(file_path, temp_file)

        participant_info_path = temp_dir / "participantInfo.csv"
        with open(participant_info_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["participant"])
            writer.writerow(["Single"])

        dataPath = str(temp_dir)
        speechTest = "SV"
        group = "Single"
        figPath = str(output_dir)

        filenames, files = audio_processing.load_audio_files(dataPath, speechTest)

        audio_processing.process_voiced_detection(files, filenames, speechTest, str(output_dir), group, figPath)

        df = audio_processing.process_feature_estimation(dataPath, str(output_dir), group, speechTest)

        shutil.rmtree(temp_dir)

        features_file = output_dir / f"features_{group}_{speechTest}.csv"
        # The plot is saved as SV_<original_filename>.png in output_dir
        plot_filename = f"SV_{Path(file_path).stem}.png"
        plot_path = output_dir / plot_filename

        return {
            "status": "success",
            "test_type": "SV",
            "file": str(file_path),
            "output": str(features_file),
            "plot_path": str(plot_path),
            "message": "SV processing completed",
            "features": df.to_dict(orient="records")
        }

    except Exception as e:
        return {"error": f"SV processing failed: {str(e)}"}


def process_sr_single(file_path, output_dir):
    """Process single Syllable Repetition file"""

def process_pr_single(file_path, output_dir):
    """Process single Paragraph Reading file"""

def main():
    """Main entry point - handle command line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python main.py <test_type> <file_path>")
        print("Test types: SV, SR, PR")
        print("File format: WAV only")
        print("Examples:")
        print("  python main.py SV /path/to/audio.wav")
        print("  python main.py SR /path/to/audio.wav")
        print("  python main.py PR /path/to/audio.wav")
        sys.exit(1)
    
    test_type = sys.argv[1]
    file_path = sys.argv[2]

    result = process_audio(file_path, test_type)
    
    print(json.dumps(result))


if __name__ == "__main__":
    main()
