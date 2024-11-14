// components/ResultsDisplay.jsx
import React, { useState } from 'react';

const DEFAULT_COVER_IMAGE = "https://via.placeholder.com/300?text=No+Cover+Image";

const ResultsDisplay = ({
    songName = "Unknown Song",
    artist = "Unknown Artist",
    coverImageUrl = DEFAULT_COVER_IMAGE,
    genres = [],
    filename = null 
}) => {
    const [isOpen, setIsOpen] = useState(false);

    const handleOpen = () => {
        setIsOpen(!isOpen);
    };

    const audioSrc = filename ? `http://127.0.0.1:5001/uploads/${filename}` : null;

    return (
        <div className="max-w-md mx-auto p-6 bg-slate-800 text-white rounded-lg shadow-md">
            {/* Song Metadata */}
            <div className="text-center mb-4">
                <h2 className="text-2xl font-bold">{songName}</h2>
                <p className="text-purple-400">by {artist}</p>
            </div>

            {/* Cover Image */}
            <div className="w-full h-64 bg-gray-700 rounded-lg overflow-hidden mb-4">
                <img 
                    src={coverImageUrl} 
                    alt={`${songName} cover`} 
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Genre List */}
            {genres.length > 0 && (
                <div className="mb-4">
                    <h3 className="text-xl font-semibold mb-2 text-purple-400">Predicted Genres</h3>
                    <ul className="list-disc list-inside text-purple-200">
                        {genres.map((genre, index) => (
                            <li key={index}>
                                {genre.name} {genre.confidence ? `(${genre.confidence}%)` : ""}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Open Button */}
            {filename && (
                <div className="text-center mb-4">
                    <button 
                        onClick={handleOpen} 
                        className="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 text-sm md:text-base"
                    >
                        {isOpen ? 'Close' : 'Open'}
                    </button>
                </div>
            )}

            {/* Audio Player and Download Link */}
            {isOpen && audioSrc && (
                <div className="flex flex-col items-center space-y-2">
                    <audio controls className="w-full">
                        <source src={audioSrc} type="audio/mpeg" />
                        Your browser does not support the audio element.
                    </audio>
                    <a 
                        href={audioSrc} 
                        download 
                        className="text-purple-400 hover:underline"
                    >
                        Download File
                    </a>
                </div>
            )}
        </div>
    );
}

export default ResultsDisplay;