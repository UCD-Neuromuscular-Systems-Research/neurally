# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SPEECH FEATURES ACOUSTIC LONGITUDINAL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Created Ruth Filan 23/02/25 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% IMPORT LIBRARIES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Import Libraries:
import math, librosa, os
import parselmouth
import numpy as np
import pandas as pd
from parselmouth.praat import call
from scipy import signal
from scipy.signal import fftconvolve, find_peaks
import re

# Import Local Libraries:
import preProcessingAudioLongitudinal

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PRAAT FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Praat Features:
# The Praat Class performs various acoustic analyses on the participant voice recordings using the Praat software
# library.
#
# Praat() includes:
# - calculatePitch: returns the median, mean, and standard deviation of the pitch values.
# - calculateHNR: returns the mean HNR value.
# - calculateJitter: calculates various types of jitter using Praat's point process.
# - calculateShimmer: computes various types of shimmer using Praat’s functions.
# - calculateFeatures: returns a list of computed features.

class Praat():

    # Parameters:
    def __init__ (self, data, fs, fmin, fmax):
        self.sound, self.fs = parselmouth.Sound(data), fs
        self.fmin, self.fmax = fmin, fmax
        self.pointProcess = call(self.sound, "To PointProcess (periodic, cc)", fmin, fmax)

    # Pitch: returns the median, mean, and standard deviation of the pitch values.
    def calculatePitch(self):
        
        # Extract the pitch object from the sound using Praat's to_pitch function:
        pitch = self.sound.to_pitch()
        
        # Get the pitch values (frequencies) from the pitch object:
        pitch_values = pitch.selected_array['frequency']
        
        # Filter out 0 values, which represent unvoiced segments:
        pitch_values[pitch_values==0] = np.nan
        
        # Calculate the mean, median, and standard deviation of the pitch values:
        meanPitch = float(np.nanmean(pitch_values))
        medianPitch = float(np.nanmedian(pitch_values))
        stdPitch = float(np.nanstd(pitch_values))
        
        # Return: medianPitch, meanPitch, and stdPitch.
        return medianPitch, meanPitch, stdPitch

    # Harmonic-to-Noise Ratio (HNR): returns the mean HNR value.
    def calculateHNR(self):

        # Calculate the HNR using Praat's to_harmonicity function:
        harmonicity = self.sound.to_harmonicity()

        # Return: the mean HNR value, excluding -200 values (which indicate unvoiced segments?):
        return float(harmonicity.values[harmonicity.values != -200].mean())
    
    # Jitter: returns various types of jitter using Praat's point process.
    def calculateJitter(self):
        
        # Local Jitter
        jitterLocal = call(self.pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        
        # Absolute Local Jitter
        jitterAbsolute = call(self.pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        
        # RAP (Relative Average Perturbation)
        jitterRAP = call(self.pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        
        # PPQ5 (Five-point Perturbation Quotient)
        jitterPPQ5 = call(self.pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
        
        # DDP (Difference of Differences Perturbation)
        jitterDDP = call(self.pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
        
        # Returns: all jitter measures.
        return jitterLocal, jitterAbsolute, jitterRAP, jitterPPQ5, jitterDDP
        
    # Shimmer: computes various types of shimmer using Praat’s functions.
    def calculateShimmer(self):
        
        # Local Shimmer
        shimmerLocal =  call([self.sound, self.pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        # Local Shimmer in dB
        shimmerLocaldB = call([self.sound, self.pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        # APQ3, APQ5, and APQ11 (Average Perturbation Quotients)
        shimmerAPQ3 = call([self.sound, self.pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        shimemrAPQ5 = call([self.sound, self.pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        shimmerAPQ11 =  call([self.sound, self.pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        # DDA (Difference of Differences Amplitude)
        shimmerDDA = call([self.sound, self.pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        
        # Returns: all shimmer measures.
        return shimmerLocal, shimmerLocaldB, shimmerAPQ3, shimemrAPQ5, shimmerAPQ11, shimmerDDA
    
    # Features: calls all functions in the Praat() class and returns a DataFrame
    def getFeaturesPraat(self):
        
        # Pitch:
        medianPitch, meanPitch, stdPitch = self.calculatePitch()
        
        # HNR:
        praatHNR = self.calculateHNR()
        
        # Jitter:
        jitterLocal, jitterAbsolute, jitterRAP, jitterPPQ5, jitterDDP = self.calculateJitter()

        # Shimmer:
        shimmerLocal, shimmerLocaldB, shimmerAPQ3, shimmerAPQ5, shimmerAPQ11, shimmerDDA = self.calculateShimmer()
        
        # Combine features in a dictionary:
        PraatFeat = {
            "Median_Pitch": medianPitch,
            "Std_Pitch": stdPitch,
            "HNR": praatHNR,
            "Jitter_Local_Percentage": jitterLocal * 100,  # Convert to percentage
            "Jitter_RAP": jitterRAP,
            "Jitter_PPQ5": jitterPPQ5,
            "Jitter_DDP": jitterDDP,
            "Shimmer_LocaldB": shimmerLocaldB,
            "Shimmer_APQ3": shimmerAPQ3,
            "Shimmer_APQ5": shimmerAPQ5,
            "Shimmer_APQ11": shimmerAPQ11,
            "Shimmer_DDA": shimmerDDA
        }
        
        # Convert to a DataFrame:
        dfPraatFeat = pd.DataFrame([PraatFeat])
        
        # Returns: A DataFrame containing computed features
        return dfPraatFeat
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END PRAAT FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% NOVEL DYSPHONIA MEASURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Novel Dysphonia Measures:
# The Novel Dysphonia Measures Class is designed to analyse the participant voice recordings for dysphonia.
#
# novelDysphoniaMeasures() includes:
# - GNE: returns Glottal-to-Noise Excitation (GNE) measure, which quantifies the amount of noise in the voice signal.
# - MFCCs: returns Mel Frequency Cepstral Coefficients (MFCCs) and their derivatives.

class NovelDysphoniaMeasures():

    def __init__(self, data, fs):
        self.data = data
        self.fs = fs
        self.new_fs = 10000         # Downsampled frequency
    
    # Glottal-to-Noise Excitation (GNE):
    def GNE(self):
        
        # Downsample the audio signal to a lower frequency (10 kHz):
        data10k = librosa.resample(y=self.data, orig_sr=self.fs, target_sr=self.new_fs)

        # Pre-Emphasis Filter:
        # Apply a pre-emphasis filter to boost high frequencies:
        # Note: A pre-emphasis filter is a signal processing technique that boosts the higher frequencies of a signal 
        # before transmission or recording, aiming to improve the signal-to-noise ratio (SNR) and reduce noise.
        y_preEmph = librosa.effects.preemphasis(data10k, return_zf=False)

        # Fast Fourier Transformation (FFT) Transformation:
        # Convert signal from the time-domain to frequency domain using FFT.
        dftSignal = np.fft.fft(y_preEmph)
        freq = np.abs(np.fft.fftfreq(n=len(y_preEmph), d=1/self.new_fs))

        # Frequency Band Separation:
        # Divide the signal into three frequency bands (0-750 Hz, 750-1500 Hz, and 1500-2250 Hz):
        lowLim = [0, 750, 1500]
        highLim = [750, 1500, 2250]
        bandSig = [dftSignal[np.where((freq>=i) & (freq <=j))] for i,j in zip(lowLim, highLim)]
        signalFinal = np.zeros((3, len(dftSignal)))

        # Band Isolation, Hilbert Transform & Envelope Calculation:
        for i in range(len(bandSig)):
            
            # Isolate Bands i.e. zero all other frequencies:
            zeroSig = np.zeros(len(dftSignal))
            mask = (freq >= lowLim[i]) & (freq <= highLim[i])
            zeroSig[mask] = np.hanning(len(bandSig[i]))
            zeroSig[-np.sum(mask):] = np.hanning(len(bandSig[i]))

            bandSig_temp = np.multiply(dftSignal, zeroSig)
            timeSignal = np.abs(np.fft.ifft(bandSig_temp))

            # Hilbert Transform & Envelope Calculation:
            envHilb = np.abs(signal.hilbert(np.real(timeSignal)))
            signalFinal[i, :] = envHilb
    
        # Correlation Coefficient: 
        # Calculate the maximum correlation coefficient between the separated bands:
        corrCoef = np.max([np.corrcoef(signalFinal[i], signalFinal[j])[0, 1] 
                           for i in range(3) for j in range(i + 1, 3)])

        # GNE Calculation: 
        # Computes GNE using the formula:
        GNE_final = 10 * np.log10(corrCoef / (1 - corrCoef))
        
        return GNE_final
    
    def MFCCs(self):
        # Compute MFCCs
        mfccs = librosa.feature.mfcc(y=self.data, sr=self.fs, n_mfcc=13)

        # Compute the 1st (Delta) and 2nd (Delta-Delta) Derivatives of the MFCCs:
        delta = librosa.feature.delta(mfccs, mode='nearest')
        delta2 = librosa.feature.delta(mfccs, order=2, mode='nearest')

        # Compute MEAN and S.D. of MFCCs & Derivatives:
        # MFCCs: MEAN and S.D. of the MFCCs:
        meanMFCC = np.mean(np.mean(mfccs, axis=1))
        SDMFCC = np.mean(np.std(mfccs, axis=1))

        # 1st (Delta) MFCCs: MEAN and S.D. of the 1st derivative of MFCCs:
        meanDelta = np.mean(np.mean(delta, axis=1))
        SDDelta = np.mean(np.std(delta, axis=1))
        
        # 2nd (Delta-Delta) MFCCs: MEAN and S.D. of the 2nd derivative of MFCCs:
        meanDelta2 = np.mean(np.mean(delta2, axis=1))
        SDDelta2 = np.mean(np.std(delta2, axis=1))
        
        # Returns: SDMFCC, SDDelta, SDDelta2.
        return SDMFCC, SDDelta, SDDelta2
    
    def getNovelDysphoniaFeatures(self):

        # Compute features:
        gne = self.GNE()
        sd_mfcc, sd_delta, sd_delta2 = self.MFCCs()

        # Create DataFrame:
        NovelDysphoniaFeat = {
            "GNE": [gne],
            "SD_MFCC": [sd_mfcc],
            "SD_Delta": [sd_delta],
            "SD_Delta2": [sd_delta2]
        }

        return pd.DataFrame(NovelDysphoniaFeat)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END NOVEL DYSPHONIA FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TEMPORAL FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Temporal Speech Features:
# The timeFeatures class is designed to extract temporal features related to speech, such as phonation time, speech
# rate, and pause ratio.
#
# timeFeatures() includes:
# - timeFeaturesSR: calculates temporal features for the Syllable Repetition task.
# - timeFeaturesPR: calculates temporal features for the Passage Reading task.

class timeFeatures():

    # Parameters:
    # fs: The sampling frequency of the audio signal.
    # onset_temp: The onset times of voiced segments.
    # offset_temp: The offset times of voiced segments.
    # diffSignal: The signal difference, used to calculate the maximum phonation time (MPT).
    def __init__ (self, fs, onset_temp, offset_temp, diffSignal):
        self.fs, self.onset, self.offset, self.diffSignal = fs, onset_temp, offset_temp, diffSignal

    # Temporal Syllable Repetition Features (timeFeaturesSR):
    # TST (s): Total Speech Time, the amount of time the speaker was actively producing speech within the 5-second window.
    # NST (s): Net Speech Time, the total speech time minus the pause time.
    # TPT (s): Total Pause Time, the amount of time the speaker was paused during the task.
    # Mean Pause Time (s): The average duration of pauses during the task, calculated across all valid pause periods.
    # PR (%): Pause Ratio, the percentage of the total speech time spent on pauses. This is calculated as the ratio of Total Pause Time (TPT) to Total Speech Time (TST).
    # Pause Slope: The rate of change in the pause durations over repetitions. It shows whether pauses are increasing, decreasing, or remaining constant over time.
    # Pause Slope Description: A categorical description of the pause slope, indicating whether it is increasing, decreasing, or flat.
    # Mean Utterance Time (s): The average duration of utterances within the valid window. This is the time between onsets and offsets of valid speech segments.
    # Utterance Slope: The rate of change in utterance durations over repetitions. It shows whether utterance lengths are increasing, decreasing, or remaining constant over time.
    # Utterance Slope Description: A categorical description of the utterance slope, indicating whether it is increasing, decreasing, or flat.
    # Interval Duration (s): The mean duration between speech onsets in the valid 5-second window. This measures how frequently onsets occur.
    # NRep (#): The number of valid repetitions within the 5-second window, counting how many speech segments occurred in that time frame.
    # Syl Rep Rate (NST): Syllable Repetition Rate based on Net Speech Time (NST), which is the number of repetitions per unit of net speech time.
    # Syl Rep Rate (TST): Syllable Repetition Rate based on Total Speech Time (TST), which is the number of repetitions per unit of total speech time.
    # Task Failure: A binary value (1 or 0) indicating whether the task was considered a failure. 
    # Note: The task is considered a failure if the total speech time is below the threshold (5 seconds), and the speaker did not continue after a pause 
    # (based on mean pause time). A value of 1 indicates a task failure, and 0 indicates no failure.
    def timeFeaturesSR(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Total Speech Time (TST) - (s)
        # Identify the last onset within 5 seconds:
        valid_onsets = [onset for onset in self.onset if onset - self.onset[0] <= 5 * self.fs]

        # Select the corresponding offset, accounting for onset within 5s but offset ocurs after, include the onset/offset pair:
        if valid_onsets:
            last_valid_onset = valid_onsets[-1]                             # Last onset within 5s.
            final_offset = self.offset[self.onset.index(last_valid_onset)]
        else:
            final_offset = self.offset[-1]                                  # Default to last offset.

        # Total Speech Time (TST) Calculation:
        tst = (final_offset - self.onset[0]) / self.fs

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Pause Durations & Total Pause Time (TPT) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Total Pause Time (TPT) - (s)
        # Identify the indices of onsets and offsets that are included in TST 5s Window:
        valid_indices = [i for i, onset in enumerate(self.onset) if onset <= final_offset] 

        # Extract valid onsets and offsets:
        valid_onsets = [self.onset[i] for i in valid_indices]
        valid_offsets = [self.offset[i] for i in valid_indices]

        # Compute Pause Durations i.e. offset-to-onset gap:
        pause_durations = [(valid_onsets[n + 1] - valid_offsets[n]) / self.fs for n in range(len(valid_onsets) - 1)]

        # Total Pause Time (TPT)
        tpt = np.sum(pause_durations)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Pause Ratio (%) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Pause Ratio (PR %)
        pr = 100 * (tpt / tst) if tst > 0 else np.nan  # Avoid division by zero

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Net Speech Time (NST) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Net Speech Time (NST)
        nst = tst - tpt

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interval Duration (intDur) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Compute Interval Durations - i.e. onset-to-onset for the 5s window of interest:
        intDur = np.mean([(valid_onsets[n + 1] - valid_onsets[n]) / self.fs for n in range(len(valid_onsets) - 1)]) if len(valid_onsets) > 1 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Mean Pause Time (MPT) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Mean Pause Time (MPT)
        mpt = np.nanmean(pause_durations) if len(pause_durations)>0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Number of Repetitions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Number of Repetitions within the 5s window
        NRep = len(valid_onsets)  # Count valid onsets within the 5s window.

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SylRepRate based on NST and TST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # SylRepRateNST: Syllable Repetition Rate based on Net Speech Time (NST)
        sylRepRateNST = NRep / nst if nst > 0 else np.nan

        # SylRepRateTST: Syllable Repetition Rate based on Total Speech Time (TST)
        sylRepRateTST = NRep / tst if tst > 0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Generate Repetition Indices and Pause Slope ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Generate Repetition Indices:
        pauseReps = np.arange(1, len(pause_durations) + 1)

        # Calculate Slope of Pause Durations over Repetitions:
        pause_slope = np.nan
        pauseslope_description = "Not Applicable"                                    # Default if slope can't be calculated
        if len(set(pause_durations)) > 1:                                            # Ensure at least 2 unique values for slope calculation
            pause_slope, _ = np.polyfit(pauseReps, pause_durations, 1)               # Calculate Slope
            
            # Check the direction of the slope
            if pause_slope > 0:
                pauseslope_description = "Increasing"                                # Increasing Pause Slope                           
            elif pause_slope < 0:
                pauseslope_description = "Decreasing"                                # Decreasing Pause Slope
            else:
                pauseslope_description = "Flat"                                      # No change, slope is zero
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utterance Durations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Calculate Utterance Durations (offset - onset) for valid onsets and offsets within the 5s window:
        utterance_durations = [(valid_offsets[n] - valid_onsets[n]) / self.fs for n in range(len(valid_onsets))]

        # Calculate the mean utterance time (mut):
        mut = np.mean(utterance_durations) if len(utterance_durations) > 0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utterance Slope and Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Generate Utterance Repetition Indices:
        uttReps = np.arange(1, len(utterance_durations) + 1)

        # Calculate Slope of Utterance Durations over Repetitions:
        utterance_slope = np.nan
        utteranceslope_description = "Not Applicable"                           # Default if slope can't be calculated
        if len(set(utterance_durations)) > 1:                                   # Ensure at least 2 unique values for slope calculation
            utterance_slope, _ = np.polyfit(uttReps, utterance_durations, 1)    # Calculate Slope
            
            # Check the direction of the slope
            if utterance_slope > 0:
                utteranceslope_description = "Increasing"                       # Increasing Utterance Slope
            elif utterance_slope < 0:
                utteranceslope_description = "Decreasing"                       # Decreasing Utterance Slope
            else:
                utteranceslope_description = "Flat"                             # No change, slope is zero
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculate the Ratio for Each Utterance ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        utterance_ratios = []

        # Loop through each utterance except the last one:
        for i in range(len(valid_onsets) - 1):  
            # Calculate the utterance duration (offset - onset) for the current utterance:
            utterance_duration = (valid_offsets[i] - valid_onsets[i]) / self.fs

            # Calculate the interval duration (onset to onset) for the current interval:
            interval_duration = (valid_onsets[i + 1] - valid_onsets[i]) / self.fs

            # Calculate the ratio of utterance duration to interval duration - avoid division by zero:
            if interval_duration > 0: 
                ratio = utterance_duration / interval_duration
                utterance_ratios.append(ratio)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculate the Average of These Ratios ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if len(utterance_ratios) > 0:
            avg_utterance_dur_ratio = np.mean(utterance_ratios)
        else:
            avg_utterance_dur_ratio = np.nan  # If no valid ratios, set as NaN

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Task Failure Definition (Based on TST and Pause Gap) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Check if TST is less than 5 seconds - as defined in the task failure criteria:
        if tst < 5:  
            # Define the last valid offset:
            last_valid_offset = valid_offsets[-1] if valid_offsets else np.nan
            
            # Check for false task failure definitions due to pauses at 5s, i.e. the speaker continued after 5s after a reasonble mean pause time:
            # Check whether there is an onset occuring AFTER the last valid offset, meaning the speaker continued after 5 second window:
            next_onset = next((onset for onset in self.onset if onset > last_valid_offset), None)
            
            if next_onset is None:
                # If no further onset, it's a true task failure i.e no false detection occured:
                task_failure = 1  
            else:
                # If there is a new onset after 5s, check the gap between the last valid offset and the next onset:
                gap = (next_onset - last_valid_offset) / self.fs                       # Convert gap to seconds (s)
                
                if gap > mpt:
                    # If the gap is longer than the mean pause time, it was a valid break in task, so task is a failure:
                    task_failure = 1                                     # Task failure i.e. gap longer than usual pause
                else:
                    # If the gap is shorter or equal to the mean pause time, it was a false failure due to a pause:
                    task_failure = 0                              # Task continuation possible (gap is within pause time)
        else:
            task_failure = 0  # Task didn't fail if TST is greater than 5s

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create DataFrame with Extracted Features ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create DataFrame with Extracted Features
        dfTimeFeat = pd.DataFrame(
            columns=[
                'TST(s)', 'NST(s)',
                'TPT(s)', 'MeanPauseTime(s)', 'PR(%)', 'PauseSlope', 'PauseSlope Desc',
                'MeanUtteranceTime(s)', 'Utterance Ratio', 'UtteranceSlope', 'UtteranceSlope Desc',
                'intDur(s)',
                'NRep', 'Syl Rep Rate (NST)', 'Syl Rep Rate (TST)',
                'Task Failure'
            ],
            data=[[
                tst,                        # TST(s)
                nst,                        # NST(s)
                tpt,                        # TPT(s)
                mpt,                        # MeanPauseTime(s)
                pr,                         # Pause Ratio (%)
                pause_slope,                # Pause Slope
                pauseslope_description,     # Pause Slope Desc
                mut,                        # Mean Utterance Time(s)
                avg_utterance_dur_ratio,    # Utterance Ratio
                utterance_slope,            # Utterance Slope
                utteranceslope_description, # Utterance Slope Desc
                intDur,                     # intDur(s)
                NRep,                       # NRep
                sylRepRateNST,              # Syl Rep Rate (NST)
                sylRepRateTST,              # Syl Rep Rate (TST)
                task_failure                # Task Failure
            ]]
        )

        return dfTimeFeat
    
    # Temporal Features for the Passage Reading Task (timeFeaturesPR):
    def timeFeaturesPR(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TST (Total Speech Time) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        valid_onsets = self.onset

        if valid_onsets:
            last_valid_onset = valid_onsets[-1]
            final_offset = self.offset[self.onset.index(last_valid_onset)]
        else:
            final_offset = self.offset[-1]

        tst = (final_offset - self.onset[0]) / self.fs

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Pause Durations & Total Pause Time (TPT) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        valid_indices = [i for i, onset in enumerate(self.onset) if onset <= final_offset]
        valid_onsets = [self.onset[i] for i in valid_indices]
        valid_offsets = [self.offset[i] for i in valid_indices]

        pause_durations = [(valid_onsets[n + 1] - valid_offsets[n]) / self.fs for n in range(len(valid_onsets) - 1)]
        tpt = np.sum(pause_durations)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Pause Ratio (%) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pr = 100 * (tpt / tst) if tst > 0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Net Speech Time (NST) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        nst = tst - tpt

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interval Duration (intDur) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        intDur = np.mean([(valid_onsets[n + 1] - valid_onsets[n]) / self.fs for n in range(len(valid_onsets) - 1)]) if len(valid_onsets) > 1 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Mean Pause Time (MPT) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        mpt = np.nanmean(pause_durations) if len(pause_durations) > 0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utterance Durations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        utterance_durations = [(valid_offsets[n] - valid_onsets[n]) / self.fs for n in range(len(valid_onsets))]
        mut = np.mean(utterance_durations) if len(utterance_durations) > 0 else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utterance Slope ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        uttReps = np.arange(1, len(utterance_durations) + 1)
        utterance_slope = np.nan
        utteranceslope_description = "Not Applicable"
        if len(set(utterance_durations)) > 1:
            utterance_slope, _ = np.polyfit(uttReps, utterance_durations, 1)

            if utterance_slope > 0:
                utteranceslope_description = "Increasing"
            elif utterance_slope < 0:
                utteranceslope_description = "Decreasing"
            else:
                utteranceslope_description = "Flat"

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Task Failure Definition ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        task_failure = 0

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create DataFrame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        dfTimeFeatPR = pd.DataFrame(
            columns=[
                'TST(s)', 'NST(s)', 'TPT(s)', 'MeanPauseTime(s)', 'PR(%)', 'PauseSlope', 'PauseSlope Desc',
                'MeanUtteranceTime(s)', 'Utterance Ratio', 'UtteranceSlope', 'UtteranceSlope Desc',
                'intDur(s)', 'NRep', 'Syl Rep Rate (NST)', 'Syl Rep Rate (TST)', 'Task Failure'
            ],
            data=[[
                tst,                        # TST(s)
                nst,                        # NST(s)
                tpt,                        # TPT(s)
                mpt,                        # MeanPauseTime(s)
                pr,                         # Pause Ratio (%)
                np.nan,                     # PauseSlope
                np.nan,                     # PauseSlope Desc
                mut,                        # Mean Utterance Time(s)
                np.nan,                     # Utterance Ratio
                utterance_slope,            # Utterance Slope
                utteranceslope_description, # Utterance Slope Desc
                intDur,                     # intDur(s)
                np.nan,                     # NRep
                np.nan,                     # Syl Rep Rate (NST)
                np.nan,                     # Syl Rep Rate (TST)
                task_failure                # Task Failure
            ]]
        )

        # Return the DataFrame:
        return dfTimeFeatPR
    
    # Temporal Features for the Sustained Vowel Task (timeFeaturesSV):
    def timeFeaturesSV(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Maximum Phonation Time (MPT) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MPT is the duration of the longest continuous phonation (i.e., offset - onset)
        
        # Compute durations for each voiced segment:
        durations = [(off - on) / self.fs for on, off in zip(self.onset, self.offset)]

        # Maximum Phonation Time
        mpt = max(durations) if durations else np.nan

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create DataFrame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        dfTimeFeatSV = pd.DataFrame(
            columns=['MaxPhonationTime(s)'],
            data=[[mpt]]
        )

        return dfTimeFeatSV
    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END - TEMPORAL FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GET FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class: featuresTable() includes:
# - participantInfo
# - initDataFrame
# - getFeaturesSV
# - getFeaturesSR
# - getFeaturesPR

class featuresTable():
    # INITIALISE:
    def __init__ (self, dataPath, outputPath, group, speechTest, fmin = [75, 75], fmax = [600, 5000], nPeriods = [3,6]):
        self.dataPath, self.outputPath = dataPath, outputPath
        self.group, self.speechTest = group, speechTest
        self.fmin_list, self.fmax_list, self.nPeriods_list = fmin, fmax, nPeriods
        self.filenames, self.files = preProcessingAudioLongitudinal.open_wav(dataPath, speechTest).openFiles()
        self.dfVoiced = pd.read_csv(os.path.join(outputPath, 'onsetOffset_' + group + '_' + speechTest + '.csv'))
        self.df = self.participantInfo()
        self.dfFeatures = pd.DataFrame()

    # PARTICIPANT INFO
    def participantInfo(self):
        if self.group == "Control" or self.group == "HD":
            studyID, deviceName, testName = zip(*[(self.filenames[i].split("_")[0], 
                                      self.filenames[i].split("_")[-1], self.filenames[i].split("_")[1]) for i in range(len(self.filenames))])
            dfInfo = pd.read_csv(os.path.join(self.dataPath, 'participantInfo.csv'))
            dfInfo.drop('device', axis=1, inplace=True)
            df = pd.concat((dfInfo.loc[dfInfo['participant']==i, :]) for i in studyID).reset_index(drop=True)
            df.insert(0, 'filename', self.filenames)
            df.insert(2, 'test', testName)
            df.loc[:,'device'] = deviceName
        else:
            studyID = [self.filenames[i].split("_")[0] for i in range(len(self.filenames))]
            dfInfo = pd.read_csv(os.path.join(self.dataPath, 'participantInfo.csv'))
            df = pd.concat((dfInfo.loc[dfInfo['participant']==i, :]) for i in studyID).reset_index(drop=True)
            df.insert(0, 'filename', self.filenames)
            df.insert(2, 'test', self.speechTest)
        return df
    
    # GET FEATURES SV:
    def getFeaturesSV(self):
        dfNovelDysphonia = pd.DataFrame()  # Novel Dysphonia Feature DataFrame
        dfPraat = pd.DataFrame()           # Praat Feature DataFrame
        dfTime = pd.DataFrame()            # Temporal Feature DataFrame 

        for j in range(len(self.files)):
            filename = self.filenames[j]
            print(j, ':', filename)

            # Process the audio file:
            data_list = self.files[j]
            audioProcess = preProcessingAudioLongitudinal.preProcess_Audio(data_list)
            data, fs = audioProcess.preProcess_resample()

            # Clean and process the onset and offset fields:
            onset = self.dfVoiced.loc[j, 'onset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")
            offset = self.dfVoiced.loc[j, 'offset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")

            # Convert the onset/offset strings to integer lists:
            onset = [int(s.replace(",", "").strip()) for s in onset.split(' ')]
            offset = [int(s.replace(",", "").strip()) for s in offset.split(' ')]

            # Compute Maximum Phonation Time (MPT) only:
            dfTimeFeat = timeFeatures(fs, onset, offset, diffSignal=None).timeFeaturesSV()
            dfTime = pd.concat([dfTime, dfTimeFeat])

            # Compute Novel Dysphonia Features:
            ndm = NovelDysphoniaMeasures(data, fs)
            dfNovelDysphoniaFeat = ndm.getNovelDysphoniaFeatures()
            dfNovelDysphonia = pd.concat([dfNovelDysphonia, dfNovelDysphoniaFeat], axis=0)

            # Compute Praat Features:
            pf = Praat(data, fs, fmin=self.fmin_list[0], fmax=self.fmax_list[1])
            dfPraatFeat = pf.getFeaturesPraat()
            dfPraat = pd.concat([dfPraat, dfPraatFeat], axis=0)

        # Combine everything, including dfTime (MPT):
        self.dfFeatures = pd.concat([
            self.df.reset_index(drop=True),
            dfTime.reset_index(drop=True),
            dfNovelDysphonia.reset_index(drop=True),
            dfPraat.reset_index(drop=True)
        ], axis=1)

        # Save to CSV:
        self.dfFeatures.to_csv(os.path.join(self.outputPath, 'features_' + self.group + '_' + self.speechTest + '.csv'))

        return self.dfFeatures

    # GET FEATURES SR:
    def getFeaturesSR(self):
        dfTime = pd.DataFrame()  # Temporal feature DataFrame

        for j in range(len(self.files)):
            filename = self.filenames[j]
            print(j, ':', filename)

            data_list = self.files[j]
            audioProcess = preProcessingAudioLongitudinal.preProcess_Audio(data_list)
            data, fs = audioProcess.preProcess_resample()

            # Process the onset and offset:
            onset = self.dfVoiced.loc[j, 'onset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")
            offset = self.dfVoiced.loc[j, 'offset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")

            # Strip any leading/trailing spaces and convert the strings into lists of integers:
            onset = [int(s.replace(",", "").strip()) for s in onset.split(' ')]
            offset = [int(s.replace(",", "").strip()) for s in offset.split(' ')]

            # Temporal features:
            dfTimeFeat = timeFeatures(fs, onset, offset, diffSignal=np.subtract(offset, onset) / fs).timeFeaturesSR()
            dfTime = pd.concat([dfTime, dfTimeFeat])

        # Final DataFrame with temporal features:
        self.dfFeatures = pd.concat([self.df, dfTime.reset_index(drop=True)], axis=1)
        self.dfFeatures = self.dfFeatures.loc[:, ~self.dfFeatures.columns.str.contains('^Unnamed')]
        self.dfFeatures.to_csv(os.path.join(self.outputPath, 'features_' + self.group + '_' + self.speechTest + '.csv'))

        return self.dfFeatures
    
    # GET FEATURES PR:
    def getFeaturesPR(self):
        dfTime = pd.DataFrame()                 # Temporal Feature DataFrame
        dfNovelDysphonia = pd.DataFrame()       # Novel Dysphonia Feature DataFrame
        dfPraat = pd.DataFrame()                # Praat Feature DataFrame

        for j in range(len(self.files)):
            filename = self.filenames[j]
            print(j, ':', filename)

            # Process the audio file:
            data_list = self.files[j]
            audioProcess = preProcessingAudioLongitudinal.preProcess_Audio(data_list)
            data, fs = audioProcess.preProcess_resample()

            # Process the onset and offset:
            onset = self.dfVoiced.loc[j, 'onset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")
            offset = self.dfVoiced.loc[j, 'offset'].replace("[", "").replace("]", "").replace("\n", "").replace("  ", " ")

            # Strip any leading/trailing spaces and convert the strings into lists of integers:
            onset = [int(s.replace(",", "").strip()) for s in onset.split(' ')]
            offset = [int(s.replace(",", "").strip()) for s in offset.split(' ')]

            # Temporal features for Passage Reading:
            dfTimeFeat = timeFeatures(fs, onset, offset, diffSignal=np.subtract(offset, onset) / fs).timeFeaturesPR()
            dfTime = pd.concat([dfTime, dfTimeFeat])

            # Compute Novel Dysphonia Features:
            ndm = NovelDysphoniaMeasures(data, fs)
            dfNovelDysphoniaFeat = ndm.getNovelDysphoniaFeatures()  # GNE, SD_MFCC, SD_Delta, SD_Delta2
            
            # Concatenate the Novel Dysphonia features to the DataFrame:
            dfNovelDysphonia = pd.concat([dfNovelDysphonia, dfNovelDysphoniaFeat], axis=0)

            # Compute Praat Features:
            pf = Praat(data, fs, fmin=self.fmin_list[0], fmax=self.fmax_list[1])
            dfPraatFeat = pf.getFeaturesPraat()  
            dfPraat = pd.concat([dfPraat, dfPraatFeat], axis=0)

        # DataFrame Concatenation:
        self.dfFeatures = pd.concat([
            self.df, 
            dfTime.reset_index(drop=True), 
            dfNovelDysphonia.reset_index(drop=True), 
            dfPraat.reset_index(drop=True) 
        ], axis=1)
    
        # Save the features to a CSV file
        self.dfFeatures.to_csv(os.path.join(self.outputPath, 'features_' + self.group + '_' + self.speechTest + '.csv'))

        return self.dfFeatures

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END - GET FEATURES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END - SPEECH FEATURES ACOUSTIC LONGITUDINAL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
