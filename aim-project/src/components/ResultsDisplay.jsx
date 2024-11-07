//components/ResultsDisplay.jsx
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

    const audioSrc = filename ? `http://localhost:5001/uploads/${filename}` : null;

    return (
        <div style={styles.container}>
            {/* Song Metadata */}
            <div style={styles.metadata}>
                <h2 style={styles.songName}>{songName}</h2>
                <p style={styles.artist}>by {artist}</p>
            </div>

            {/* Cover Image */}
            <div style={styles.coverImageContainer}>
                <img 
                    src={coverImageUrl} 
                    alt={`${songName} cover`} 
                    style={styles.coverImage} 
                />
            </div>

            {/* Genre List */}
            {genres.length > 0 && (
                <div style={styles.genreList}>
                    <h3>Predicted Genres</h3>
                    <ul style={styles.genreItems}>
                        {genres.map((genre, index) => (
                            <li key={index} style={styles.genreItem}>
                                {genre.name} {genre.confidence ? `(${genre.confidence}%)` : ""}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Open Button */}
            {filename && (
                <div style={styles.openButtonContainer}>
                    <button onClick={handleOpen} style={styles.openButton}>
                        {isOpen ? 'Close' : 'Open'}
                    </button>
                </div>
            )}

            {/* Audio Player and Download Link */}
            {isOpen && audioSrc && (
                <div style={styles.audioSection}>
                    <audio controls>
                        <source src={audioSrc} type="audio/mpeg" />
                        Your browser does not support the audio element.
                    </audio>
                    <a href={audioSrc} download style={styles.downloadLink}>
                        Download File
                    </a>
                </div>
            )}
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '400px',
        margin: '20px auto',
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#f9f9f9',
    },
    metadata: {
        marginBottom: '20px',
    },
    songName: {
        fontSize: '24px',
        fontWeight: 'bold',
        margin: '0',
    },
    artist: {
        fontSize: '18px',
        color: '#555',
        margin: '5px 0',
    },
    coverImageContainer: {
        width: '100%',
        paddingTop: '100%', 
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '8px',
        marginBottom: '20px',
    },
    coverImage: {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
    },
    genreList: {
        textAlign: 'left',
    },
    genreItems: {
        listStyleType: 'none',
        padding: 0,
        margin: 0,
    },
    genreItem: {
        padding: '5px 0',
        fontSize: '16px',
    },
    openButtonContainer: {
        marginTop: '20px',
    },
    openButton: {
        padding: '10px 20px',
        backgroundColor: '#17a2b8',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
    },
    audioSection: {
        marginTop: '20px',
    },
    downloadLink: {
        display: 'block',
        marginTop: '10px',
        color: '#007bff',
        textDecoration: 'none',
    },
};

export default ResultsDisplay;
