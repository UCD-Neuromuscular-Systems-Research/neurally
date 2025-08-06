import {
  SV_FEATURES_DATA,
  SR_FEATURES_DATA,
  PR_FEATURES_DATA,
} from '../config/featuresData.js';

export const getFeatureNameWithUnits = (featureName, testType = 'SV') => {
  let featuresData;
  switch (testType) {
    case 'SR':
      featuresData = SR_FEATURES_DATA;
      break;
    case 'PR':
      featuresData = PR_FEATURES_DATA;
      break;
    default:
      featuresData = SV_FEATURES_DATA;
      break;
  }
  const featureData = featuresData[featureName];

  if (
    featureData &&
    featureData.units &&
    featureData.units !== 'dimensionless'
  ) {
    return `${featureData.title} (${featureData.units})`;
  }
  return featureData ? featureData.title : featureName.replace(/_/g, ' ');
};

export const getFeatureTitleWithUnits = (selectedFeature) => {
  if (selectedFeature.units === 'dimensionless') {
    return selectedFeature.title;
  }
  return `${selectedFeature.title} (${selectedFeature.units})`;
};
