// App.js
import { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import Loading from './components/Loading';

function App() {
  const [displayState, setDisplayState] = useState('upload');
  const [uploadedFile, setUploadedFile] = useState(null); 

  const handleFileUpload = (fileData) => {
    setUploadedFile(fileData);
    setDisplayState('uploaded'); // Change to 'uploaded' state
    
    // After displaying 'uploaded', transition to 'loading' and 'results'
    setTimeout(() => {
      setDisplayState('loading'); 
      setTimeout(() => {
        setDisplayState('results'); 
      }, 2000); // Adjust time as needed
    }, 2000); // Time to display 'Uploaded' status
  };

  return (
    <>
      <div className="navbar">
        <div className="navbar-name">
          <h1>Genre Classification</h1>
        </div>
        <ul>
          <li>Use our App</li>
          <li>About the model</li>
          <li>About us</li>
        </ul>
      </div>

      {displayState === 'upload' && (
        <section id="upload" className="upload-section">
          <h2>Upload Your File</h2>
          <FileUpload onFileUpload={handleFileUpload} />
        </section>
      )}

      {displayState === 'uploading' && (
        <div className="uploading-section">
          <Loading />
          <p>Uploading...</p>
        </div>
      )}

      {displayState === 'uploaded' && (
        <div className="uploaded-section">
          <p>Uploaded Successfully!</p>
        </div>
      )}

      {displayState === 'loading' && (
        <div className="loading-section">
          <Loading />
        </div>
      )}

      {displayState === 'results' && uploadedFile && (
        <div className="results-section">
          <ResultsDisplay 
            songName={uploadedFile.song_name} 
            artist={uploadedFile.artist} 
            coverImageUrl={uploadedFile.cover_image_url} 
            genres={uploadedFile.genres} 
            filename={uploadedFile.filename}
          /> 
        </div>
      )}
    </>
  );
}

export default App;
