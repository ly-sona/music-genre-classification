//components/FileUpload.jsx
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onFileUpload }) => {
    const [file, setFile] = useState(null);
    const [songName, setSongName] = useState("");
    const [artist, setArtist] = useState("");
    const [url, setUrl] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError("");
    };

    const handleUrlChange = (event) => {
        setUrl(event.target.value);
        setFile(null);
        setError("");
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if ((!file && !url) || !songName || !artist) {
            setError("Please provide a file or URL, and fill in all required fields.");
            return;
        }

        const formData = new FormData();
        if (file) formData.append("file", file);
        if (url) formData.append("url", url);
        formData.append("song_name", songName);
        formData.append("artist", artist);

        try {
            const response = await axios.post("http://localhost:5001/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            console.log("Response:", response.data);
            alert("File uploaded successfully!");

            onFileUpload(response.data); 
        } catch (error) {
            console.error("Upload failed:", error);
            setError("Upload failed. Please try again.");
        }
    };

    return (
        <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.inputGroup}>
                <input
                    type="file"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    id="file-upload"
                    accept=".mp3, .wav, .ogg" // Restrict file types
                />
                <label htmlFor="file-upload" style={styles.fileLabel}>
                    Choose File
                </label>
                <input
                    type="text"
                    placeholder="Or enter a URL"
                    value={url}
                    onChange={handleUrlChange}
                    style={styles.urlInput}
                />
            </div>
            <div style={styles.inputGroup}>
                <input
                    type="text"
                    placeholder="Song Name"
                    value={songName}
                    onChange={(e) => setSongName(e.target.value)}
                    required
                    style={styles.textInput}
                />
            </div>
            <div style={styles.inputGroup}>
                <input
                    type="text"
                    placeholder="Artist"
                    value={artist}
                    onChange={(e) => setArtist(e.target.value)}
                    required
                    style={styles.textInput}
                />
            </div>
            {error && <p style={styles.errorText}>{error}</p>}
            <button type="submit" style={styles.submitButton}>
                Submit
            </button>
        </form>
    );
};

const styles = {
    form: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    inputGroup: {
        marginBottom: '15px',
        width: '100%',
        maxWidth: '400px',
    },
    fileLabel: {
        cursor: 'pointer',
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: '#fff',
        borderRadius: '4px',
        display: 'inline-block',
    },
    urlInput: {
        marginTop: '10px',
        width: '100%',
        padding: '8px',
        borderRadius: '4px',
        border: '1px solid #ccc',
    },
    textInput: {
        width: '100%',
        padding: '8px',
        borderRadius: '4px',
        border: '1px solid #ccc',
    },
    submitButton: {
        padding: '10px 20px',
        backgroundColor: '#28a745',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    },
    errorText: {
        color: 'red',
        marginBottom: '10px',
    },
};

export default FileUpload;
