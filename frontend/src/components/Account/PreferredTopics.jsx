// src/components/Account/PreferredTopics.jsx
import React from 'react';
import TopicTag from './TopicTag';

const PreferredTopics = ({ topics }) => {
  return (
    <div className="bg-white p-8 rounded-lg mt-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Preferred news topics</h2>
      <div className="flex items-center gap-4 mb-6">
        <input
          type="text"
          placeholder="Enter a new topic..."
          className="flex-grow border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-black"
        />
        <button className="bg-black text-white font-semibold px-6 py-2 rounded-md hover:bg-gray-800">
          Add Topic
        </button>
      </div>
      <div>
        <p className="text-sm font-medium text-gray-600 mb-4">Your topics</p>
        <div className="flex flex-wrap gap-2">
          {topics.map(topic => <TopicTag key={topic.id} topic={topic} />)}
        </div>
      </div>
    </div>
  );
};

export default PreferredTopics;