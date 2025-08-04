import React from 'react';
import { Link } from 'react-router';

function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">
        Clinical speech assessment platform
      </h1>

      <p className="text-base text-gray-600 mb-8 text-center">
        Analyze speech features based on any of the test types below
      </p>

      <div className="flex flex-col space-y-4 mb-6 w-full max-w-xs">
        <button className="bg-blue-500 text-white hover:bg-blue-700  px-6 py-2 rounded-xl transition cursor-pointer">
          <Link to="tests/SV">Sustained Vowel (SV)</Link>
        </button>
        <button className="bg-green-500 text-white px-6 py-2 rounded-xl hover:bg-green-700 transition cursor-pointer">
          Syllable Repetition (SR)
        </button>
        <button className="bg-purple-500 text-white px-6 py-2 rounded-xl hover:bg-purple-700 transition cursor-pointer">
          Paragraph reading (PR)
        </button>
      </div>

      <button className="flex items-center space-x-1 text-sm text-zinc-500 hover:underline cursor-pointer">
        <span>Tutorial of the app</span>
        <span className="text-xs cursor-pointer">↗</span>
      </button>
    </div>
  );
}

export default Home;
