// src/components/Account/SourceCard.jsx
import React from 'react';

const SourceCard = ({ source }) => {
  return (
    <div className="flex items-center justify-between border border-gray-200 rounded-lg p-4">
      <div>
        <h3 className="font-semibold text-gray-800">{source.name}</h3>
        {/* Adicionei a verificação de 'url' para caso não exista */}
        {source.url && <p className="text-sm text-gray-500">{source.url}</p>}
      </div>
      <button className="text-gray-400 hover:text-red-500">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
};

export default SourceCard;