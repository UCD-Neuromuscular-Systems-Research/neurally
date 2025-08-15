import React from 'react';
import { useNavigate } from 'react-router';

function Tutorial() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors p-2 rounded-md cursor-pointer"
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
          <h1 className="text-3xl font-bold text-gray-800">
            Tutorial of Neurally
          </h1>
          <div className="w-6 h-6"></div>
        </div>

        {/* Introduction */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Welcome to Neurally
          </h2>
          <p className="text-gray-600 leading-relaxed">
            Neurally is a clinical speech assessment platform designed to
            analyze speech features for individuals with Huntington's disease.
            This tutorial will guide you through the simple process of using the
            application.
          </p>
        </div>

        {/* Step-by-step guide */}
        <div className="space-y-8">
          {/* Step 1 */}
          <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              Step 1: Choose Your Speech Task
            </h3>
            <p className="text-gray-600 mb-4">
              On the home screen, you'll see three different speech test types.
              Each test is designed to assess different aspects of speech:
            </p>
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <div className="bg-blue-100 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">
                  Sustained Vowel (SV)
                </h4>
                <p className="text-sm text-blue-700">
                  Hold a vowel sound (like "ah" or "ee") for an extended period.
                  This test measures vocal endurance and quality.
                </p>
              </div>
              <div className="bg-green-100 p-4 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-2">
                  Syllable Repetition (SR)
                </h4>
                <p className="text-sm text-green-700">
                  Rapidly repeat syllables (like "pa-ta-ka") in a consistent
                  rhythm. This assesses motor speech planning and coordination.
                </p>
              </div>
              <div className="bg-purple-100 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800 mb-2">
                  Paragraph Reading (PR)
                </h4>
                <p className="text-sm text-purple-700">
                  Read a standardized paragraph aloud. This evaluates natural
                  speech patterns and communication effectiveness.
                </p>
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-400">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              Step 2: Upload Your Audio Files
            </h3>
            <p className="text-gray-600 mb-4">
              After selecting a test type, you'll see a description of the test
              and the features that will be analyzed.
            </p>
            <div className="bg-white p-4 rounded-lg border mb-4">
              <h4 className="font-semibold text-gray-800 mb-2">
                File Requirements:
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Format: WAV files only</li>
                <li>• You can upload single or multiple files</li>
                <li>• Choose descriptive file names for easy identification</li>
                <li>
                  • Ensure recordings are clear and free from background noise
                </li>
              </ul>
            </div>
          </div>

          {/* Step 3 */}
          <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-400">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              Step 3: Review and Process
            </h3>
            <p className="text-gray-600 mb-4">
              Once your files are uploaded, you can:
            </p>
            <ul className="text-gray-600 space-y-2 mb-4">
              <li>• Review the list of uploaded files</li>
              <li>• See the total count of files to be processed</li>
              <li>• Click "Proceed" to start the analysis</li>
              <li>• Change your file selection before processing if needed</li>
            </ul>
            <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <p className="text-sm text-yellow-800">
                <strong>Note:</strong> Once you click "Proceed," the file
                selection cannot be modified. The processing will begin
                immediately.
              </p>
            </div>
          </div>

          {/* Step 4 */}
          <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-400">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              Step 4: View Your Results
            </h3>
            <p className="text-gray-600 mb-4">
              After processing, your results will be displayed in an organized
              table format:
            </p>
            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div className="bg-white p-4 rounded-lg border">
                <h4 className="font-semibold text-gray-800 mb-2">
                  Results Table
                </h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Each column represents a file</li>
                  <li>• Each row shows a specific speech feature</li>
                  <li>• Values are automatically calculated and displayed</li>
                </ul>
              </div>
              <div className="bg-white p-4 rounded-lg border">
                <h4 className="font-semibold text-gray-800 mb-2">
                  Visualization
                </h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• View voiced/unvoiced detection plots</li>
                  <li>• Download plots as PNG images</li>
                  <li>• Export feature data as CSV files</li>
                </ul>
              </div>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-blue-800">
                <strong>Pagination:</strong> If you have more than 10 files,
                results will be paginated for easier viewing.
              </p>
            </div>
          </div>

          {/* Step 5 */}
          <div className="bg-red-50 p-6 rounded-lg border-l-4 border-red-400">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              Step 5: Download and Continue
            </h3>
            <p className="text-gray-600 mb-4">
              Once you've reviewed your results, you can:
            </p>
            <ul className="text-gray-600 space-y-2 mb-4">
              <li>• Download individual feature data as CSV files</li>
              <li>• Save plot visualizations as PNG images</li>
              <li>
                • Click "Process More Files" to analyze additional recordings
              </li>
            </ul>
            <div className="bg-red-100 p-4 rounded-lg border border-red-200">
              <p className="text-sm text-red-800">
                <strong>Important:</strong> Clicking "Process More Files" will
                delete all previously processed data. Make sure to download any
                results you want to keep before proceeding.
              </p>
            </div>
          </div>
        </div>

        {/* Get Started Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-8 py-3 rounded-xl hover:bg-blue-700 transition-colors font-semibold cursor-pointer"
          >
            Get Started with Neurally
          </button>
        </div>
      </div>
    </div>
  );
}

export default Tutorial;
