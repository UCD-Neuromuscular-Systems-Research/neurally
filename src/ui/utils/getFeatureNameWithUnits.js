import { SV_FEATURES_DATA } from '../config/featuresData.js';

export const getFeatureNameWithUnits = (featureName) => {
  const featureData = SV_FEATURES_DATA[featureName];

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
