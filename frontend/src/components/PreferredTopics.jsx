// src/components/PreferredTopics.jsx
import React from "react";

const PreferredTopics = ({
  topics,
  newTopic,
  onNewTopicChange,
  onAddTopic,
  onDeleteTopic, // Prop para a função de deletar
}) => {
  return (
    <div className="mt-6 rounded-lg">
      <h2 className="text-xl font-medium text-gray-900 font-montserrat">
        Preferred news topics
      </h2>
      <hr className="my-4 border-t-2 border-black mb-6" />

      {/* Formulário para adicionar tópico */}
      <div className="flex items-end gap-4">
        <input
          type="text"
          value={newTopic}
          onChange={onNewTopicChange} // Usa a função recebida via props
          placeholder="enter a new topic..."
          className="h-11 flex-grow border border-gray-800 rounded px-4 focus:outline-none focus:ring-2 focus:ring-black text-xs font-montserrat"
        />
        <button
          onClick={onAddTopic} // Usa a função recebida via props
          className="h-11 flex items-center bg-black text-white text-xs font-bold px-4 rounded hover:bg-gray-800 font-montserrat"
        >
          Add Topic
        </button>
      </div>

      {/* Lista de tópicos existentes */}
      <div>
        <p className="mt-8 mb-3 text-base font-medium text-gray-900 font-montserrat">
          Your topics
        </p>
        <div className="flex flex-wrap gap-2">
          {topics.map((topic) => (
            <div
              key={topic.id}
              className="flex items-center gap-2 bg-white text-gray-900 text-xs font-medium border border-black shadow-lg pl-3 pr-2 py-1 rounded-full font-montserrat"
            >
              <span>{topic.name}</span>
              <button
                onClick={() => onDeleteTopic(topic.id)} // Chama a função de deletar com o id do tópico
                className="text-red-500 hover:text-red-700 rounded-full hover:bg-gray-100 p-0.2"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PreferredTopics;
