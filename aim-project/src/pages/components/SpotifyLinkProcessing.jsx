//src/pages/components/SpotifyLinkProcessing.jsx

//CHALLENGE: Implement a Spotify Link to mp3 or wav file component! Try to populate the name and artist fields automatically if possible.
// You'll need to understand the Flask code as well. Make sure to implement validifcation and error checking!

//mock file
// components/SpotifyLinktoFile.jsx
// components/SpotifyLinkProcessing.jsx
import React from 'react';

const SpotifyLinkProcessing = ({ onFileUpload }) => {
    const handleMockSubmit = () => {
        // Indicate the upload has started
        onFileUpload(null);
        // Simulate a delay for processing
        setTimeout(() => {
            // Mock data to simulate a successful upload
            const mockData = {
                song_name: 'Mock Song from Spotify',
                artist: 'Mock Artist',
                cover_image_url: 'https://via.placeholder.com/300?text=Spotify+Mock+Image',
                genres: [{ name: 'Pop', confidence: 90 }],
                filename: 'mock_spotify_song.mp3'
            };
            onFileUpload(mockData);
        }, 2000); // Simulate a 2-second delay
    };

    return (
        <div className="flex flex-col items-center space-y-4">
            <p className="text-purple-400">This is a mock Spotify link upload component.</p>
            <button
                onClick={handleMockSubmit}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 text-sm md:text-base"
            >
                Submit Mock Spotify Link
            </button>
        </div>
    );
};

export default SpotifyLinkProcessing;