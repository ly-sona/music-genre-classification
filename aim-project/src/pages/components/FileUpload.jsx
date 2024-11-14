// components/FileUpload.jsx
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onFileUpload, onBack }) => {
    const [file, setFile] = useState(null);
    const [songName, setSongName] = useState("");
    const [artist, setArtist] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError("");
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!file || !songName || !artist) {
            setError("Please provide a file and fill in all required fields.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("song_name", songName);
        formData.append("artist", artist);

        try {
            onFileUpload(null); // Indicate upload has started
            const response = await axios.post("http://127.0.0.1:5001/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                },
            });
            console.log("Response:", response.data);
            onFileUpload(response.data);
        } catch (error) {
            console.error("Upload failed:", error);
            setError("Upload failed. Please try again.");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col items-center space-y-6 w-full">
            {/* Upload Button */}
            <div className="w-full">
                <input
                    type="file"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                    accept=".mp3, .wav, .ogg"
                />
                <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex items-center justify-center w-full px-5 py-2.5 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 text-sm md:text-base"
                >
                    {file ? file.name : "Upload Music File"}
                </label>
            </div>

            {/* Inputs Row */}
            <div className="flex flex-col sm:flex-row gap-4 w-full">
                {/* Song Name Input */}
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Song Name"
                        value={songName}
                        onChange={(e) => setSongName(e.target.value)}
                        required
                        className="w-full px-4 py-2 bg-slate-800 text-white border border-purple-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-600 text-sm md:text-base"
                    />
                </div>

                {/* Artist Input */}
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Artist"
                        value={artist}
                        onChange={(e) => setArtist(e.target.value)}
                        required
                        className="w-full px-4 py-2 bg-slate-800 text-white border border-purple-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-600 text-sm md:text-base"
                    />
                </div>
            </div>

            {/* Error Message */}
            {error && <p className="text-red-500 text-center w-full text-sm md:text-base">{error}</p>}

            {/* Buttons Row */}
            <div className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                {/* Submit Button */}
                <button
                    type="submit"
                    className={`w-full sm:w-1/2 px-5 py-2.5 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 text-sm md:text-base ${
                        (!file || !songName || !artist) && "opacity-50 cursor-not-allowed"
                    }`}
                    disabled={!file || !songName || !artist}
                >
                    Submit
                </button>

                {/* Back Button */}
                <button
                    type="button"
                    onClick={onBack}
                    className="w-full sm:w-1/2 px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-700 text-white rounded-xl shadow-lg hover:from-red-600 hover:to-red-800 transition duration-300 text-sm md:text-base"
                >
                    Back
                </button>
            </div>
        </form>
    );
};

export default FileUpload;