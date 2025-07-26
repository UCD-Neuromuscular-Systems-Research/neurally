# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Version Control %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Updated 26/03/25 - added the ability to process the Passage Reading task, including voiced detection and feature extraction.
# Updated 01/04/25 - updated the logging process to ensure the log listener is stopped appropriately.
# Updated 05/04/25 - added the ability to process 'SV' task

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Description %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This script executes the audio processing for:
# - Syllable Repetition (SR) Task
# - Paragraph Reading (PR) Task
# - Sustained Vowel (SV) Task 

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Initial Checks %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import os
import pandas as pd
import preProcessingAudioLongitudinal  
import speechFeaturesAcousticLongitudinal
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
from multiprocessing import Queue
from logging.handlers import QueueHandler, QueueListener
import atexit

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Logger Set-Up %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# UPDATED LOGGING METHOD:
# Get module-specific logger instead of root logger:
logger = logging.getLogger(__name__)

# Create a looging queue:
log_queue = Queue(-1)

# Create a queue handler to route log messages to the queue:
queue_handler = QueueHandler(log_queue)
logger.addHandler(queue_handler)

# Set up log file & console handlers:
# File Handlers:
file_handler = logging.FileHandler('audio_processing.log')
file_handler.setLevel(logging.INFO)

# Console Handlers:
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set up the formatter:
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Apply the formatter to the handlers:
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Create a listener to process log messages from the queue and apply handlers:
listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()

# Register an exit handler to ensure the listener is stopped:
def stop_listener():
    if listener:
        listener.stop()

atexit.register(stop_listener)

# Start to log messages:
logger.info("Logging setup complete.")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Constants %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define Subtest Names:
nameSV = ['SV']                                         # Sustained Vowel Task
nameSR = ['SR1', 'SR2', 'SR3', 'SR4', 'SR5']            # Syllable Repetition Task
namePR = ['PR']                                         # Passage Reading Task            

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def load_audio_files(dataPath, speechTest):
    # Helper function to load audio files for a given task:
    try:
        filenames, files = preProcessingAudioLongitudinal.open_wav(dataPath, speechTest).openFiles()

        # Log the structure of the returned data:
        logger.info(f"Loaded {len(files)} audio files for {speechTest}.")
        # Show first two samples of files for inspection
        logger.info(f"Files (sample): {files[:2]}")  

        # Log:
        logger.info(f"Extracted audio data and sampling rates for {speechTest}.")
        
        return filenames, files
    
    except Exception as e:
        logger.error(f"Error loading audio files for {speechTest}: {str(e)}")
        raise

