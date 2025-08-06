/*
  Feature names are taken from backend
  Uses those names to avoid conflicts in frontend
*/

export const SV_FEATURES_DATA = {
  'MaxPhonationTime(s)': {
    title: 'Max Phonation Time',
    description:
      'Duration of sustained vowel production at a consistent pitch and loudness. This measures how long a person can hold a vowel sound, indicating vocal endurance and respiratory support.',
    units: 's',
  },
  GNE: {
    title: 'GNE',
    description:
      'Glottal-to-Noise Excitation ratio - measures the ratio of periodic to aperiodic energy in the voice. This is a key indicator of voice quality and vocal fold function.',
    units: 'dimensionless',
  },
  SD_MFCC: {
    title: 'SD MFCC',
    description:
      'Standard deviation of Mel-frequency cepstral coefficients - measures spectral variability. This indicates stability of vocal tract configuration and voice quality consistency.',
    units: 'dimensionless',
  },
  SD_Delta: {
    title: 'SD Delta',
    description:
      'Standard deviation of first-order delta coefficients - measures rate of spectral change. This indicates how quickly the voice spectrum changes over time.',
    units: 'dimensionless',
  },
  SD_Delta2: {
    title: 'SD Delta2',
    description:
      'Standard deviation of second-order delta coefficients - measures acceleration of spectral change. This indicates the stability of spectral change rates over time.',
    units: 'dimensionless',
  },
  Median_Pitch: {
    title: 'Median Pitch',
    description:
      'The middle value of fundamental frequency measurements during sustained vowel production. This indicates the typical speaking pitch and vocal fold tension.',
    units: 'Hz',
  },
  Std_Pitch: {
    title: 'Std Pitch',
    description:
      'Standard deviation of fundamental frequency - measures pitch stability. This indicates how consistent the pitch remains during sustained vowel production.',
    units: 'Hz',
  },
  HNR: {
    title: 'HNR',
    description:
      'Harmonics-to-Noise Ratio - measures the ratio of harmonic to noise components in the voice. This is a key indicator of voice quality and vocal fold function.',
    units: 'dB',
  },
  Jitter_Local_Percentage: {
    title: 'Jitter Local Percentage',
    description:
      'Local jitter percentage - measures cycle-to-cycle variation in fundamental frequency. This indicates vocal fold vibration regularity and stability.',
    units: '%',
  },
  Jitter_RAP: {
    title: 'Jitter RAP',
    description:
      'Relative Average Perturbation - average absolute difference between consecutive periods. This measures fundamental frequency stability over time.',
    units: '%',
  },
  Jitter_PPQ5: {
    title: 'Jitter PPQ5',
    description:
      'Pitch Perturbation Quotient - measures jitter using 5-point smoothing. This is a more robust measure of pitch stability that reduces noise effects.',
    units: '%',
  },
  Jitter_DDP: {
    title: 'Jitter DDP',
    description:
      'Difference of Differences of Periods - measures jitter using period-to-period differences. This is an advanced measure of vocal fold vibration regularity.',
    units: '%',
  },
  Shimmer_LocaldB: {
    title: 'Shimmer Local dB',
    description:
      'Local shimmer in decibels - measures cycle-to-cycle amplitude variation. This indicates amplitude stability of vocal fold vibration.',
    units: 'dB',
  },
  Shimmer_APQ3: {
    title: 'Shimmer APQ3',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 3-point smoothing. This is a robust measure of amplitude stability that reduces noise effects.',
    units: '%',
  },
  Shimmer_APQ5: {
    title: 'Shimmer APQ5',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 5-point smoothing. This is a more robust measure of amplitude stability with increased smoothing.',
    units: '%',
  },
  Shimmer_APQ11: {
    title: 'Shimmer APQ11',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 11-point smoothing. This is the most robust measure of amplitude stability with maximum smoothing.',
    units: '%',
  },
  Shimmer_DDA: {
    title: 'Shimmer DDA',
    description:
      'Difference of Differences of Amplitudes - measures shimmer using amplitude differences. This is an advanced measure of amplitude stability using period-to-period differences.',
    units: '%',
  },
};

