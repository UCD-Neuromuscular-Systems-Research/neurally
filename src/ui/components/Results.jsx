import React from 'react';
import image from './sample_SV.png';

function Results() {
  return (
    <div className="w-full p-6 space-y-8">
      {/* Heading */}
      <h2 className="text-2xl font-bold text-center text-gray-800">
        Your file is processed and here&apos;s your analysis.
      </h2>

      {/* Two-column layout */}
      <div className="flex flex-col md:flex-row md:space-x-8 space-y-6 md:space-y-0">
        {/* Left: Feature Table */}
        <div className="flex-1 bg-white p-4 rounded-md shadow-sm border border-gray-200">
          <h3 className="font-semibold text-lg mb-4 text-gray-700">
            Extracted Features
          </h3>
          <table className="table-auto w-full border-collapse border border-gray-300 text-sm">
            <tbody>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">
                  Fundamental frequency (F0)
                </td>
                <td className="border px-3 py-2">145.2 Hz</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">
                  Standard deviation of F0
                </td>
                <td className="border px-3 py-2">12.4 Hz</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">HNR</td>
                <td className="border px-3 py-2">21.7 dB</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">Jitter</td>
                <td className="border px-3 py-2">0.45%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">
                  RAP of Jitter
                </td>
                <td className="border px-3 py-2">0.19%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">PPQ5</td>
                <td className="border px-3 py-2">0.24%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">DDP</td>
                <td className="border px-3 py-2">0.56%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">Shimmer</td>
                <td className="border px-3 py-2">0.32%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">APQ3</td>
                <td className="border px-3 py-2">0.17%</td>
              </tr>
              <tr className="text-center">
                <td className="border px-3 py-2 font-semibold">APQ5</td>
                <td className="border px-3 py-2">0.22%</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Right: PNG Plot */}
        <div className="flex-1 flex items-center justify-center bg-white p-4 rounded-md shadow-sm border border-gray-200">
          <img
            src={image}
            alt="Feature Analysis Plot"
            className="max-w-full max-h-[400px] object-contain"
          />
        </div>
      </div>
      <button
        className="block mx-auto w-1/2 max-w-xs bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition cursor-pointer"
        onClick={() => {
          // Replace this with your actual download logic
          console.log('Download triggered');
        }}
      >
        Download Results
      </button>
    </div>
  );
}

export default Results;
