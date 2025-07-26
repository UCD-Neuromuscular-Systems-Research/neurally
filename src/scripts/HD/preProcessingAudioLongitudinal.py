# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Version Control %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Updated 01/04/2025 - updated logging process to fix errors when executing the main script.
# Updated 01/04/2025 - updated to enable processing of the Sustained Vowel task.

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% IMPORT LIBRARIES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np                                          # Numerical Operations
from scipy import signal                                    # Signal Processing
from scipy.io import wavfile                                # Audio Processing (scipy)
import os, librosa                                          # Audio Processing
import matplotlib.pyplot as plt                             # Plot & Visualisation
from concurrent.futures import ProcessPoolExecutor          # Parallel Processing
from pathlib import Path                                    # Path Management
import logging                                              # Logging
from skimage.filters import threshold_otsu                  # Otsu Thresholding
import pandas as pd                                         # DataFrame Management
import atexit                                               # Logger Cleanup on Exit
from multiprocessing import Queue                           # Queue for Logging Process
from logging.handlers import QueueHandler, QueueListener    # Queue Handlers for Logging
import re                                                   # Used for removing trailing numbers from filenames
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Logger Set-Up %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS: OPEN AUDIO FILES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class open_wav:

    # INITIALISE:
    def __init__(self, dataPath, speechTest):
        self.dataPath, self.speechTest = dataPath, speechTest

    # LOAD FILE: Helper function to load a single .wav file using scipy
    def load_file(self, file_path):
        filename = file_path.stem
        try:
            # Use scipy to load the .wav file
            fs, data = wavfile.read(file_path)
            
            # Convert data to float32 required for librosa:
            data = data.astype(np.float32) / 32768.0  # Normalise to range [-1, 1]

        except Exception as e:
            logger.error(f"Error loading {filename} from {file_path}: {e}")
            return None, None  
        return filename, (data, fs)

    # OPEN FILES: Open & load .wav files for a specific speech test (SR, SV, or PR task)
    def openFiles(self):
        # Get all .wav files in directory, filtered by speech test task (SR, SV, PR):
        onlyfiles = [f for f in os.listdir(self.dataPath) if f.endswith(".wav")]
        filtered_files = [file for file in onlyfiles if self.speechTest in file]

        # Log the number of files found for the given speechTest:
        logger.info(f"Found {len(filtered_files)} files for {self.speechTest} task.")

        if len(filtered_files) == 0:
            logger.warning(f"No files found for {self.speechTest} task in {self.dataPath}. Ensure correct filenames.")

        # Use the helper function to load each file:
        filenames, files = zip(*[self.load_file(Path(self.dataPath) / file) for file in filtered_files])

        return filenames, files
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS: PRE-PROCESS AUDIO FROM SPEECH TEST %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class preProcess_Audio:

    # INITIALISE:
    def __init__(self, data_list, order=4, fc_low=10, fc_high=5000, new_fs=44100, crop_len=0.5, pad_len=2):
        data = data_list[0]                                                             # Audio Data
        self.fs = int(data_list[1])                                                     # Original Sampling Frequency
        self.data = data - np.nanmean(data[round(self.fs):round(len(data) - self.fs)])  # Remove DC Offset
        self.order, self.fc_low, self.fc_high = order, fc_low, fc_high                  # Filter Parameters
        self.new_fs = new_fs                                                            # Target Sample Rate
        self.crop_len, self.pad_len = crop_len, pad_len                                 # Length for Cropping & Padding

    # BAND-PASS FILTER: Apply Butterworth bandpass filter.
    def bandpassFilter(self):
        low_lim = self.fc_low / (self.fs / 2)                                           # Normalise Low Cutoff Frequency
        high_lim = self.fc_high / (self.fs / 2)                                         # Normalise High Cutoff Frequency
        b, a = signal.butter(self.order, [low_lim, high_lim], btype='band')             # Filter Design
        self.dataFiltered = signal.filtfilt(b, a, self.data)                            # Apply Filter
        return self.dataFiltered, self.fs

    # RESAMPLE AUDIO: Resample audio to a new sample rate.
    def resampleAudio(self):
        resampData = librosa.resample(
            self.data,
            orig_sr=self.fs,
            target_sr=self.new_fs,
            res_type='kaiser_best'                                                      # Kaiser Resampling Method
        )
        self.fs = self.new_fs                                                           # Update Sample Rate
        self.dataFiltered = resampData.copy()                                           # Store Resampled Data
        return self.dataFiltered, self.fs

    # CROP AND PAD: Crop and pad the audio data.
    def crop_and_pad(self):
        deMeanData = self.dataFiltered - np.nanmean(self.dataFiltered[round(self.fs):round(len(self.dataFiltered) - self.fs)])      # Remove DC Offset
        dataCrop = deMeanData[int(self.crop_len * self.fs):len(deMeanData) - int(self.crop_len * self.fs)]                          # Crop Data
        self.dataProcessed_resamp = np.pad(dataCrop, (int(self.pad_len * self.fs), int(self.pad_len * self.fs)), mode='constant')   # Pad Data
        self.dataProcessed_resamp = self.dataProcessed_resamp / np.max(self.dataProcessed_resamp)                                   # Normalise Data
        return self.dataProcessed_resamp, self.fs

    # COMBINE: Band-pass filter, resample, and crop/pad in one step.
    def preProcess_resample(self):
        self.bandpassFilter()                       # Apply Bandpass Filter
        self.resampleAudio()                        # Resample to New Sample Rate
        self.crop_and_pad()                         # Crop and Pad Data
        return self.dataProcessed_resamp, self.fs

    # COMBINE WITHOUT RESAMPLING: Only bandpass filter and crop/pad in one step - exclude resample.
    def preProcess_no_resample(self):
        self.bandpassFilter()                       # Apply Bandpass Filter
        self.crop_and_pad()                         # Crop and Pad Data
        return self.dataProcessed_resamp, self.fs

    # PROCESS SINGLE FILE: Helper function to process one file (Bandpass filter, resample, crop/pad)
    def process_single_file(self, data_list):
        data, fs = data_list                                                          # Load data and sample rate
        self.data = data - np.nanmean(data)                                           # Remove DC Offset
        self.fs = fs                                                                  # Set sample rate
        self.bandpassFilter()                                                         # Apply Bandpass Filter
        self.resampleAudio()                                                          # Resample Audio
        self.crop_and_pad()                                                           # Crop and Pad Audio
        return self.dataProcessed_resamp, self.fs

    # PROCESS ALL FILES: Apply the processing pipeline to all files in parallel
    def process_all_files(self, data_list):
        with ProcessPoolExecutor() as executor:                                        # Parallel Processing
            results = list(executor.map(self.process_single_file, data_list))          # Process each file in parallel
        return results
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS: SIGNAL DETECTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class signalDetection:

    # INITIALISE:
    def __init__(self, data, fs, filename, sizeEpoch=0.25, overlap=0.75):
        self.data = data                                                    # Audio Signal
        self.fs = fs                                                        # Sampling Frequency
        self.filename = filename                                            # File Name
        self.sizeEpoch = sizeEpoch                                          # Epoch Duration (in seconds)
        self.overlap = overlap                                              # Overlap Ratio between Epochs

    # DIVIDE EPOCHS: Split data into overlapping epochs.
    def divideEpochs(self):
        step = self.sizeEpoch * self.fs * (1 - self.overlap)  # Step Size between Epochs
        endIdx = len(self.data)

        # Array Indexing:
        startEpoch = np.arange(0, endIdx, step).astype(int)
        endEpoch = np.minimum(startEpoch + int(self.sizeEpoch * self.fs), endIdx)

        # Generate Epoch Names:
        nameEpoch = [f'{self.filename}_epoch{i + 1}' for i in range(len(startEpoch))]

        return nameEpoch, startEpoch, endEpoch

    # TEAGER-KAISER ENERGY OPERATOR (TKEO): Compute non-linear energy operator envelope of the signal.
    def TKEO(self):
        # Vectorised TKEO Calculation:
        x = self.data[:-4]
        x1 = self.data[1:-3]
        x2 = self.data[2:-2]
        x_1 = self.data[3:-1]
        x_2 = self.data[4:]

        # Apply TKEO Formula:
        tkeo = 2 * x ** 2 + (x1 - x_1) ** 2 - (x * (x2 + x_2))

        # Apply Rolling Window:
        tkeo_smoothed = np.convolve(np.abs(tkeo), np.ones(3) / 3, mode='same')  # Apply Rolling Window with Size 3
        tkeo_smoothed = np.convolve(tkeo_smoothed, np.ones(5) / 5, mode='same')  # Apply Second Rolling Window with Size 5

        # Envelope Detection using Low-Pass Filter:
        b, a = signal.butter(2, 10 / (0.5 * self.fs), btype='low')
        tkeo_envelope = signal.filtfilt(b, a, tkeo_smoothed)

        return tkeo_envelope

    # ROOT-MEAN SQUARED (RMS): Compute RMS energy for each epoch. [Note: Currently not using this method.]
    def RMS(self):
        nameEpoch, startEpoch, endEpoch = self.divideEpochs()  # Get Epoch Info

        # Vectorised RMS calculation:
        data_epochs = [self.data[j:k] * np.hanning(k - j) for j, k in zip(startEpoch, endEpoch)]  # Apply Hanning Window
        dataRMS = np.array([np.sqrt(np.mean((epoch - np.mean(epoch)) ** 2)) for epoch in data_epochs])

        return dataRMS
    
    # ROOT-MEAN SQUARED (RMS): Compute RMS energy using a sliding window approach for the same resolution as TKEO.
    def RMS_sliding(self):
        # Define Window Size:
        window_size = 5
        
        # Zero-Padding for edge cases:
        padded_signal = np.pad(self.data, (window_size//2, window_size//2), mode='edge')
        
        # Initialise RMS array:
        rms_values = np.zeros(len(self.data))
        
        # Calculate RMS using sliding window:
        for i in range(len(self.data)):
            window = padded_signal[i:i+window_size]
            rms_values[i] = np.sqrt(np.mean(window**2))
        
        # Apply same smoothing as TKEO for consistency:
        rms_smoothed = np.convolve(rms_values, np.ones(3)/3, mode='same')
        rms_smoothed = np.convolve(rms_smoothed, np.ones(5)/5, mode='same')
        
        # Apply same low-pass filter as TKEO:
        b, a = signal.butter(2, 10/(0.5*self.fs), btype='low')
        rms_envelope = signal.filtfilt(b, a, rms_smoothed)
        
        return rms_envelope

    # Adaptive Thresholding with Overlap: Apply Otsu's method to each window of the envelope.
    def adaptive_thresholding_with_overlap(self, envelope, window_length, overlap_ratio):

        thresholds = []                                          # List to store thresholds for each window.
        step_size = int(window_length * (1 - overlap_ratio))     # Step size based on overlap ratio.

        # Sliding window loop with overlap:
        for start in range(0, len(envelope) - window_length + 1, step_size):
            end = start + window_length
            window = envelope[start:end]
            
            # Apply Otsu's thresholding to the window:
            threshold = threshold_otsu(window)
            
            # Store the threshold for this window:
            thresholds.append(threshold)
        
        return thresholds



    # Detects voiced onset-offset pairs ensuring:
    # - Each onset has a corresponding offset.
    # - No consecutive onsets/offsets without proper pairing.
    # - A minimum gap between an offset and the next onset to prevent overlap.
    def getOnsetOffsetNew(self, data, adaptive_threshold, window_length, overlap_ratio, 
                        threshold_multiplier=1.5, max_iterations=10, detection_threshold_ratio=0.4, 
                        min_gap_ms=20):

        assert len(adaptive_threshold) <= len(data)

        step_size = int(window_length * (1 - overlap_ratio))  # Step size for overlapping windows

        # Initialise arrays for final threshold values:
        final_threshold = np.zeros_like(data)
        sample_count = np.zeros_like(data)

        # Apply adaptive thresholding with overlapping windows:
        threshold_index = 0
        for start in range(0, len(data) - window_length + 1, step_size):
            end = min(start + window_length, len(data)) 
            final_threshold[start:end] += adaptive_threshold[threshold_index]
            sample_count[start:end] += 1
            threshold_index += 1

        # Compute the final adaptive threshold per sample:
        final_threshold = np.divide(final_threshold, sample_count, where=sample_count > 0)
        final_threshold *= 0.65  # Apply threshold multiplier.

        # Calculate the minimum energy threshold based on the mean of TKEO data:
        min_threshold = 0.45 * np.mean(data)

        # Initial onset/offset detection using the adaptive threshold and minimum threshold
        above_threshold = (data > final_threshold) & (data > min_threshold)  # Apply min threshold.
        diff = np.diff(above_threshold.astype(int))
        onset = np.where(diff == 1)[0]
        offset = np.where(diff == -1)[0]

        # Ensure every onset has a corresponding offset
        if len(onset) > 0 and len(offset) > 0:
            if offset[0] < onset[0]:  # If the first offset comes before the first onset, remove it
                offset = offset[1:]
            if len(onset) > 0 and len(offset) > 0 and onset[-1] > offset[-1]:  # If last onset has no offset, remove it
                onset = onset[:-1]

        # Define the minimum gap in samples:
        min_gap = int((min_gap_ms / 1000) * self.fs)  # Convert ms to samples.

        # Ensure onset-offset pairs are properly aligned with min gap:
        valid_onsets = []
        valid_offsets = []
        i, j = 0, 0 

        while i < len(onset) and j < len(offset):
            # Valid onset-offset pair:
            if onset[i] < offset[j]:  
                if len(valid_offsets) == 0 or (onset[i] - valid_offsets[-1] > min_gap):  
                    # Ensure there's a minimum gap between previous offset and current onset:
                    valid_onsets.append(onset[i])
                    valid_offsets.append(offset[j])
                i += 1
                j += 1  # Move to the next pair
            else:
                j += 1  # Skip extra offsets

        onset = np.array(valid_onsets)
        offset = np.array(valid_offsets)

        return onset, offset

    # Onset/Offset Detection Method for Sustained Vowel Task:
    def getOnsetOffsetSV(self, data, threshold):
        
        # Ensure data is not empty and has at least two samples:
        if data is None or len(data) < 2:
            return [], []  

        # Initialise lists for onsets and offsets:
        onsets = []
        offsets = []
        BelowThresh = True                          # Assume the signal starts below the threshold.

        for i in range(len(data) - 1):              # Prevent index out of bounds.
            
            if BelowThresh and data[i] > threshold and data[i + 1] > threshold:
                onsets.append(i)
                BelowThresh = False
            elif not BelowThresh and data[i] < threshold and data[i + 1] < threshold:
                offsets.append(i)
                BelowThresh = True

        # Clean up unmatched onset/offset pairs:
        if offsets and onsets and offsets[0] < onsets[0]:
            del offsets[0]
        if onsets and offsets and onsets[-1] > offsets[-1]:
            del onsets[-1]

        return onsets, offsets

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS: TASK SPECIFIC DETECTION FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class detectionFunctions:

    # INITIALISE:
    def __init__(self, data, fs, filename, sizeEpoch=0.25, overlap=0.75, thresh_multiplier=1.5):
        self.data = data                                                                            # Audio Signal
        self.fs = fs                                                                                # Sampling Frequency
        self.filename = filename                                                                    # File Name
        self.thresh_multiplier = thresh_multiplier                                                  # Threshold Multiplier for Detection
        self.sizeEpoch = sizeEpoch                                                                  # Epoch Duration (in seconds)
        self.overlap = overlap                                                                      # Overlap Ratio between Epochs
        self.signal_detector = signalDetection(data, fs, filename, sizeEpoch, overlap)              # Reuse signalDetection object

    # Sustained Vowel Function:
    def voicedUnvoiced_SustainedVowel(self, figPath):
        # Compute TKEO Energy:
        dataTKEO = self.signal_detector.TKEO()

        # Define Threshold:
        #threshold = self.thresh_multiplier * np.nanmean(dataTKEO)
        threshold = 0.15 * np.nanmean(dataTKEO)

        # Detect Onset/Offset using the original SV detection method:
        onset_temp, offset_temp = self.signal_detector.getOnsetOffsetSV(dataTKEO, threshold)

        # Convert to Time (seconds):
        onset_temp = np.array(onset_temp) / self.fs
        offset_temp = np.array(offset_temp) / self.fs

        # Filter Out Short Durations (<0.5 seconds):
        valid_indices = (offset_temp - onset_temp) > 1
        startPeaks = onset_temp[valid_indices]
        endPeaks = offset_temp[valid_indices]

        # Plot Results:
        time_axis = np.arange(len(self.data)) / self.fs  # Time Axis (in seconds)
        self.plot_detection(
            figPath,
            dataTKEO,
            startPeaks,
            endPeaks,
            None,    
            None,
            time_axis,
            None,
            is_syllable_repetition=False,
            static_threshold = threshold
        )

        # Revert to Sample Indices:
        startPeaks = np.round(startPeaks * self.fs).astype(int)
        endPeaks = np.round(endPeaks * self.fs).astype(int)

        # Return as lists:
        return startPeaks.tolist(), endPeaks.tolist()

    # Syllable Repetition Function:
    def voicedUnvoiced_SyllableRepetition(self, figPath):
        # Compute TKEO Energy:
        dataTKEO = self.signal_detector.TKEO()

        # Define Window Length and Overlap:
        window_length = int(0.10 * self.fs)  
        overlap_ratio = 0.5  # 50% overlap between windows

        # Apply the adaptive Otsu thresholding with forward and backward methods:
        adaptive_threshold = self.signal_detector.adaptive_thresholding_with_overlap(
            dataTKEO, window_length, overlap_ratio
        )

        # Detect Onset/Offset using adaptive thresholding:
        startPeaks_temp, endPeaks_temp = self.signal_detector.getOnsetOffsetNew(
            dataTKEO, adaptive_threshold, window_length, overlap_ratio
        )

        # Convert to Time (seconds):
        startPeaks_temp = np.array(startPeaks_temp) / self.fs
        endPeaks_temp = np.array(endPeaks_temp) / self.fs

        # Filter Out Short Durations (<0.08 seconds):
        valid_indices = (endPeaks_temp - startPeaks_temp) > 0.08
        startPeaks = startPeaks_temp[valid_indices]
        endPeaks = endPeaks_temp[valid_indices]

        # Compute RMS Energy of Signal:
        dataRMS = self.signal_detector.RMS_sliding()

        # Calculate mean RMS Energy for each syllable segment:
        meanRMS = [np.mean(dataRMS[int(startPeaks[i]*self.fs):int(endPeaks[i]*self.fs)]) for i in range(len(startPeaks))]
        
        # Calculate RMS slope if more than one segment exists:
        rms_slope = None
        if len(meanRMS) > 1:
            # Get midpoints for time reference:
            midpoints = [(startPeaks[i] + endPeaks[i]) / 2 for i in range(len(startPeaks))]
            # Calculate slope:
            rms_slope, _ = np.polyfit(midpoints, meanRMS, 1)
    
        # Plot Results:
        time_axis = np.arange(len(self.data)) / self.fs  # Time Axis (in seconds)
        self.plot_detection(figPath, dataTKEO, startPeaks, endPeaks, adaptive_threshold, dataRMS, time_axis, meanRMS, is_syllable_repetition=True)

        # Revert to Sample Indices:
        startPeaks = np.round(startPeaks * self.fs).astype(int)
        endPeaks = np.round(endPeaks * self.fs).astype(int)

        # Return as lists:
        return startPeaks.tolist(), endPeaks.tolist(), meanRMS, rms_slope   

    # VOICED UNVOICED - Passage Reading Task
    def voicedUnvoiced_PassageReading(self, figPath):
        # Compute TKEO Energy:
        dataTKEO = self.signal_detector.TKEO()

        # Define Window Length and Overlap for Adaptive Thresholding:
        window_length = int(0.10 * self.fs)  # 100ms Window
        overlap_ratio = 0.5                  # 50% Overlap

        # Apply the adaptive Otsu thresholding with forward and backward methods
        adaptive_threshold = self.signal_detector.adaptive_thresholding_with_overlap(
            dataTKEO, window_length, overlap_ratio
        )

        # Detect Onset/Offset using adaptive thresholding:
        startPeaks_temp, endPeaks_temp = self.signal_detector.getOnsetOffsetNew(
            dataTKEO, adaptive_threshold, window_length, overlap_ratio
        )

        # Convert to Time (seconds):
        startPeaks_temp = np.array(startPeaks_temp) / self.fs
        endPeaks_temp = np.array(endPeaks_temp) / self.fs

        # Filter Out Short Durations (<0.05 seconds):
        valid_indices = (endPeaks_temp - startPeaks_temp) > 0.05  # Identify suitable threshold for PR Task
        startPeaks = startPeaks_temp[valid_indices]
        endPeaks = endPeaks_temp[valid_indices]

        # Find the 5 longest pauses (sentence boundaries)
        if len(endPeaks) > 5:
            pauses = np.diff(endPeaks)                          # Compute gaps between offsets and next onset
            top_pause_indices = np.argsort(pauses)[-5:]         # Indices of the 5 longest pauses
            sentence_boundaries = endPeaks[top_pause_indices]   # Get the time of these boundaries
        else:
            sentence_boundaries = []                            # Not enough pauses to find boundaries

        # Plot Results:
        time_axis = np.arange(len(self.data)) / self.fs  # Time Axis (in seconds)
        self.plot_detection(figPath, dataTKEO, startPeaks, endPeaks, adaptive_threshold, None, time_axis, None, is_syllable_repetition=False, sentence_boundaries=sentence_boundaries)

        # Revert to Sample Indices:
        startPeaks = np.round(startPeaks * self.fs).astype(int)
        endPeaks = np.round(endPeaks * self.fs).astype(int)

        # Return as lists:
        return startPeaks.tolist(), endPeaks.tolist()

    # PLOT DETECTION METHOD - updated for Sentence Boundaries in Paragraph Reading Task - 18:27 01/04/25
    def plot_detection(self, figPath, dataTKEO, startPeaks, endPeaks, adaptive_threshold = None, dataRMS = None, time_axis = None, meanRMS = None, is_syllable_repetition = True, sentence_boundaries=None, static_threshold = None):
        plt.figure(figsize=(20, 15)) 
        plt.suptitle(self.filename, fontsize=24)

        # Plot 1: Speech Signal with Detected Onsets/Offsets
        plt.subplot(3, 1, 1)  # First subplot
        if time_axis is None:
            plt.plot(self.data, label="Waveform", color='b')
        else:
            plt.plot(time_axis[:len(self.data)], self.data, label="Waveform", color='b')  

        # Plot detected onsets and offsets:
        for st, en in zip(startPeaks, endPeaks):
            # Convert start and end peaks (time) to indices if necessary
            st_idx = int(st * self.fs) if time_axis is None else np.searchsorted(time_axis, st)
            en_idx = int(en * self.fs) if time_axis is None else np.searchsorted(time_axis, en)
            
            # Plot Onsets & Offsets as Vertical Lines:
            plt.axvline(x=time_axis[st_idx] if time_axis is not None else st, color='g', linestyle='--', label="Onset" if st == startPeaks[0] else "")
            plt.axvline(x=time_axis[en_idx] if time_axis is not None else en, color='r', linestyle='--', label="Offset" if en == endPeaks[0] else "")
        
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.title("Speech Signal with Detected Segments")

        # Plot 2: TKEO Energy with Theshold Logic:
        plt.subplot(3, 1, 2)  # Second subplot

        # Ensure time_axis and dataTKEO have the same length
        min_len = min(len(time_axis), len(dataTKEO)) if time_axis is not None else len(dataTKEO)
        plt.plot(time_axis[:min_len], dataTKEO[:min_len], label="TKEO Energy", color='c') if time_axis is not None else plt.plot(dataTKEO[:min_len])

        for st, en in zip(startPeaks, endPeaks):
            # Convert start and end peaks to indices if necessary
            st_idx = int(st * self.fs) if time_axis is None else np.searchsorted(time_axis, st)
            en_idx = int(en * self.fs) if time_axis is None else np.searchsorted(time_axis, en)

            plt.axvline(x=time_axis[st_idx] if time_axis is not None else st, color='g', linestyle='--')  # Green for Onset
            plt.axvline(x=time_axis[en_idx] if time_axis is not None else en, color='r', linestyle='--')  # Red for Offset

        # Threshold Logic:
        if adaptive_threshold is not None:
          
          # Calculate the threshold time axis corresponding to the center of each window:
            window_length = len(dataTKEO) // len(adaptive_threshold)  # Length of each window
            threshold_time_axis = [(i * window_length + window_length / 2) / self.fs for i in range(len(adaptive_threshold))]

            # Plot adaptive threshold:
            plt.plot(threshold_time_axis, 0.65 * np.array(adaptive_threshold), label="Adaptive Threshold", color='purple', linestyle='-')  

            # Compute minimum threshold:
            min_threshold = 0.45 * np.mean(dataTKEO)  # Mean of the TKEO data as the minimum threshold

            # Plot minimum threshold as a horizontal line:
            plt.axhline(y=min_threshold, color='orange', linestyle='--', label="Min Threshold at X%")

        elif static_threshold is not None:
            # Static threshold line (for SV task)
            plt.axhline(y=static_threshold, color='purple', linestyle='-', label="Threshold")
    
        # Plot sentence boundaries (only on TKEO plot for PR task)
        if sentence_boundaries is not None and len(sentence_boundaries) > 0:
            for boundary in sentence_boundaries:
                plt.axvline(x=boundary, color='magenta', linestyle='-', linewidth=2, label="Sentence Boundary" if boundary == sentence_boundaries[0] else "")

        # Plot 3: RMS Energy with Detected Syllable Segments (Only for Syllable Repetition, not PR)
        if is_syllable_repetition and dataRMS is not None and meanRMS is not None:  # Only plot RMS if it's not None
            plt.subplot(3, 1, 3)  # Third subplot

            # Ensure time_axis and dataRMS have the same length
            min_len = min(len(time_axis), len(dataRMS)) if time_axis is not None else len(dataRMS)
            plt.plot(time_axis[:min_len], dataRMS[:min_len], label="RMS Energy", color='b') if time_axis is not None else plt.plot(dataRMS[:min_len], label="RMS Energy", color='b')

            # Overlay detected syllable onsets and offsets
            for st, en in zip(startPeaks, endPeaks):
                # Convert start and end peaks to indices if necessary
                st_idx = int(st * self.fs) if time_axis is None else np.searchsorted(time_axis, st)
                en_idx = int(en * self.fs) if time_axis is None else np.searchsorted(time_axis, en)

                plt.axvline(x=time_axis[st_idx] if time_axis is not None else st, color='g', linestyle='--')  # Green for Onset
                plt.axvline(x=time_axis[en_idx] if time_axis is not None else en, color='r', linestyle='--')  # Red for Offset

            # Add mean RMS points: 
            if meanRMS is not None:
                # Calculate midpoints between start and end peaks for positioning:
                midpoints = [(st + en) / 2 for st, en in zip(startPeaks, endPeaks)]
                
                # Plot mean RMS energy values:
                plt.scatter(midpoints, meanRMS, color='purple', s=50, zorder=5, label="Mean RMS per syllable")
                
                # Add fitted line:
                if len(meanRMS) > 1:
                    # Fit a line to the time-domain data points
                    time_slope, time_intercept = np.polyfit(midpoints, meanRMS, 1)
                    
                    # Create line points
                    x_line = np.array([min(midpoints), max(midpoints)])
                    y_line = time_slope * x_line + time_intercept
                    
                    plt.plot(x_line, y_line, color='red', linestyle='-', 
                            label=f'Fitted line (slope = {time_slope:.6f})')

            plt.xlabel("Time (seconds)")
            plt.ylabel("RMS Energy")
            plt.legend()
            plt.title("RMS Energy with Detected Syllable Segments and Mean RMS Analysis")

        # Add Square Over the 5-Second Window (Only for Syllable Repetition, not PR)
        if is_syllable_repetition:
            first_onset = startPeaks[0]
            window_duration = 5  # 5 seconds window
            window_start_idx = int(first_onset * self.fs)
            window_end_idx = int((first_onset + window_duration) * self.fs)

            # Ensure the window doesn't exceed the data length
            window_end_idx = min(window_end_idx, len(dataTKEO))

            # Convert to time for plotting (if using time_axis)
            if time_axis is not None:
                window_start_time = time_axis[window_start_idx]
                window_end_time = time_axis[window_end_idx]
            else:
                window_start_time = window_start_idx / self.fs
                window_end_time = window_end_idx / self.fs

            # Add a patch to the plot to highlight the 5-second window:
            plt.gca().add_patch(
                plt.Rectangle(
                    (window_start_time, np.min(dataTKEO)),  # (x, y) position (start time, min value of TKEO)
                    window_end_time - window_start_time,    # width (duration in seconds)
                    np.max(dataTKEO) - np.min(dataTKEO),    # height (range of TKEO values)
                    linewidth=2, edgecolor='b', facecolor='none', linestyle='--', label="5s Window"
                )
            )

        plt.tight_layout()                                          
        plt.savefig(os.path.join(figPath, self.filename + '.png'))
        plt.close()

        return None
    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS: EXECUTE DETECTION FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class exeDetectionFunctions():

    # INITIALISE:
    def __init__(self, files, filenames, df_voiced, figPath, sizeEpoch=0.25, overlap=0.75, thresh_multiplier=1,
                 n_devices=3):
        self.files = files
        self.filenames = filenames
        self.df_voiced = df_voiced
        self.figPath = figPath
        self.thresh_multiplier = thresh_multiplier
        self.sizeEpoch = sizeEpoch
        self.overlap = overlap
        self.n_devices = n_devices

        # Pre-process audio files outside the loop to avoid redundant computations:
        self.processed_data = [
            (preProcess_Audio(file).preProcess_resample(), filename)
            for file, filename in zip(self.files, self.filenames)
        ]

    def voiceDetector(self, detection_type):

        # Extract base type to remove any trailing numbers:
        base_type = ''.join([c for c in detection_type if not c.isdigit()])

        # Handle different task types:
        detection_map = {
            'SV': 'voicedUnvoiced_SustainedVowel',
            'PR': 'voicedUnvoiced_PassageReading',
            'SR': 'voicedUnvoiced_SyllableRepetition'
        }

        # Create a separate dataframe for RMS values if doing SR detection:
        df_rms = None
        if base_type == 'SR':
            # Create a new DataFrame with the same structure as df_voiced for the identifiers:
            df_rms = pd.DataFrame(columns=['pID', 'meanRMS', 'rms_slope'])
            if self.n_devices == 1:
                df_rms['pID'] = self.df_voiced['pID'].copy()
            
        # Check for valid task type:
        if base_type not in detection_map:
            print(f"Error! Invalid detection type: {base_type}")
            return self.df_voiced, df_rms

        detect_func = detection_map[base_type]

        # Process each file:
        for j, (data_list, filename) in enumerate(self.processed_data):
            print(j, ':', filename)

            # Get processed data and sampling frequency:
            data, fs = data_list

            # Create detection object:
            detect = detectionFunctions(data, fs, filename, self.sizeEpoch, self.overlap, self.thresh_multiplier)

            # Call corresponding detection function:
            if detect_func == 'voicedUnvoiced_SyllableRepetition':
                # Handle the additional return values for SyllableRepetition
                onset, offset, meanRMS, rms_slope = getattr(detect, detect_func)(self.figPath)
                
                # Store RMS values in the separate dataframe
                if self.n_devices == 1:
                    df_rms.at[j, 'meanRMS'] = meanRMS
                    df_rms.at[j, 'rms_slope'] = rms_slope
                elif self.n_devices > 1:
                    prefix_1, _, prefix_2 = filename.split('_')
                    matching_rows = self.df_voiced[
                        self.df_voiced['pID'].str.contains(prefix_1) & self.df_voiced['pID'].str.contains(prefix_2)]
                    
                    for idx in matching_rows.index:
                        # Add a new row to df_rms
                        new_row = pd.DataFrame({'pID': [self.df_voiced.at[idx, 'pID']], 
                                            'meanRMS': [meanRMS], 
                                            'rms_slope': [rms_slope]})
                        df_rms = pd.concat([df_rms, new_row], ignore_index=True)
            else:
                # Original behavior for other detection types:
                onset, offset = getattr(detect, detect_func)(self.figPath)

            # Efficiently update the df_voiced based on the number of devices:
            if self.n_devices == 1:
                # Store onset and offset as lists in the DataFrame:
                self.df_voiced.at[j, 'onset'] = onset           # Store as list of onsets
                self.df_voiced.at[j, 'offset'] = offset         # Store as list of offsets
            elif self.n_devices > 1:
                # Extract identifiers:
                prefix_1, _, prefix_2 = filename.split('_')
                matching_rows = self.df_voiced[
                    self.df_voiced['pID'].str.contains(prefix_1) & self.df_voiced['pID'].str.contains(prefix_2)]

                # Only update matching rows:
                self.df_voiced.loc[matching_rows.index, 'onset'] = onset        # Store as list of onsets
                self.df_voiced.loc[matching_rows.index, 'offset'] = offset      # Store as list of offsets
            else:
                print('Error! Input the right number of devices.')

        # Return the correct result:
        if base_type == 'SR':
            return self.df_voiced, df_rms
        else:
            return self.df_voiced, None  # For any non-SR tasks.
        
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% IF MAIN SCRIPT EXECUTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# If this script is run directly
if __name__ == "__main__":
    try:
        logger.info("Pre-processing module loaded")
    except Exception as e:
        logger.error(f"Error in main module: {str(e)}", exc_info=True)
    finally:
        # Ensure the queue listener is stopped when the script ends:
        stop_listener()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%