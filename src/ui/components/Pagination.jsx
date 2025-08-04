import React from 'react';

function Pagination({ 
  currentPage, 
  totalPages, 
  onPageChange, 
  showPagination = true 
}) {
  if (!showPagination) return null;

  return (
    <div className="flex justify-center items-center space-x-4 mt-6 h-12">
      <button
        onClick={() => onPageChange(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
        title={
          currentPage === 1
            ? "You're on the first page"
            : 'Previous page'
        }
        className={`px-4 py-2 rounded-lg transition-colors ${
          currentPage === 1
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-gray-600 hover:text-gray-800 cursor-pointer'
        }`}
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </button>

      {/* Page Number Buttons */}
      <div className="flex space-x-2">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map(
          (page) => (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`px-3 py-2 rounded-lg transition-colors cursor-pointer ${
                currentPage === page
                  ? 'bg-gray-200 text-gray-800 px-2 py-1'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              {page}
            </button>
          )
        )}
      </div>

      <button
        onClick={() =>
          onPageChange(Math.min(totalPages, currentPage + 1))
        }
        disabled={currentPage === totalPages}
        title={
          currentPage === totalPages
            ? "You're on the last page"
            : 'Next page'
        }
        className={`px-4 py-2 rounded-lg transition-colors ${
          currentPage === totalPages
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-gray-600 hover:text-gray-800 cursor-pointer'
        }`}
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>
    </div>
  );
}

export default Pagination; 