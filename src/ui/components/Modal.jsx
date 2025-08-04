import React from 'react';
import CloseIcon from './CloseIcon.jsx';

function Modal({ open, onClose, title, children }) {
  if (!open) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      onClick={handleBackdropClick}
      className="fixed bg-black/50 min-h-screen z-10 w-screen flex justify-center items-center top-0 left-0 p-4"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-gray-50 rounded-lg p-6 max-w-md w-full relative"
      >
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-start">
            <h2 className="text-xl font-bold text-gray-800">{title}</h2>
            <CloseIcon onClick={onClose} className="-mt-3 -mr-3" />
          </div>
          <div className="text-gray-600">{children}</div>
        </div>
      </div>
    </div>
  );
}

export default Modal;
