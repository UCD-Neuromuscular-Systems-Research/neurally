import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router';

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const [processingResult, setProcessingResult] = useState(null);
  const [error, setError] = useState(null);
  const [filePath, setFilePath] = useState(null);
  const [plotDataUrl, setPlotDataUrl] = useState(null);
  const [plotLoading, setPlotLoading] = useState(false);

  useEffect(() => {
    if (processingResult && processingResult.plot_path) {
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
      setFilePath(location.state.filePath);

      // If there's raw result data, try to parse it
      if (location.state.rawResult) {
        try {
          const parsed = JSON.parse(location.state.rawResult);
          setProcessingResult(parsed);
        } catch (parseError) {
          setError(`Failed to parse result: ${parseError.message}`);
        }
      }
    }
  }, [location.state]);

  const renderFeaturesTable = (features) => {
    if (!features || features.length === 0) return null;

    const feature = features[0]; // Get the first (and only) feature object
    const featureEntries = Object.entries(feature);

    return (
      <table className="table-auto w-full border-collapse border border-gray-300 text-sm">
        <tbody>
          {featureEntries.map(([key, value]) => {
            // Skip certain fields that are not features
            if (['filename', 'participant', 'test'].includes(key)) return null;

            return (
              <tr key={key} className="text-center">
                <td className="border px-3 py-2 font-semibold">
                  {key.replace(/_/g, ' ')}
                </td>
                <td className="border px-3 py-2">
                  {typeof value === 'number' ? value.toFixed(4) : value}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    );
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
        Your file is processed and here&apos;s your analysis.
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
          {filePath && (
            <div className="text-sm mt-1">
              File: {filePath.split('/').pop()}
            </div>
          )}
        </div>
      )}

      {/* Plot on top */}
      <div className="w-full bg-white p-4 rounded-md shadow-sm border border-gray-200 flex items-center justify-center min-h-[400px]">
        {plotLoading ? (
          <p className="text-gray-500">Loading plot...</p>
        ) : processingResult && processingResult.plot_path && plotDataUrl ? (
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

      {/* Results table below */}
      <div className="bg-white p-4 rounded-md shadow-sm border border-gray-200">
        <h3 className="font-semibold text-lg mb-4 text-gray-700">
          Extracted Features
        </h3>
        {processingResult && processingResult.features ? (
          renderFeaturesTable(processingResult.features)
        ) : (
          <p className="text-gray-500">No features available</p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-600 text-white px-6 py-2 rounded-xl hover:bg-gray-700 transition cursor-pointer"
        >
          Go Back
        </button>
        <button
          className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition cursor-pointer"
          onClick={() => {
            console.log('Download triggered');
          }}
        >
          Download Results
        </button>
      </div>
    </div>
  );
}

export default Results;
