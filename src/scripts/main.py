import os
import sys
import json
from pathlib import Path
import time
import csv
import shutil

sys.path.append(str(Path(__file__).parent / "HD"))
import HD.audioProcessingHDLongitudinal as audio_processing

TEST_TYPES = ["SV", "SR", "PR"]
VALID_EXTENSIONS = ['.wav']

def validate_audio_file(file_path):
    """Audio file validation"""
    
    if not os.path.exists(file_path):
        return False, f"Audio file not found: {file_path}"

    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"

    file_extension = Path(file_path).suffix.lower()

    if file_extension not in VALID_EXTENSIONS:
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

def setup_temp_directory(file_paths, test_type, output_dir):
    """Setup temporary directory for processing"""
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    for i, file_path in enumerate(file_paths):
        unique_name = f"{test_type}_{i+1}_{Path(file_path).name}"
        temp_file = temp_dir / unique_name
        shutil.copy2(file_path, temp_file)

    participant_info_path = temp_dir / "participantInfo.csv"
    with open(participant_info_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["participant"])
        for i in range(len(file_paths)):
            writer.writerow([f"File_{i+1}"])

    return temp_dir

def process_sv_files(file_paths, output_dir):
    """Process Sustained Vowel files (single or multiple) using existing HD capabilities"""

    speechTestType = "SV"

    try:
        temp_dir = setup_temp_directory(file_paths, speechTestType, output_dir)

        dataPath = str(temp_dir)
        group = "Multiple" if len(file_paths) > 1 else "Single"
        figPath = str(output_dir)

        filenames, files = audio_processing.load_audio_files(dataPath, speechTestType)
        audio_processing.process_voiced_detection(files, filenames, speechTestType, str(output_dir), group, figPath)
        df = audio_processing.process_feature_estimation(dataPath, str(output_dir), group, speechTestType)

        shutil.rmtree(temp_dir)

        # Get all plot files and match them to original files
        plot_files = list(output_dir.glob("*.png"))
        
        results = {
            "status": "success",
            "test_type": "SV",
            "total_files": len(file_paths),
            "files": []
        }

        for i, file_path in enumerate(file_paths):
            original_filename = Path(file_path).stem  # filename without extension
            file_result = {
                "filename": Path(file_path).name,
                "original_path": str(file_path),
                "status": "success"
            }
            
            if i < len(df):
                file_result["features"] = df.iloc[i].to_dict()
            
            # Find the plot file that matches this original filename
            matching_plot = None
            for plot_file in plot_files:
                if original_filename in plot_file.stem:
                    matching_plot = plot_file
                    break
            
            if matching_plot:
                file_result["plot_path"] = str(matching_plot.absolute())
            
            results["files"].append(file_result)

        return results

    except Exception as e:
        return {"error": f"SV processing failed: {str(e)}"}


def process_audio_files(file_paths, test_type):
    """Process audio files (single or multiple) for specific test type (SV, SR, PR)"""
    try:
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        for file_path in file_paths:
            is_valid, message = validate_audio_file(file_path)
            if not is_valid:
                return {"error": f"Invalid file {file_path}: {message}"}

        if test_type not in ["SV", "SR", "PR"]:
            return {"error": f"Invalid test type: {test_type}. Must be SV, SR, or PR."}

        current_dir = Path(__file__).parent
        output_dir = current_dir / "output" / test_type
        output_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        if test_type == 'SV':
            result = process_sv_files(file_paths, output_dir)
        elif test_type == 'SR':
            result = process_sr_files(file_paths, output_dir)
        elif test_type == 'PR':
            result = process_pr_files(file_paths, output_dir)

        end_time = time.time()
        elapsed = end_time - start_time
        result["elapsed_seconds"] = elapsed

        return result
    
    except Exception as e:
        return {"error": f"Error processing files: {str(e)}"}

