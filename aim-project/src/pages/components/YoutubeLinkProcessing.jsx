// src/pages/components/YoutubeLinkProcessing.jsx

import React, { useState } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

const YoutubeLinkProcessing = ({ onFileUpload }) => {
    const [youtubeURL, setYoutubeURL] = useState("");
    const [artist, setArtist] = useState("");
    const [songTitle, setSongTitle] = useState("");
    const [error, setError] = useState("");
    const [isValid, setIsValid] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Function to validate YouTube URL
    const validateYouTubeURL = (url) => {
        const regex = /^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$/;
        return regex.test(url);
    };

    const handleURLChange = (e) => {
        const url = e.target.value;
        setYoutubeURL(url);
        if (validateYouTubeURL(url)) {
            setIsValid(artist.trim() !== "" && songTitle.trim() !== "");
            setError("");
        } else {
            setIsValid(false);
            setError("Please enter a valid YouTube URL.");
        }
    };

    const handleArtistChange = (e) => {
        const artistInput = e.target.value;
        setArtist(artistInput);
        if (artistInput.trim() === "") {
            setError("Artist name is required.");
            setIsValid(false);
        } else if (validateYouTubeURL(youtubeURL) && songTitle.trim() !== "") {
            setError("");
            setIsValid(true);
        }
    };

    const handleSongTitleChange = (e) => {
        const titleInput = e.target.value;
        setSongTitle(titleInput);
        if (titleInput.trim() === "") {
            setError("Song title is required.");
            setIsValid(false);
        } else if (validateYouTubeURL(youtubeURL) && artist.trim() !== "") {
            setError("");
            setIsValid(true);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!isValid) {
            setError("Please enter a valid YouTube URL, Artist, and Song Title.");
            return;
        }

        try {
            setIsSubmitting(true);
            setError("");
            onFileUpload(null); // Indicate upload has started

            // Create FormData and append the URL, artist, and song title
            const formData = new FormData();
            formData.append('url', youtubeURL);
            formData.append('artist', artist);
            formData.append('song_name', songTitle);

            const response = await axios.post("http://127.0.0.1:5001/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });

            console.log("Response:", response.data);
            onFileUpload(response.data);
        } catch (err) {
            console.error("Error processing YouTube URL:", err.response?.data?.error || err.message);
            setError(err.response?.data?.error || "Failed to process YouTube URL. Please try again.");
            onFileUpload(null); // Reset upload state on error
        } finally {
            setIsSubmitting(false);
        }
    };    

    return (
        <form onSubmit={handleSubmit} className="flex flex-col items-center space-y-6 w-full">
            {/* YouTube URL Input */}
            <div className="w-full">
                <input
                    type="url"
                    placeholder="Enter YouTube URL"
                    value={youtubeURL}
                    onChange={handleURLChange}
                    required
                    className="w-full px-4 py-2 bg-slate-800 text-white border border-purple-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-600 text-sm md:text-base"
                />
            </div>

            {/* Artist Input */}
            <div className="w-full">
                <input
                    type="text"
                    placeholder="Artist Name"
                    value={artist}
                    onChange={handleArtistChange}
                    required
                    className="w-full px-4 py-2 bg-slate-800 text-white border border-purple-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-600 text-sm md:text-base"
                />
            </div>

            {/* Song Title Input */}
            <div className="w-full">
                <input
                    type="text"
                    placeholder="Song Title"
                    value={songTitle}
                    onChange={handleSongTitleChange}
                    required
                    className="w-full px-4 py-2 bg-slate-800 text-white border border-purple-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-600 text-sm md:text-base"
                />
            </div>

            {/* Error Message */}
            {error && <p className="text-red-500 text-center w-full text-sm md:text-base">{error}</p>}

            {/* Buttons Row */}
            <div className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                {/* Submit Button */}
                <button
                    type="submit"
                    className={`w-full sm:w-1/2 px-5 py-2.5 bg-gradient-to-r from-pink-500 to-pink-700 text-white rounded-xl shadow-lg hover:from-pink-600 hover:to-pink-800 transition duration-300 text-sm md:text-base ${
                        !isValid || isSubmitting ? "opacity-50 cursor-not-allowed" : ""
                    }`}
                    disabled={!isValid || isSubmitting}
                >
                    {isSubmitting ? "Processing..." : "Submit"}
                </button>
            </div>
        </form>
    );
}

YoutubeLinkProcessing.propTypes = {
    onFileUpload: PropTypes.func.isRequired,
};

export default YoutubeLinkProcessing