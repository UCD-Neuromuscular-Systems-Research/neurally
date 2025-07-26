import React, { useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router';

function Dashboard() {
  const { testType } = useParams();
  const navigate = useNavigate();
  const [uploadedFile, setUploadedFile] = useState(null);
  const inputRef = useRef();

  const handleFile = (file) => {
    if (file) {
      setUploadedFile(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    handleFile(file);
  };

  return (
    <div className="flex flex-col h-screen w-full p-6 space-y-8 bg-gray-50">
      {/* Test heading */}
      <h2 className="text-2xl font-bold text-center text-gray-800">
        Sustained Vowel Test
      </h2>

      {/* Two blocks */}
      <div className="flex flex-col md:flex-row md:space-x-8 space-y-6 md:space-y-0">
        {/* Description */}
        <div className="flex-1 bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200">
          <p className="text-gray-600">
            <span className="font-bold">Description:</span> The act of holding a
            vowel sound (like "ah" or "ee") for an extended period, usually at a
            consistent pitch and loudness. This technique is often used in
            clinical settings and research to assess voice quality and identify
            potential vocal issues.
          </p>
        </div>

        {/* Features */}
        <div className="flex-1 bg-gray-50 p-4 rounded-md shadow-sm">
          <h3 className="font-semibold mb-2 text-gray-700">
            You'll get all these features:
          </h3>

          <table className="table-auto w-full border-collapse border border-gray-300">
            <tbody>
              <tr className="text-center">
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  Fundamental frequency (F0)
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  Standard deviation of F0
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  HNR
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  Jitter
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  RAP of Jitter
                </td>
              </tr>
              <tr className="text-center">
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  PPQ5
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  DDP
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  Shimmer
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  APQ3
                </td>
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  APQ5
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Drag & Drop */}
      <div
        className="flex-grow border-4 border-dashed border-gray-400 rounded-lg flex items-center justify-center text-gray-500 text-lg cursor-pointer hover:border-gray-600 transition mb-4"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={handleClick}
      >
        {uploadedFile
          ? `Successfully uploaded: ${uploadedFile.name}`
          : 'Drag and drop your file here or click to browse'}
        <input
          type="file"
          ref={inputRef}
          className="hidden"
          onChange={handleChange}
        />
      </div>

      {/* Proceed Button */}
      <button
        disabled={!uploadedFile}
        onClick={() => navigate('/results')}
        className={`block mx-auto w-1/2 max-w-xs px-6 py-2 rounded-xl transition
          ${
            uploadedFile
              ? 'bg-green-600 text-white hover:bg-green-700 cursor-pointer'
              : 'bg-gray-300 text-gray-600 cursor-not-allowed'
          }`}
      >
        Proceed
      </button>
    </div>
  );
}

export default Dashboard;
