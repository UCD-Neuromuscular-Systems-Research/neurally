import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router';
import { getFeatureNameWithUnits } from '../utils/getFeatureNameWithUnits.js';
import { SV_FEATURES_DATA, SR_FEATURES_DATA } from '../config/featuresData.js';
import Pagination from './Pagination.jsx';
import { FILES_PER_PAGE, METADATA_FIELDS } from '../config/constants.js';

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const [processingResult, setProcessingResult] = useState(null);
  const [error, setError] = useState(null);
  const [filePaths, setFilePaths] = useState([]);
  const [testType, setTestType] = useState('SV');
  const [plotDataUrl, setPlotDataUrl] = useState(null);
  const [plotLoading, setPlotLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const roundValue = (value) => {
    if (typeof value === 'number') {
      return Number(value.toFixed(4));
    }
    return value;
  };

  useEffect(() => {
    // Handle multiple plots or single plot
    if (
      processingResult &&
      processingResult.files &&
      processingResult.files.length > 0
    ) {
      // For multi-file results, show first plot or create a gallery
      const firstFile = processingResult.files[0];
      if (firstFile.plot_path) {
        setPlotLoading(true);
        window.electron.getImageDataUrl(firstFile.plot_path).then((dataUrl) => {
          setPlotDataUrl(dataUrl);
          setPlotLoading(false);
        });
      }
    } else if (processingResult && processingResult.plot_path) {
      // For single file results (backward compatibility)
      setPlotLoading(true);
      window.electron
        .getImageDataUrl(processingResult.plot_path)
        .then((dataUrl) => {
          setPlotDataUrl(dataUrl);
          setPlotLoading(false);
        });
    } else {
      setPlotDataUrl(null);
    }
  }, [processingResult]);

  useEffect(() => {
    // Get data from navigation state
    if (location.state) {
      setProcessingResult(location.state.processingResult);
      setError(location.state.error);
      setFilePaths(location.state.filePaths || []);
      setTestType(location.state.testType || 'SV');

      // If there's raw result data, try to parse it
      if (location.state.rawResult) {
        try {
          const parsed = JSON.parse(location.state.rawResult);
          setProcessingResult(parsed);
          // eslint-disable-next-line no-unused-vars
        } catch (parseError) {
          setError('Failed to process results. Please try again.');
        }
      }
    }
  }, [location.state]);

  function featuresToCSV(features) {
    if (!features || features.length === 0) return '';
    const keys = Object.keys(features[0]);

    const displayNames = keys.map((key) =>
      getFeatureNameWithUnits(key, testType)
    );

    const header = displayNames.join(',');
    const rows = features.map((f) =>
      keys.map((k) => roundValue(f[k])).join(',')
    );
    return [header, ...rows].join('\n');
  }

  function allFeaturesToCSV(processingResult) {
    if (
      !processingResult ||
      !processingResult.files ||
      processingResult.files.length === 0
    )
      return '';

    const files = processingResult.files.filter((file) => file.features);
    if (files.length === 0) return '';

    const allFeatureNames = new Set();
    files.forEach((file) => {
      Object.keys(file.features).forEach((key) => {
        if (!METADATA_FIELDS.includes(key)) {
          allFeatureNames.add(key);
        }
      });
    });

    const featureNames = Array.from(allFeatureNames).sort();
    const displayNames = featureNames.map((key) =>
      getFeatureNameWithUnits(key, testType)
    );

    const header = ['Filename', ...displayNames].join(',');

    const rows = files.map((file) => {
      const values = featureNames.map((key) =>
        roundValue(file.features[key] || '')
      );
      return [file.filename, ...values].join(',');
    });

    return [header, ...rows].join('\n');
  }

  const openPlotInNewTab = async (plotPath, filename) => {
    try {
      const dataUrl = await window.electron.getImageDataUrl(plotPath);
      if (dataUrl) {
        const response = await fetch(dataUrl);
        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);

        const newWindow = window.open(blobUrl, '_blank');
        if (newWindow) {
          setTimeout(() => {
            newWindow.document.title = `${filename} - Voiced Detection Plot`;
          }, 100);
        }

        setTimeout(() => {
          URL.revokeObjectURL(blobUrl);
        }, 1000);
      } else {
        alert('Plot not available. Please try again.');
      }
      // eslint-disable-next-line no-unused-vars
    } catch (error) {
      alert('Failed to open plot. Please try again.');
    }
  };

  const renderFeaturesTable = (processingResult) => {
    if (!processingResult) return null;

    // Handle multi-file results
    if (processingResult.files && processingResult.files.length > 0) {
      const files = processingResult.files.filter((file) => file.features);

      if (files.length === 0)
        return <p className="text-gray-500">No features available</p>;

      // Pagination logic for 10+ files
      const totalPages = Math.ceil(files.length / FILES_PER_PAGE);
      const startIndex = (currentPage - 1) * FILES_PER_PAGE;
      const endIndex = startIndex + FILES_PER_PAGE;
      const currentFiles = files.slice(startIndex, endIndex);
      const showPagination = files.length > FILES_PER_PAGE;

      // Get all unique feature names (excluding metadata fields)
      const allFeatureNames = new Set();
      files.forEach((file) => {
        Object.keys(file.features).forEach((key) => {
          if (!METADATA_FIELDS.includes(key)) {
            allFeatureNames.add(key);
          }
        });
      });

      const featureNames = Array.from(allFeatureNames).sort();

      return (
        <div className="overflow-x-auto">
          <div className="flex justify-center">
            <table
              className="table-auto border-collapse border border-gray-300 text-sm"
              style={{
                minWidth: currentFiles.length <= 2 ? '600px' : 'none',
                maxWidth: currentFiles.length <= 5 ? '1200px' : 'none',
              }}
            >
              <thead>
                <tr className="bg-gray-50">
                  <th className="border px-3 py-2 font-semibold text-left">
                    Feature
                  </th>
                  {currentFiles.map((file, index) => (
                    <th
                      key={index}
                      className="border px-3 py-2 font-semibold text-center"
                    >
                      File {startIndex + index + 1}
                      <div className="text-xs text-gray-500 font-normal">
                        {file.filename}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Plot row at the top */}
                <tr>
                  <td className="border px-3 py-2 font-semibold text-left">
                    Voiced Detection Plot
                  </td>
                  {currentFiles.map((file, fileIndex) => (
                    <td
                      key={fileIndex}
                      className="border px-3 py-2 text-center"
                    >
                      {file.plot_path ? (
                        <button
                          onClick={() =>
                            openPlotInNewTab(file.plot_path, file.filename)
                          }
                          className="flex items-center justify-center space-x-1 text-blue-600 hover:text-blue-800 transition-colors mx-auto"
                          title={`Open plot for ${file.filename}`}
                        >
                          <span className="text-sm">View Plot</span>
                          <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                          </svg>
                        </button>
                      ) : (
                        <span className="text-gray-500 text-sm">No plot</span>
                      )}
                    </td>
                  ))}
                </tr>
                {/* Feature rows */}
                {featureNames.map((featureName) => (
                  <tr key={featureName}>
                    <td className="border px-3 py-2 font-semibold text-left">
                      {getFeatureNameWithUnits(featureName, testType)}
                    </td>
                    {currentFiles.map((file, fileIndex) => (
                      <td
                        key={fileIndex}
                        className="border px-3 py-2 text-center"
                      >
                        {file.features[featureName] !== undefined
                          ? roundValue(file.features[featureName])
                          : 'N/A'}
                      </td>
                    ))}
                  </tr>
                ))}

                {/* Download CSV row */}
                <tr>
                  <td className="border px-3 py-2 font-semibold text-left">
                    Download Features
                  </td>
                  {currentFiles.map((file, fileIndex) => (
                    <td
                      key={fileIndex}
                      className="border px-3 py-2 text-center"
                    >
                      <button
                        onClick={async () => {
                          try {
                            const csvContent = featuresToCSV([file.features]);
                            const defaultPath = `${file.filename.replace(
                              /\.[^/.]+$/,
                              ''
                            )}_features.csv`;
                            const res =
                              await window.electron.downloadResultsCSV(
                                csvContent,
                                defaultPath
                              );
                            if (res.success) {
                              alert('CSV saved!');
                            } else {
                              // Don't show error if user cancelled
                              if (
                                res.error &&
                                !res.error.includes('cancelled') &&
                                !res.error.includes('canceled')
                              ) {
                                alert('Failed to save CSV. Please try again.');
                              }
                            }
                            // eslint-disable-next-line no-unused-vars
                          } catch (error) {
                            alert('Failed to download CSV. Please try again.');
                          }
                        }}
                        className="bg-blue-600 text-white px-3 py-1 rounded-md hover:bg-blue-700 transition-colors cursor-pointer text-xs font-medium"
                        title={`Download CSV for ${file.filename}`}
                      >
                        📥 CSV
                      </button>
                    </td>
                  ))}
                </tr>

                {/* Download Plot row */}
                <tr>
                  <td className="border px-3 py-2 font-semibold text-left">
                    Download Plot
                  </td>
                  {currentFiles.map((file, fileIndex) => (
                    <td
                      key={fileIndex}
                      className="border px-3 py-2 text-center"
                    >
                      {file.plot_path ? (
                        <button
                          onClick={async () => {
                            try {
                              const defaultPath = `${file.filename.replace(
                                /\.[^/.]+$/,
                                ''
                              )}_plot.png`;
                              const res =
                                await window.electron.downloadResultsImage(
                                  file.plot_path,
                                  defaultPath
                                );
                              if (res.success) {
                                alert('Plot image saved!');
                              } else {
                                // Don't show error if user cancelled
                                if (
                                  res.error &&
                                  !res.error.includes('cancelled') &&
                                  !res.error.includes('canceled')
                                ) {
                                  alert(
                                    'Failed to save plot. Please try again.'
                                  );
                                }
                              }
                              // eslint-disable-next-line no-unused-vars
                            } catch (error) {
                              alert(
                                'Failed to download plot. Please try again.'
                              );
                            }
                          }}
                          className="bg-green-600 text-white px-3 py-1 rounded-md hover:bg-green-700 transition-colors cursor-pointer text-xs font-medium"
                          title={`Download plot for ${file.filename}`}
                        >
                          📊 Plot
                        </button>
                      ) : (
                        <span className="text-gray-500 text-xs">No plot</span>
                      )}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            showPagination={showPagination}
          />
        </div>
      );
    }

    // Handle single file results (backward compatibility)
    if (processingResult.features && processingResult.features.length > 0) {
      const feature = processingResult.features[0];
      const featureEntries = Object.entries(feature);

      return (
        <table className="table-auto w-full border-collapse border border-gray-300 text-sm">
          <tbody>
            {featureEntries.map(([featureName, value]) => {
              if (METADATA_FIELDS.includes(featureName)) return null;
              return (
                <tr key={featureName} className="text-center">
                  <td className="border px-3 py-2 font-semibold">
                    {getFeatureNameWithUnits(featureName, testType)}
                  </td>
                  <td className="border px-3 py-2">{roundValue(value)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      );
    }

    return <p className="text-gray-500">No features available</p>;
  };

  // If no data is available, show a message
  if (!processingResult && !error) {
    return (
      <div className="w-full p-6 space-y-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            No Results Available
          </h2>
          <p className="text-gray-600 mb-4">
            Please go back and process a file to see results.
          </p>
          <button
            onClick={() => navigate(-1)}
            className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full p-6 space-y-8">
      <h2 className="text-2xl font-bold text-center text-gray-800">
        Your files are processed and here&apos;s your analysis.
      </h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Error:</strong> {error}
        </div>
      )}

      {processingResult && processingResult.status === 'success' && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          <strong>Success!</strong> {processingResult.message}
          <div className="text-sm mt-1">
            Processing time: {processingResult.elapsed_seconds?.toFixed(2)}{' '}
            seconds
          </div>
          {filePaths && filePaths.length > 0 && (
            <div className="text-sm mt-1">
              Files processed: {filePaths.length}
            </div>
          )}
          {filePaths && filePaths.length > 0 && (
            <div className="text-sm mt-1">
              Files:{' '}
              {filePaths
                .map((filePath) => filePath.split('/').pop())
                .join(', ')}
            </div>
          )}
        </div>
      )}

      {/* Plot on top - only for single file */}
      {processingResult &&
        processingResult.files &&
        processingResult.files.length === 1 && (
          <div className="w-full bg-white p-4 rounded-md shadow-sm border border-gray-200 flex items-center justify-center min-h-[400px]">
            {plotLoading ? (
              <p className="text-gray-500">Loading plot...</p>
            ) : plotDataUrl ? (
              <div className="w-full aspect-[16/9] flex items-center justify-center bg-gray-100 rounded-xl overflow-hidden">
                <img
                  src={plotDataUrl}
                  alt="Voiced Detection Plot"
                  className="w-full h-full object-contain block"
                />
              </div>
            ) : (
              <p className="text-gray-500">No plot available</p>
            )}
          </div>
        )}

      {/* Results table below */}
      <div className="bg-white p-4 rounded-md shadow-sm border border-gray-200">
        <h3 className="font-semibold text-lg mb-4 text-gray-700">
          Extracted Features
        </h3>
        {processingResult ? (
          renderFeaturesTable(processingResult)
        ) : (
          <p className="text-gray-500">No features available</p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => navigate(-1)}
          className="bg-green-600 text-white px-6 py-2 rounded-xl hover:bg-green-700 transition cursor-pointer"
        >
          Process More Files
        </button>
        {processingResult &&
          processingResult.files &&
          processingResult.files.length > 1 && (
            <button
              onClick={() => {
                const csvContent = allFeaturesToCSV(processingResult);
                if (csvContent) {
                  const blob = new Blob([csvContent], { type: 'text/csv' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `${testType}_all_results.csv`;
                  document.body.appendChild(a);
                  a.click();
                  document.body.removeChild(a);
                  URL.revokeObjectURL(url);
                }
              }}
              className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition cursor-pointer"
            >
              Download All
            </button>
          )}
      </div>
    </div>
  );
}

export default Results;