export const SV_FEATURE_LIST = [
  'MaxPhonationTime(s)',
  'GNE',
  'SD_MFCC',
  'SD_Delta',
  'SD_Delta2',
  'Median_Pitch',
  'Std_Pitch',
  'HNR',
  'Jitter_Local_Percentage',
  'Jitter_RAP',
  'Jitter_PPQ5',
  'Jitter_DDP',
  'Shimmer_LocaldB',
  'Shimmer_APQ3',
  'Shimmer_APQ5',
  'Shimmer_APQ11',
  'Shimmer_DDA',
];

export const SR_FEATURES_DATA = {
  'TST(s)': {
    title: 'Total Speech Time',
    description:
      'Total duration of speech activity within the 5-second analysis window. This measures the overall time spent producing syllable repetitions.',
    units: 's',
  },
  'TPT(s)': {
    title: 'Total Pause Time',
    description:
      'Total duration of pauses between syllable repetitions. This measures the cumulative time spent in silence between speech segments.',
    units: 's',
  },
  'PR(%)': {
    title: 'Pause Ratio',
    description:
      'Percentage of total time spent in pauses relative to total speech time. This indicates the proportion of silence in the speech pattern.',
    units: '%',
  },
  'NST(s)': {
    title: 'Net Speech Time',
    description:
      'Total speech time minus total pause time. This represents the actual time spent producing speech sounds.',
    units: 's',
  },
  'intDur(s)': {
    title: 'Interval Duration',
    description:
      'Average time between consecutive syllable repetitions. This measures the rhythm and timing of syllable production.',
    units: 's',
  },
  'MeanPauseTime(s)': {
    title: 'Mean Pause Time',
    description:
      'Average duration of individual pauses between syllable repetitions. This indicates the typical pause length.',
    units: 's',
  },
  NRep: {
    title: 'Number of Repetitions',
    description:
      'Total count of syllable repetitions within the 5-second analysis window. This measures repetition frequency.',
    units: 'count',
  },
  'Syl Rep Rate (NST)': {
    title: 'Syllable Repetition Rate (NST)',
    description:
      'Number of repetitions per second of net speech time. This measures repetition rate during actual speech production.',
    units: 'repetitions/s',
  },
  'Syl Rep Rate (TST)': {
    title: 'Syllable Repetition Rate (TST)',
    description:
      'Number of repetitions per second of total speech time. This measures overall repetition rate including pauses.',
    units: 'repetitions/s',
  },
  PauseSlope: {
    title: 'Pause Slope',
    description:
      'Rate of change in pause durations across repetitions. Positive values indicate increasing pause times, negative values indicate decreasing pause times.',
    units: 's/repetition',
  },
  'PauseSlope Desc': {
    title: 'Pause Slope Description',
    description:
      'Description of pause slope direction: "Increasing" (longer pauses over time), "Decreasing" (shorter pauses over time), or "Flat" (consistent pause times).',
    units: 'dimensionless',
  },
  'MeanUtteranceTime(s)': {
    title: 'Mean Utterance Time',
    description:
      'Average duration of individual syllable utterances. This measures the typical length of each syllable production.',
    units: 's',
  },
  'Utterance Ratio': {
    title: 'Utterance Ratio',
    description:
      'Ratio of utterance duration to interval duration. This measures the proportion of time spent speaking versus total time.',
    units: 'dimensionless',
  },
  UtteranceSlope: {
    title: 'Utterance Slope',
    description:
      'Rate of change in utterance durations across repetitions. Positive values indicate increasing utterance times, negative values indicate decreasing utterance times.',
    units: 's/repetition',
  },
  'UtteranceSlope Desc': {
    title: 'Utterance Slope Description',
    description:
      'Description of utterance slope direction: "Increasing" (longer utterances over time), "Decreasing" (shorter utterances over time), or "Flat" (consistent utterance times).',
    units: 'dimensionless',
  },
  'Task Failure': {
    title: 'Task Failure',
    description:
      'Indicates whether the participant failed to complete the syllable repetition task within the required time frame.',
    units: 'dimensionless',
  },
};

export const SR_FEATURE_LIST = [
  'TST(s)',
  'NST(s)',
  'TPT(s)',
  'PR(%)',
  'intDur(s)',
  'MeanPauseTime(s)',
  'NRep',
  'Syl Rep Rate (NST)',
  'Syl Rep Rate (TST)',
  'PauseSlope',
  'PauseSlope Desc',
  'MeanUtteranceTime(s)',
  'Utterance Ratio',
  'UtteranceSlope',
  'UtteranceSlope Desc',
  'Task Failure',
];

