export const SV_FEATURES_DATA = {
  'Max Phonation Time': {
    title: 'Max Phonation Time',
    description:
      'Duration of sustained vowel production at a consistent pitch and loudness. This measures how long a person can hold a vowel sound, indicating vocal endurance and respiratory support.',
    units: 's',
  },
  GNE: {
    title: 'GNE',
    description:
      'Glottal-to-Noise Excitation ratio - measures the ratio of periodic to aperiodic energy in the voice. This is a key indicator of voice quality and vocal fold function.',
    units: 'ratio (dimensionless)',
  },
  'SD MFCC': {
    title: 'SD MFCC',
    description:
      'Standard deviation of Mel-frequency cepstral coefficients - measures spectral variability. This indicates stability of vocal tract configuration and voice quality consistency.',
    units: 'dimensionless',
  },
  'SD Delta': {
    title: 'SD Delta',
    description:
      'Standard deviation of first-order delta coefficients - measures rate of spectral change. This indicates how quickly the voice spectrum changes over time.',
    units: 'dimensionless',
  },
  'SD Delta2': {
    title: 'SD Delta2',
    description:
      'Standard deviation of second-order delta coefficients - measures acceleration of spectral change. This indicates the stability of spectral change rates over time.',
    units: 'dimensionless',
  },
  'Median Pitch': {
    title: 'Median Pitch',
    description:
      'The middle value of fundamental frequency measurements during sustained vowel production. This indicates the typical speaking pitch and vocal fold tension.',
    units: 'Hz',
  },
  'Std Pitch': {
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
  'Jitter Local Percentage': {
    title: 'Jitter Local Percentage',
    description:
      'Local jitter percentage - measures cycle-to-cycle variation in fundamental frequency. This indicates vocal fold vibration regularity and stability.',
    units: '%',
  },
  'Jitter RAP': {
    title: 'Jitter RAP',
    description:
      'Relative Average Perturbation - average absolute difference between consecutive periods. This measures fundamental frequency stability over time.',
    units: '%',
  },
  'Jitter PPQ5': {
    title: 'Jitter PPQ5',
    description:
      'Pitch Perturbation Quotient - measures jitter using 5-point smoothing. This is a more robust measure of pitch stability that reduces noise effects.',
    units: '%',
  },
  'Jitter DDP': {
    title: 'Jitter DDP',
    description:
      'Difference of Differences of Periods - measures jitter using period-to-period differences. This is an advanced measure of vocal fold vibration regularity.',
    units: '%',
  },
  'Shimmer Local dB': {
    title: 'Shimmer Local dB',
    description:
      'Local shimmer in decibels - measures cycle-to-cycle amplitude variation. This indicates amplitude stability of vocal fold vibration.',
    units: 'dB',
  },
  'Shimmer APQ3': {
    title: 'Shimmer APQ3',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 3-point smoothing. This is a robust measure of amplitude stability that reduces noise effects.',
    units: '%',
  },
  'Shimmer APQ5': {
    title: 'Shimmer APQ5',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 5-point smoothing. This is a more robust measure of amplitude stability with increased smoothing.',
    units: '%',
  },
  'Shimmer APQ11': {
    title: 'Shimmer APQ11',
    description:
      'Amplitude Perturbation Quotient - measures shimmer using 11-point smoothing. This is the most robust measure of amplitude stability with maximum smoothing.',
    units: '%',
  },
  'Shimmer DDA': {
    title: 'Shimmer DDA',
    description:
      'Difference of Differences of Amplitudes - measures shimmer using amplitude differences. This is an advanced measure of amplitude stability using period-to-period differences.',
    units: '%',
  },
};

export const SV_FEATURE_LIST = [
  'Max Phonation Time',
  'GNE',
  'SD MFCC',
  'SD Delta',
  'SD Delta2',
  'Median Pitch',
  'Std Pitch',
  'HNR',
  'Jitter Local Percentage',
  'Jitter RAP',
  'Jitter PPQ5',
  'Jitter DDP',
  'Shimmer Local dB',
  'Shimmer APQ3',
  'Shimmer APQ5',
  'Shimmer APQ11',
  'Shimmer DDA',
];
