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


def process_audio_files(file_paths, test_type):
    """Process audio files (single or multiple) for specific test type (SV, SR, PR)"""
    try:
        # Convert single file to list for unified processing
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        # Input validation for all files
        for file_path in file_paths:
            is_valid, message = validate_audio_file(file_path)
            if not is_valid:
                return {"error": f"Invalid file {file_path}: {message}"}

        if test_type not in ["SV", "SR", "PR"]:
            return {"error": f"Invalid test type: {test_type}. Must be SV, SR, or PR."}

        # Set up paths
        current_dir = Path(__file__).parent
        output_dir = current_dir / "output" / test_type
        output_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        # Process based on test type
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

def process_sv_files(file_paths, output_dir):
    """Process Sustained Vowel files (single or multiple) using existing HD capabilities"""
    try:
        temp_dir = output_dir / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        # Copy all files to temp directory with proper naming
        copied_files = []
        for i, file_path in enumerate(file_paths):
            # Create unique filename to avoid conflicts
            unique_name = f"SV_{i+1}_{Path(file_path).name}"
            temp_file = temp_dir / unique_name
            shutil.copy2(file_path, temp_file)
            copied_files.append(unique_name)

        # Create participant info for all files
        participant_info_path = temp_dir / "participantInfo.csv"
        with open(participant_info_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["participant"])
            for i in range(len(file_paths)):
                writer.writerow([f"File_{i+1}"])

        dataPath = str(temp_dir)
        speechTest = "SV"
        group = "Multiple" if len(file_paths) > 1 else "Single"
        figPath = str(output_dir)

        # Use existing HD multi-file processing
        filenames, files = audio_processing.load_audio_files(dataPath, speechTest)
        audio_processing.process_voiced_detection(files, filenames, speechTest, str(output_dir), group, figPath)
        df = audio_processing.process_feature_estimation(dataPath, str(output_dir), group, speechTest)

        # Clean up temp directory
        shutil.rmtree(temp_dir)

        # Get all plot files created
        plot_files = list(output_dir.glob("SV_*.png"))
        
        # Create results structure
        results = {
            "status": "success",
            "test_type": "SV",
            "total_files": len(file_paths),
            "files": []
        }

        # Add individual file results
        for i, file_path in enumerate(file_paths):
            file_result = {
                "filename": Path(file_path).name,
                "original_path": str(file_path),
                "status": "success"
            }
            
            # Add features for this file if available
            if i < len(df):
                file_result["features"] = df.iloc[i].to_dict()
            
            # Add plot file if available
            if i < len(plot_files):
                file_result["plot_path"] = str(plot_files[i])
            
            results["files"].append(file_result)

        return results

    except Exception as e:
        return {"error": f"SV processing failed: {str(e)}"}

def process_sr_files(file_paths, output_dir):
    """Process Syllable Repetition files (single or multiple)"""
    # TODO: Implement similar to process_sv_files but with "SR"
    pass

def process_pr_files(file_paths, output_dir):
    """Process Paragraph Reading files (single or multiple)"""
    # TODO: Implement similar to process_sv_files but with "PR"
    pass

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <test_type> <file_path>")
        print("Usage: python main.py <test_type> --multiple <file_path1|file_path2|...>")
        print("Test types: SV, SR, PR")
        print("File format: WAV only")
        print("Examples:")
        print("  python main.py SV /path/to/audio.wav")
        print("  python main.py SV --multiple /path1.wav|/path2.wav|/path3.wav")
        sys.exit(1)
    
    test_type = sys.argv[1]
    
    # Check if processing multiple files
    if len(sys.argv) > 3 and sys.argv[2] == '--multiple':
        file_paths = sys.argv[3].split('|')
    else:
        file_paths = sys.argv[2]  # Single file as string
    
    result = process_audio_files(file_paths, test_type)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
