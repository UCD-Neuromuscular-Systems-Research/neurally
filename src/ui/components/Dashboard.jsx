import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import Modal from '../layout/Modal.jsx';
import {
  SV_FEATURES_DATA,
  SV_FEATURE_LIST,
  SR_FEATURES_DATA,
  SR_FEATURE_LIST,
  PR_FEATURES_DATA,
  PR_FEATURE_LIST,
} from '../config/featuresData.js';
import { getFeatureTitleWithUnits } from '../utils/getFeatureNameWithUnits.js';

function Dashboard() {
  const { testType } = useParams();
  const navigate = useNavigate();
  const [filePaths, setFilePaths] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedFeature, setSelectedFeature] = useState(null);

  const getTestData = () => {
    switch (testType) {
      case 'SV':
        return {
          title: 'Sustained Vowel Test',
          description:
            'The act of holding a vowel sound (like "ah" or "ee") for an extended period, usually at a consistent pitch and loudness. This technique is often used in clinical settings and research to assess voice quality and identify potential vocal issues.',
          featuresData: SV_FEATURES_DATA,
          featureList: SV_FEATURE_LIST,
        };
      case 'SR':
        return {
          title: 'Syllable Repetition Test',
          description:
            'The act of rapidly repeating syllables (like "pa-ta-ka") in a consistent rhythm. This technique is used to assess motor speech planning, coordination, and timing abilities.',
          featuresData: SR_FEATURES_DATA,
          featureList: SR_FEATURE_LIST,
        };
      case 'PR':
        return {
          title: 'Paragraph Reading Test',
          description:
            'The act of reading a standardized paragraph aloud. This technique is used to assess natural speech patterns, prosody, fluency, and overall communication effectiveness in a more realistic speaking context.',
          featuresData: PR_FEATURES_DATA,
          featureList: PR_FEATURE_LIST,
        };
      default:
        return {
          title: 'Speech Test',
          description: 'Speech analysis test for voice and speech assessment.',
          featuresData: {},
          featureList: [],
        };
    }
  };

  const testData = getTestData();

  // Cleanup any leftover state when component mounts
  useEffect(() => {
    // Reset any potential leftover state
    setIsModalOpen(false);
    setSelectedFeature(null);
    setIsProcessing(false);
    setFilePaths([]);

    const cleanupPreviousOutput = async () => {
      try {
        await window.electron.cleanupOutputDirectory();
      } catch (cleanupError) {
        console.warn('Cleanup warning:', cleanupError);
      }
    };

    cleanupPreviousOutput();
  }, []);

  const handleFileUpload = async () => {
    try {
      const selectedFilePaths = await window.electron.fileUpload();
      if (selectedFilePaths && selectedFilePaths.length > 0) {
        setFilePaths(selectedFilePaths);
      }
    } catch (error) {
      console.error('Error selecting file:', error);
    }
  };

  const handleFileProcessing = async () => {
    if (filePaths.length > 0 && testType) {
      setIsProcessing(true);
      try {
        const result = await window.electron.processHD(testType, filePaths);

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
              filePaths: filePaths,
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
              filePath: filePaths,
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
            filePath: filePaths,
          },
        });
      } finally {
        setIsProcessing(false);
      }
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center bg-gray-50"
      onClick={() => {
        // Clear any potential leftover tooltips or overlays
        const tooltips = document.querySelectorAll('[title]');
        tooltips.forEach((tooltip) => {
          if (tooltip.title.includes('Download plot for')) {
            tooltip.removeAttribute('title');
          }
        });
      }}
    >
      <div className="w-full max-w-4xl mx-auto bg-white rounded-xl shadow p-8 space-y-8">
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate('/')}
            className="text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors p-2 cursor-pointer rounded-md"
            title="Back to Home"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7 7-7"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 12H5"
              />
            </svg>
          </button>
          <h2 className="text-2xl font-bold text-gray-800">{testData.title}</h2>
          <div className="w-6 h-6"></div>
        </div>
        {/* Description */}
        <div className="bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200 mb-6">
          <p className="text-gray-600">
            <span className="font-bold">Description:</span>{' '}
            {testData.description}
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200 mb-6">
          <p className="text-lg font-semibold text-gray-700 mb-2">
            ✅ You'll get these features for this test:
          </p>
          <ol className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 list-decimal list-inside mt-4">
            {testData.featureList.map((feature, index) => (
              <li
                key={index}
                onClick={() => {
                  setSelectedFeature(testData.featuresData[feature]);
                  setIsModalOpen(true);
                }}
                className="cursor-pointer hover:text-gray-800 hover:bg-gray-100 px-2 py-1 rounded transition-colors duration-150"
              >
                {testData.featuresData[feature].title}
              </li>
            ))}
          </ol>
        </div>

        {/* Call to Action Buttons */}
        <div className="flex flex-col items-center space-y-4">
          <button
            disabled={isProcessing}
            onClick={handleFileUpload}
            className={`px-6 py-3 rounded-lg transition-colors ${
              isProcessing
                ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700 cursor-pointer'
            }`}
          >
            Select Audio Files
          </button>
          {filePaths.length > 0 && (
            <div className="text-center">
              <p className="text-green-600 font-medium">
                Files selected: {filePaths.length}
              </p>
              {filePaths.map((filePath, index) => (
                <p key={index} className="text-sm text-gray-500">
                  {index + 1}. {filePath.split('/').pop()}
                </p>
              ))}
            </div>
          )}
          <button
            disabled={filePaths.length === 0 || isProcessing}
            onClick={handleFileProcessing}
            className={`w-48 px-6 py-2 rounded-xl transition
              ${
                filePaths.length > 0 && !isProcessing
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

      {isModalOpen && selectedFeature && (
        <Modal
          open={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedFeature(null);
          }}
          title={getFeatureTitleWithUnits(selectedFeature)}
        >
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Description</h3>
              <p className="text-gray-600">{selectedFeature.description}</p>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default Dashboard;
