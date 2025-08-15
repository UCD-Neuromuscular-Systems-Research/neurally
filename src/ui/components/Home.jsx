import React from 'react';
import { Link, useNavigate } from 'react-router';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">
        Clinical speech assessment platform
      </h1>

      <p className="text-base text-gray-600 mb-8 text-center">
        Analyze speech features based on any of the test types below
      </p>

      <div className="flex flex-col space-y-4 mb-6 w-full max-w-xs">
        <Link
          to="tests/SV"
          className="bg-blue-500 text-white hover:bg-blue-700 px-6 py-2 rounded-xl transition cursor-pointer block text-center"
        >
          Sustained Vowel (SV)
        </Link>
        <Link
          to="tests/SR"
          className="bg-green-500 text-white hover:bg-green-700 px-6 py-2 rounded-xl transition cursor-pointer block text-center"
        >
          Syllable Repetition (SR)
        </Link>
        <Link
          to="tests/PR"
          className="bg-purple-500 text-white hover:bg-purple-700 px-6 py-2 rounded-xl transition cursor-pointer block text-center"
        >
          Paragraph Reading (PR)
        </Link>
      </div>

      <button
        onClick={() => navigate('/tutorial')}
        className="flex items-center space-x-1 text-sm text-zinc-500 hover:underline cursor-pointer"
      >
        <span>Tutorial of the app</span>
        <span className="text-xs cursor-pointer">↗</span>
      </button>
    </div>
  );
}

export default Home;
