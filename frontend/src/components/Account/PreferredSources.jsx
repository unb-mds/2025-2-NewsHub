// src/components/Account/PreferredSources.jsx
import React from 'react';
import SourceCard from './SourceCard';

const PreferredSources = ({ sources }) => {
  return (
    <div className="bg-white p-8 rounded-lg mt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Preferred news sources</h2>
        <button className="bg-black text-white font-semibold px-6 py-2 rounded-md hover:bg-gray-800">
          Add Source
        </button>
      </div>
      <div>
        <p className="text-sm font-medium text-gray-600 mb-4">Your Sources</p>
        <div className="space-y-4">
          {sources.map(source => <SourceCard key={source.id} source={source} />)}
        </div>
      </div>
    </div>
  );
};

export default PreferredSources;