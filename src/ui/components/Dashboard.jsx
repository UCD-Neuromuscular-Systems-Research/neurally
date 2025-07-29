import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router';

function Dashboard() {
  const { testType } = useParams();
  const navigate = useNavigate();
  const [filePath, setFilePath] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const SVFeatureList = [
    'Max Phonation Time (s)',
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

  const handleFileUpload = async () => {
    try {
      const selectedFilePath = await window.electron.fileUpload();
      if (selectedFilePath) {
        setFilePath(selectedFilePath);
      }
    } catch (error) {
      console.error('Error selecting file:', error);
    }
  };

  const handleSingleFileProcessing = async () => {
    if (filePath && testType) {
      setIsProcessing(true);
      try {
        const result = await window.electron.processSingleFileHD(
          testType,
          filePath
        );

        // Try to clean the result before parsing
        let cleanResult = result;
        if (typeof result === 'string') {
          // Remove any leading/trailing whitespace
          cleanResult = result.trim();
          // If it starts with numbers or other characters, try to find the JSON part
          if (!cleanResult.startsWith('{')) {
            // Find the first '{' character
            const jsonStart = cleanResult.indexOf('{');
            if (jsonStart !== -1) {
              cleanResult = cleanResult.substring(jsonStart);
            }
          }

          // Replace Python NaN with null for valid JSON
          cleanResult = cleanResult.replace(/:\s*NaN\s*([,}])/g, ': null$1');
        }

        try {
          const parsedResult = JSON.parse(cleanResult);
          // Navigate to Results with the processing data
          navigate('/results', {
            state: {
              processingResult: parsedResult,
              testType: testType,
              filePath: filePath,
            },
          });
        } catch (parseError) {
          console.error('JSON parse error:', parseError);
          console.error('Failed to parse:', cleanResult);
          // Navigate to Results with error
          navigate('/results', {
            state: {
              error: `Failed to parse result: ${parseError.message}`,
              rawResult: cleanResult,
              testType: testType,
              filePath: filePath,
            },
          });
        }
      } catch (error) {
        console.error('Processing error:', error);
        // Navigate to Results with error
        navigate('/results', {
          state: {
            error: error.message,
            testType: testType,
            filePath: filePath,
          },
        });
      } finally {
        setIsProcessing(false);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="w-full max-w-4xl mx-auto bg-white rounded-xl shadow p-8 space-y-8">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-4">
          Sustained Vowel Test
        </h2>
        {/* Description */}
        <div className="bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200 mb-6">
          <p className="text-gray-600">
            <span className="font-bold">Description:</span> The act of holding a
            vowel sound (like "ah" or "ee") for an extended period, usually at a
            consistent pitch and loudness. This technique is often used in
            clinical settings and research to assess voice quality and identify
            potential vocal issues.
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200 mb-6">
          <p className="text-lg font-semibold text-gray-700 mb-2">
            ✅ You'll get these features for this test:
          </p>
          <ol className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 list-decimal list-inside mt-4">
            {SVFeatureList.map((feature, index) => (
              <li key={index}>{feature}</li>
            ))}
          </ol>
        </div>

        {/* Features in 3 columns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          {[].map((feature, idx) => (
            <div
              key={feature}
              className="bg-gray-100 rounded-lg p-4 flex items-center justify-center text-center font-semibold text-gray-800 text-base"
            >
              {idx + 1}. {feature}
            </div>
          ))}
        </div>
        {/* Call to Action Buttons */}
        <div className="flex flex-col items-center space-y-4">
          <button
            onClick={handleFileUpload}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Select Audio File
          </button>
          {filePath && (
            <div className="text-center">
              <p className="text-green-600 font-medium">
                File selected: {filePath.split('/').pop()}
              </p>
              <p className="text-sm text-gray-500">Path: {filePath}</p>
            </div>
          )}
          <button
            disabled={!filePath || isProcessing}
            onClick={handleSingleFileProcessing}
            className={`w-48 px-6 py-2 rounded-xl transition
              ${
                filePath && !isProcessing
                  ? 'bg-green-600 text-white hover:bg-green-700 cursor-pointer'
                  : 'bg-gray-300 text-gray-600 cursor-not-allowed'
              } flex items-center justify-center`}
          >
            {isProcessing ? (
              <>
                <svg
                  className="animate-spin h-5 w-5 mr-2 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  ></path>
                </svg>
                Processing...
              </>
            ) : (
              'Proceed'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