export const PR_FEATURES_DATA = {
  // Temporal Features
  'TST(s)': {
    title: 'Total Speech Time',
    description:
      'Total duration of speech activity during paragraph reading. This measures the overall time spent producing speech sounds.',
    units: 's',
  },
  'NST(s)': {
    title: 'Net Speech Time',
    description:
      'Total speech time minus total pause time. This represents the actual time spent producing speech sounds.',
    units: 's',
  },
  'TPT(s)': {
    title: 'Total Pause Time',
    description:
      'Total duration of pauses during paragraph reading. This measures the cumulative time spent in silence between speech segments.',
    units: 's',
  },
  'MeanPauseTime(s)': {
    title: 'Mean Pause Time',
    description:
      'Average duration of individual pauses during paragraph reading. This indicates the typical pause length.',
    units: 's',
  },
  'PR(%)': {
    title: 'Pause Ratio',
    description:
      'Percentage of total time spent in pauses relative to total speech time. This indicates the proportion of silence in the speech pattern.',
    units: '%',
  },
  PauseSlope: {
    title: 'Pause Slope',
    description:
      'Rate of change in pause durations across utterances. Positive values indicate increasing pause times, negative values indicate decreasing pause times.',
    units: 's/utterance',
  },
  'PauseSlope Desc': {
    title: 'Pause Slope Description',
    description:
      'Description of pause slope direction: "Increasing" (longer pauses over time), "Decreasing" (shorter pauses over time), or "Flat" (consistent pause times).',
    units: 'dimensionless',
  },
  'MeanUtteranceTime(s)': {
    title: 'Mean Utterance Time',
    description:
      'Average duration of individual utterances during paragraph reading. This measures the typical length of each speech segment.',
    units: 's',
  },
  'Utterance Ratio': {
    title: 'Utterance Ratio',
    description:
      'Ratio of utterance duration to interval duration. This measures the proportion of time spent speaking versus total time.',
    units: 'dimensionless',
  },
  UtteranceSlope: {
    title: 'Utterance Slope',
    description:
      'Rate of change in utterance durations across the reading. Positive values indicate increasing utterance times, negative values indicate decreasing utterance times.',
    units: 's/utterance',
  },
  'UtteranceSlope Desc': {
    title: 'Utterance Slope Description',
    description:
      'Description of utterance slope direction: "Increasing" (longer utterances over time), "Decreasing" (shorter utterances over time), or "Flat" (consistent utterance times).',
    units: 'dimensionless',
  },
  'intDur(s)': {
    title: 'Interval Duration',
    description:
      'Average time between consecutive utterances during paragraph reading. This measures the rhythm and timing of speech production.',
    units: 's',
  },
  NRep: {
    title: 'Number of Repetitions',
    description:
      'Total count of utterances during paragraph reading. This measures speech segment frequency.',
    units: 'count',
  },
  'Syl Rep Rate (NST)': {
    title: 'Syllable Repetition Rate (NST)',
    description:
      'Number of repetitions per second of net speech time. This measures repetition rate during actual speech production.',
    units: 'repetitions/s',
  },
  'Syl Rep Rate (TST)': {
    title: 'Syllable Repetition Rate (TST)',
    description:
      'Number of repetitions per second of total speech time. This measures overall repetition rate including pauses.',
    units: 'repetitions/s',
  },
  'Task Failure': {
    title: 'Task Failure',
    description:
      'Indicates whether the participant failed to complete the paragraph reading task within the required time frame.',
    units: 'dimensionless',
  },
  // Novel Dysphonia Features
  GNE: {
    title: 'GNE',
    description:
      'Glottal-to-Noise Excitation ratio - measures the ratio of periodic to aperiodic energy in the voice. This is a key indicator of voice quality and vocal fold function.',
    units: 'dimensionless',
  },
  SD_MFCC: {
    title: 'SD MFCC',
    description:
      'Standard deviation of Mel-frequency cepstral coefficients - measures spectral variability. This indicates stability of vocal tract configuration and voice quality consistency.',
    units: 'dimensionless',
  },
  SD_Delta: {
    title: 'SD Delta',
    description:
      'Standard deviation of first-order delta coefficients - measures rate of spectral change. This indicates how quickly the voice spectrum changes over time.',
    units: 'dimensionless',
  },
  SD_Delta2: {
    title: 'SD Delta2',
    description:
      'Standard deviation of second-order delta coefficients - measures acceleration of spectral change. This indicates the stability of spectral change rates over time.',
    units: 'dimensionless',
  },
  // Praat Features
  Median_Pitch: {
    title: 'Median Pitch',
    description:
      'The middle value of fundamental frequency measurements during paragraph reading. This indicates the typical speaking pitch and vocal fold tension.',
    units: 'Hz',
  },
  Std_Pitch: {
    title: 'Std Pitch',
    description:
      'Standard deviation of fundamental frequency - measures pitch stability. This indicates how consistent the pitch remains during paragraph reading.',
    units: 'Hz',
  },
  HNR: {
    title: 'HNR',
    description:
      'Harmonics-to-Noise Ratio - measures the ratio of harmonic to noise components in the voice. This is a key indicator of voice quality and vocal fold function.',
    units: 'dB',
  },
  Jitter_Local_Percentage: {
    title: 'Jitter Local Percentage',
    description:
      'Local jitter percentage - measures cycle-to-cycle variation in fundamental frequency. This indicates vocal fold vibration regularity and stability.',
    units: '%',
  },
  Jitter_RAP: {
    title: 'Jitter RAP',
    description:
      'Relative Average Perturbation - average absolute difference between consecutive periods. This measures fundamental frequency stability over time.',
    units: '%',
  },
  Jitter_PPQ5: {
    title: 'Jitter PPQ5',
    description:
      'Pitch Perturbation Quotient - measures jitter using 5-point smoothing. This is a more robust measure of pitch stability that reduces noise effects.',
    units: '%',
  },
  Jitter_DDP: {
    title: 'Jitter DDP',
    description:
      'Difference of Differences of Periods - measures jitter using period-to-period differences. This is an advanced measure of vocal fold vibration regularity.',
    units: '%',
  },
  Shimmer_LocaldB: {
    title: 'Shimmer Local dB',
    description:
      'Local shimmer in decibels - measures cycle-to-cycle amplitude variation. This indicates amplitude stability of vocal fold vibration.',
    units: 'dB',
  },
  Shimmer_APQ3: {
    title: 'Shimmer APQ3',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 3-point smoothing. This is a robust measure of amplitude stability that reduces noise effects.',
    units: '%',
  },
  Shimmer_APQ5: {
    title: 'Shimmer APQ5',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 5-point smoothing. This is a more robust measure of amplitude stability with increased smoothing.',
    units: '%',
  },
  Shimmer_APQ11: {
    title: 'Shimmer APQ11',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 11-point smoothing. This is the most robust measure of amplitude stability with maximum smoothing.',
    units: '%',
  },
  Shimmer_DDA: {
    title: 'Shimmer DDA',
    description:
      'Difference of Differences of Amplitudes - measures shimmer using amplitude differences. This is an advanced measure of amplitude stability using period-to-period differences.',
    units: '%',
  },
};

export const PR_FEATURE_LIST = [
  // Temporal Features
  'TST(s)',
  'NST(s)',
  'TPT(s)',
  'MeanPauseTime(s)',
  'PR(%)',
  'PauseSlope',
  'PauseSlope Desc',
  'MeanUtteranceTime(s)',
  'Utterance Ratio',
  'UtteranceSlope',
  'UtteranceSlope Desc',
  'intDur(s)',
  'NRep',
  'Syl Rep Rate (NST)',
  'Syl Rep Rate (TST)',
  'Task Failure',
  // Novel Dysphonia Features
  'GNE',
  'SD_MFCC',
  'SD_Delta',
  'SD_Delta2',
  // Praat Features
  'Median_Pitch',
  'Std_Pitch',
  'HNR',
  'Jitter_Local_Percentage',
  'Jitter_RAP',
  'Jitter_PPQ5',
  'Jitter_DDP',
  'Shimmer_LocaldB',
  'Shimmer_APQ3',
  'Shimmer_APQ5',
  'Shimmer_APQ11',
  'Shimmer_DDA',
];
