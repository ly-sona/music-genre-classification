// components/ResultsDisplay.jsx
import React from 'react';

// Default cover image URL (you can replace this with your own image)
const DEFAULT_COVER_IMAGE = "https://via.placeholder.com/300?text=No+Cover+Image";

const ResultsDisplay = ({
    songName = "Unknown Song",
    artist = "Unknown Artist",
    coverImageUrl = DEFAULT_COVER_IMAGE,
    genres = []
}) => {
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
        </div>
    );
};

// Inline styles for the component
const styles = {
    container: {
        maxWidth: '400px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
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
        paddingTop: '100%', // Creates a square aspect ratio
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
};

export default ResultsDisplay;
