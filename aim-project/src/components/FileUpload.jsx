import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [songName, setSongName] = useState("");
    const [artist, setArtist] = useState("");
    const [url, setUrl] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError(""); // Clear any previous errors
    };

    const handleUrlChange = (event) => {
        setUrl(event.target.value);
        setFile(null); // Clear file input if URL is being used
        setError("");
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Validation: ensure either file or URL is provided and songName & artist are filled
        if ((!file && !url) || !songName || !artist) {
            setError("Please provide a file or URL, and fill in all required fields.");
            return;
        }

        // Prepare form data
        const formData = new FormData();
        if (file) formData.append("file", file);
        if (url) formData.append("url", url);
        formData.append("song_name", songName);
        formData.append("artist", artist);

        try {
            // Axios POST request to Flask backend
            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            console.log("Response:", response.data);
            alert("File uploaded successfully!");
        } catch (error) {
            console.error("Upload failed:", error);
            setError("Upload failed. Please try again.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input
                    type="file"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    id="file-upload"
                />
                <label htmlFor="file-upload" style={{ cursor: 'pointer', padding: '8px', backgroundColor: '#007bff', color: '#fff', borderRadius: '4px' }}>
                    Choose File
                </label>
                <input
                    type="text"
                    placeholder="Or enter a URL"
                    value={url}
                    onChange={handleUrlChange}
                    style={{ display: 'block', marginTop: '10px' }}
                />
            </div>
            <div style={{ marginTop: '10px' }}>
                <input
                    type="text"
                    placeholder="Song Name"
                    value={songName}
                    onChange={(e) => setSongName(e.target.value)}
                    required
                />
            </div>
            <div style={{ marginTop: '10px' }}>
                <input
                    type="text"
                    placeholder="Artist"
                    value={artist}
                    onChange={(e) => setArtist(e.target.value)}
                    required
                />
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button type="submit" style={{ marginTop: '15px', padding: '8px', backgroundColor: '#007bff', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}>
                Submit
            </button>
        </form>
    );
};

export default FileUpload;