# VOICED DETECTION METHOD - Updated to accept SR, PR & SV Tasks:
def process_voiced_detection(files, filenames, speechTest, outputPath, group, figPath):

    try:
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
            logger.info(f"Created directory: {outputPath}")

        logger.info(f"Processing voiced detection for {speechTest}")

        # Initialise DataFrame to store pID, onset, and offset as lists:
        df_voiced = pd.concat([pd.DataFrame(filenames, columns=['pID']), pd.DataFrame(columns=['onset', 'offset'])],
                              ignore_index=True).astype(object)

        detector = preProcessingAudioLongitudinal.exeDetectionFunctions(
            files, filenames, df_voiced, figPath, sizeEpoch=0.25, overlap=0.75, thresh_multiplier=1, n_devices=1)
        
        # Adjust detection method based on task type:
        if speechTest.startswith('SR'):
            # For Syllable Repetition, get both df_voiced and df_rms
            df_voiced, df_rms = detector.voiceDetector(speechTest)
            result_file = os.path.join(outputPath, f'onsetOffset_{group}_{speechTest}.csv')
            df_voiced.to_csv(result_file)
            logger.info(f"Saved SR voiced detection to {result_file}")

            # Save RMS data if available:
            if df_rms is not None:
                rms_file = os.path.join(outputPath, f'rms_{group}_{speechTest}.csv')
                df_rms.to_csv(rms_file)
                logger.info(f"Saved RMS data to {rms_file}")

            return df_voiced, df_rms
        
        elif speechTest.startswith('PR') or speechTest.startswith('SV'):
            # For PR and SV, only need df_voiced (df_rms will be None):
            df_voiced, _ = detector.voiceDetector(speechTest)  
            result_file = os.path.join(outputPath, f'onsetOffset_{group}_{speechTest}.csv')
            df_voiced.to_csv(result_file)
            logger.info(f"Saved {speechTest} voiced detection to {result_file}")

            return df_voiced

    except Exception as e:
        logger.error(f"Error processing voiced detection for {speechTest}: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        raise

# UPDATED METHOD - to accept SV Task - 05/04/25
def process_feature_estimation(dataPath, outputPath, group, speechTest):

    try:
        # Adjust feature extraction based on task type:
        if speechTest.startswith('SR'):
            df = speechFeaturesAcousticLongitudinal.featuresTable(
                dataPath, outputPath, group, speechTest, 
                fmin=[75, 75], fmax=[600, 5000], nPeriods=[3, 6]
            ).getFeaturesSR()
        elif speechTest.startswith('PR'):
            df = speechFeaturesAcousticLongitudinal.featuresTable(
                dataPath, outputPath, group, speechTest, 
                fmin=[75, 75], fmax=[600, 5000], nPeriods=[3, 6]
            ).getFeaturesPR()
        elif speechTest.startswith('SV'):
            df = speechFeaturesAcousticLongitudinal.featuresTable(
                dataPath, outputPath, group, speechTest, 
                fmin=[75, 75], fmax=[600, 5000], nPeriods=[3, 6]
            ).getFeaturesSV()
        
        features_file = os.path.join(outputPath, f'features_{group}_{speechTest}.csv')
        df.to_csv(features_file)
        logger.info(f"Processed features for {speechTest}, saved to {features_file}.")
        return df
    
    except Exception as e:
        logger.error(f"Error processing features for {speechTest}: {str(e)}")
        raise

# Combine and Save Features - updated to accept SV Task - 05/04/25:
def combine_and_save_features(outputPath, group, task_type='SR'):

    try:
        # Adjust based on task type:
        if task_type == 'SR':
            # Step 1: Combine temporal features from all SR1 to SR5 files
            frames = []
            for i in range(1, 6):  # SR1 to SR5
                df = pd.read_csv(os.path.join(outputPath, f'features_{group}_SR{i}.csv'))
                frames.append(df)

            # Concatenate all the frames:
            df_combined = pd.concat(frames, ignore_index=True)

            # Clean up any 'Unnamed' columns:
            df_combined = df_combined.loc[:, ~df_combined.columns.str.contains('^Unnamed')]
            
            # Step 2: Combine RMS slope values for all SR1 to SR5 files:
            rms_frames = []
            for i in range(1, 6):   # SR1 to SR5
                rms_df = pd.read_csv(os.path.join(outputPath, f'rms_{group}_SR{i}.csv'))
                rms_frames.append(rms_df)
            
            # Concatenate all the RMS frames:
            rms_combined = pd.concat(rms_frames, ignore_index=True)

            # Clean up any 'Unnamed' columns in the RMS data:
            rms_combined = rms_combined.loc[:, ~rms_combined.columns.str.contains('^Unnamed')]
            
            # Ensure the RMS dataframe has the correct column names: - 'filename' to match with the combined DataFrame.
            rms_combined = rms_combined.rename(columns={'pID': 'filename'})
            
            # Step 3: Merge the RMS data into the combined temporal features dataframe
            df_combined = pd.merge(df_combined, rms_combined[['filename', 'rms_slope']], on='filename', how='left')
            
             # Step 4: Save the combined DataFrame to a CSV file
            combined_file = os.path.join(outputPath, f'features_{group}_SR.csv')
            df_combined.to_csv(combined_file, index=False)
            
            logger.info(f"Combined and saved SR features with RMS slope for {group} into {combined_file}.")
        
        # For PR and SV:
        elif task_type in ['PR', 'SV']:
            logger.info(f"Skipping feature combination for {task_type} as only a single {task_type} file is present for {group}.")

    except Exception as e:
        logger.error(f"Error combining and saving features for {task_type} in {group}: {str(e)}")
        raise

# Check Processed Files: Check if all necessary output files are present before running the next step.
def check_processed_files(outputPath, group, names):

    for speechTest in names:
        voiced_file = os.path.join(outputPath, f'onsetOffset_{group}_{speechTest}.csv')
        feature_file = os.path.join(outputPath, f'features_{group}_{speechTest}.csv')
        
        if not os.path.exists(voiced_file):
            logger.error(f"Voiced detection file not found for {speechTest}. Expected file: {voiced_file}")
            return False

        if not os.path.exists(feature_file):
            logger.error(f"Feature file not found for {speechTest}. Expected file: {feature_file}")
            return False

    logger.info("All required files are present.")
    return True

# Process Speech Features: main function to process speech features for subtests (SR, PR or SV) updated to accept SV Task - 05/04/25.
def process_speech_features(dataPath, outputPath, figPath, group, names):

    try:
        # Parallel Processing with ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=5) as executor:
            # Log before submitting tasks
            logger.info(f"Submitting tasks for voiced detection and feature estimation for group {group}.")

            # Submit voiced detection tasks
            future_voiced = {
                executor.submit(process_voiced_detection, files, filenames, speechTest, outputPath, group, figPath): speechTest
                for speechTest, (filenames, files) in zip(names, [load_audio_files(dataPath, speechTest) for speechTest in names])
            }

            # Log task submission
            logger.info(f"Tasks submitted for {len(future_voiced)} voiced detection tasks.")

            # Wait for all voiced detection tasks to complete
            for future in as_completed(future_voiced):
                speechTest = future_voiced[future]
                try:
                    result = future.result()  # Block until task completes
                    
                    # Handle different return types based on task type
                    if speechTest.startswith('SR'):
                        df_voiced, df_rms = result
                        logger.info(f"Completed voiced detection for {speechTest}.")
                        logger.info(f"  Voiced DataFrame: {df_voiced.shape if df_voiced is not None else 'No result'}")
                        logger.info(f"  RMS DataFrame: {df_rms.shape if df_rms is not None else 'No RMS data'}")
                    elif speechTest.startswith('PR'):
                        df_voiced = result
                        logger.info(f"Completed voiced detection for {speechTest}. Result: {df_voiced.shape if df_voiced is not None else 'No result'}")
                    elif speechTest.startswith('SV'):
                        df_voiced = result
                        logger.info(f"Completed voiced detection for {speechTest}. Result: {df_voiced.shape if df_voiced is not None else 'No result'}")
                except Exception as e:
                    logger.error(f"Error during voiced detection for {speechTest}: {str(e)}")

            # After all voiced detection is complete, submit feature estimation tasks:
            future_features = {
                executor.submit(process_feature_estimation, dataPath, outputPath, group, speechTest): speechTest
                for speechTest in names
            }

            # Log task submission for feature estimation:
            logger.info(f"Tasks submitted for {len(future_features)} feature estimation tasks.")

            # Wait for all feature estimation tasks to complete:
            for future in as_completed(future_features):
                speechTest = future_features[future]
                try:
                    result_features = future.result()  # Block until task completes:
                    logger.info(f"Completed feature estimation for {speechTest}. Result: {result_features}")
                except Exception as e:
                    logger.error(f"Error during feature estimation for {speechTest}: {str(e)}")
        
        # Determine task type based on the input names (SR, PR, or SV):
        if names[0].startswith('SR'):
            task_type = 'SR'
        elif names[0].startswith('PR'):
            task_type = 'PR'
        elif names[0].startswith('SV'):  
            task_type = 'SV'
        else:
            task_type = 'Unknown'
            logger.error(f"Unknown task type for {group}. Task names: {names}")
        
        # Check if all files were processed and exist:
        if check_processed_files(outputPath, group, names):
            # Combine and Save Features:
            logging.info(f"All files processed successfully for {group}. Combining and saving features.")
            combine_and_save_features(outputPath, group, task_type)
            logging.info(f"Processing of {group} completed successfully!")
        else:
            logging.error(f"One or more required files were missing for {group}. Please check the logs for details.")

    except Exception as e:
        logger.error(f"Error in process_speech_features: {str(e)}", exc_info=True)
        raise

    finally:
        
        logger.info("Finished processing speech features.")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% IF MAIN SCRIPT EXECUTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# If this script is run directly:
if __name__ == "__main__":
    try:
        logger.info("Audio processing module loaded")
    except Exception as e:
        logger.error(f"Error in main module: {str(e)}", exc_info=True)
    finally:
        # Ensures the listener is stopped when the script ends:
        stop_listener()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%