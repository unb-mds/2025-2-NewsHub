// src/components/Account/TopicTag.jsx
import React from 'react';

const TopicTag = ({ topic }) => {
  return (
    <div className="flex items-center bg-gray-100 rounded-full px-3 py-1 text-sm font-medium text-gray-700">
      <span>{topic.name}</span>
      <button className="ml-2 text-gray-500 hover:text-gray-800 focus:outline-none">
        &times;
      </button>
    </div>
  );
};

export default TopicTag;