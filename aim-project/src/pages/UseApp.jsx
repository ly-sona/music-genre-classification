// src/pages/UseApp.jsx
import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import Loading from './components/Loading';
import './UseApp.css'
// Removed Navbar import from here

function UseApp() {
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
        {displayState === 'upload' && (
          <div className='container'>
            <section id="upload" className="upload-section">
                <h2>Upload Your File</h2>
                <FileUpload onFileUpload={handleFileUpload} />
            </section>
          </div>
        )}

        {displayState === 'uploading' && (
          <div className='container'>
            <div className="uploading-section">
                <Loading />
                <p>Uploading...</p>
            </div>
          </div>
        )}

        {displayState === 'uploaded' && (
          <div className='container'>
            <div className="uploaded-section">
                <p>Uploaded Successfully!</p>
            </div>
          </div>
        )}

        {displayState === 'loading' && (
          <div className='container'>
            <div className="loading-section">
                <Loading />
            </div>
          </div>
        )}

        {displayState === 'results' && uploadedFile && (
          <div className='container'>
            <div className="results-section">
                <ResultsDisplay 
                songName={uploadedFile.song_name} 
                artist={uploadedFile.artist} 
                coverImageUrl={uploadedFile.cover_image_url} 
                genres={uploadedFile.genres} 
                filename={uploadedFile.filename}
                /> 
            </div>
          </div>
        )}
    </>
  );
}

export default UseApp;