def process_sr_files(file_paths, output_dir):
    """Process Syllable Repetition files (single or multiple) using existing HD capabilities"""

    speechTestType = "SR"

    try:
        temp_dir = setup_temp_directory(file_paths, speechTestType, output_dir)

        dataPath = str(temp_dir)
        group = "Multiple" if len(file_paths) > 1 else "Single"
        figPath = str(output_dir)

        filenames, files = audio_processing.load_audio_files(dataPath, speechTestType)
        audio_processing.process_voiced_detection(files, filenames, speechTestType, str(output_dir), group, figPath)
        df = audio_processing.process_feature_estimation(dataPath, str(output_dir), group, speechTestType)

        shutil.rmtree(temp_dir)

        # Get all plot files and match them to original files
        plot_files = list(output_dir.glob("*.png"))
        
        results = {
            "status": "success",
            "test_type": "SR",
            "total_files": len(file_paths),
            "files": []
        }

        for i, file_path in enumerate(file_paths):
            original_filename = Path(file_path).stem  # filename without extension
            file_result = {
                "filename": Path(file_path).name,
                "original_path": str(file_path),
                "status": "success"
            }
            
            if i < len(df):
                file_result["features"] = df.iloc[i].to_dict()
            
            # Find the plot file that matches this original filename
            matching_plot = None
            for plot_file in plot_files:
                if original_filename in plot_file.stem:
                    matching_plot = plot_file
                    break
            
            if matching_plot:
                file_result["plot_path"] = str(matching_plot.absolute())
            
            results["files"].append(file_result)

        return results

    except Exception as e:
        return {"error": f"SR processing failed: {str(e)}"}

def process_pr_files(file_paths, output_dir):
    """Process Paragraph Reading files (single or multiple) using existing HD capabilities"""
    speechTestType = "PR"
    
    try:
        temp_dir = setup_temp_directory(file_paths, speechTestType, output_dir)
        
        dataPath = str(temp_dir)
        group = "Multiple" if len(file_paths) > 1 else "Single"
        figPath = str(output_dir)
        
        filenames, files = audio_processing.load_audio_files(dataPath, speechTestType)
        audio_processing.process_voiced_detection(files, filenames, speechTestType, str(output_dir), group, figPath)
        df = audio_processing.process_feature_estimation(dataPath, str(output_dir), group, speechTestType)
        
        shutil.rmtree(temp_dir)
        
        # Get all plot files and match them to original files
        plot_files = list(output_dir.glob("*.png"))
        
        results = {
            "status": "success",
            "test_type": "PR",
            "total_files": len(file_paths),
            "files": []
        }
        
        for i, file_path in enumerate(file_paths):
            original_filename = Path(file_path).stem  # filename without extension
            file_result = {
                "filename": Path(file_path).name,
                "original_path": str(file_path),
                "status": "success"
            }
            
            if i < len(df):
                file_result["features"] = df.iloc[i].to_dict()
            
            # Find the plot file that matches this original filename
            matching_plot = None
            for plot_file in plot_files:
                if original_filename in plot_file.stem:
                    matching_plot = plot_file
                    break
            
            if matching_plot:
                file_result["plot_path"] = str(matching_plot.absolute())
            
            results["files"].append(file_result)
        
        return results
        
    except Exception as e:
        return {"error": f"PR processing failed: {str(e)}"}

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <test_type> <file_path>")
        print("Usage: python main.py <test_type> --multiple <file_path1|file_path2|...>")
        print(f"Test types: {', '.join(TEST_TYPES)}")
        print("File format: WAV only")
        print("Examples:")
        print("  python main.py SV /path/to/audio.wav")
        print("  python main.py SV --multiple /path1.wav|/path2.wav|/path3.wav")
        sys.exit(1)
    
    test_type = sys.argv[1]
    
    if len(sys.argv) > 3 and sys.argv[2] == '--multiple':
        file_paths = sys.argv[3].split('|')
    else:
        file_paths = sys.argv[2]
    
    result = process_audio_files(file_paths, test_type)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
