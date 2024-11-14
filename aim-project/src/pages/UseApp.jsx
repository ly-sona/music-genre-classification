// src/pages/UseApp.jsx

import { useState } from 'react';
import axios from 'axios'; // Import axios
import FileUpload from './components/FileUpload';
import SpotifyLinkProcessing from './components/SpotifyLinkProcessing';
import YoutubeLinkProcessing from './components/YoutubeLinkProcessing';
import ResultsDisplay from './components/ResultsDisplay';
import Loading from './components/Loading';

function UseApp() {
  const [displayState, setDisplayState] = useState('initial');
  const [uploadedFile, setUploadedFile] = useState(null);

  // **New Function to Delete Uploaded File**
  const deleteUploadedFile = async (filename) => {
    try {
      const response = await axios.delete(`http://127.0.0.1:5001/delete/${filename}`);
      console.log(response.data.message);
    } catch (error) {
      console.error("Failed to delete the file:", error.response?.data?.error || error.message);
    }
  };

  const handleFileUpload = (fileData) => {
    if (fileData === null) {
      setDisplayState('uploading');
    } else {
      setUploadedFile(fileData);
      setDisplayState('uploaded');

      setTimeout(() => {
        setDisplayState('loading');
        setTimeout(() => {
          setDisplayState('results');
        }, 2000);
      }, 2000);
    }
  };

  const handleInitialChoice = (choice) => {
    if (choice === 'file') {
      setDisplayState('fileUpload');
    } else if (choice === 'link') {
      setDisplayState('linkUpload');
    }
  };

  const handleLinkChoice = (choice) => {
    if (choice === 'spotify') {
      setDisplayState('spotifyLink');
    } else if (choice === 'youtube') {
      setDisplayState('youtubeLink');
    }
  };

  // **New Function to Handle Reset (Start Over)**
  const handleReset = async () => {
    if (uploadedFile && uploadedFile.filename) {
      await deleteUploadedFile(uploadedFile.filename);
      setUploadedFile(null);
    }
    setDisplayState('initial');
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      {displayState === 'initial' && (
        <section className="relative flex flex-col md:flex-row items-center justify-center p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-4xl w-full z-20 border border-white/10 overflow-hidden">
          
          {/* Background Radial Gradient */}
          <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>

          {/* Content Wrapper */}
          <div className="flex flex-col md:flex-row items-center justify-between w-full z-10 space-y-8 md:space-y-0">
            
            {/* Left Side - Slogan */}
            <div className="md:w-1/2 px-4 text-center md:text-left">
              <h1 className="text-3xl md:text-5xl font-extrabold text-purple-600 mb-4 drop-shadow-md">
                AI-Powered Music Genre Classifier
              </h1>
              <p className="text-base md:text-xl text-purple-500 opacity-90">
                Instantly categorize your music with our advanced AI. Upload files or provide links to discover genres effortlessly.
              </p>
            </div>
            
            {/* Right Side - Buttons */}
            <div className="md:w-1/2 px-4">
              <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-purple-600 drop-shadow-md text-center md:text-left">
                Choose Upload Method
              </h2>
              <div className="flex flex-col gap-4">
                <button
                  onClick={() => handleInitialChoice('file')}
                  className="w-full px-6 py-4 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-800 transition duration-300"
                >
                  Upload Music File
                </button>
                <button
                  onClick={() => handleInitialChoice('link')}
                  className="w-full px-6 py-4 bg-gradient-to-r from-pink-500 to-pink-700 text-white rounded-xl shadow-lg hover:from-pink-600 hover:to-pink-800 transition duration-300"
                >
                  Provide Music Link
                </button>
              </div>
            </div>
          </div>
        </section>
      )}

      {displayState === 'fileUpload' && (
        <section className="relative flex flex-col items-center justify-center p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-3xl w-full z-20 border border-white/10 overflow-hidden">          
            {/* Background Radial Gradient */}
            <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
            
            {/* Content Wrapper */}
            <div className="flex flex-col items-center w-full z-10 space-y-6">    
                {/* Header */}
                <h2 className="text-2xl md:text-3xl font-semibold text-purple-600 drop-shadow-md text-center">
                    Upload Your Music File
                </h2>
                
                {/* File Upload Component */}
                <FileUpload 
                    onFileUpload={handleFileUpload} 
                    onBack={handleReset} // **Updated to use handleReset**
                />
            </div>
        </section>
      )}

      {displayState === 'linkUpload' && (
        <section className="w-full max-w-md p-8 bg-white/80 backdrop-blur-md rounded-lg shadow-xl">
          <h2 className="text-2xl font-semibold mb-6">Choose Link Type</h2>
          <div className="flex flex-col space-y-4">
            <button
              onClick={() => handleLinkChoice('spotify')}
              className="px-6 py-3 bg-primary text-white rounded hover:bg-primary-dark transition"
            >
              Spotify Link
            </button>
            <button
              onClick={() => handleLinkChoice('youtube')}
              className="px-6 py-3 bg-secondary text-white rounded hover:bg-secondary-dark transition"
            >
              YouTube Link
            </button>
          </div>
          <button
            onClick={handleReset} // **Updated to use handleReset**
            className="mt-6 w-full px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
          >
            Back
          </button>
        </section>
      )}

      {['spotifyLink', 'youtubeLink'].includes(displayState) && (
        <section className="relative flex flex-col md:flex-row items-center justify-center p-8 md:p-14 
          backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-5xl w-full z-20 
          border border-white/10 overflow-hidden">
          
          {/* Background Radial Gradient */}
          <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white 
            bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%, 
            rgba(120,119,198,0.3), rgba(255,255,255,0))]">
          </div>

          {/* Content Wrapper */}
          <div className="flex flex-col md:flex-row items-center w-full z-10 space-y-6 
            md:space-y-0 md:space-x-6">
            
            {/* Left Side - Back Button */}
            <div className="w-full md:w-1/2 flex justify-center">
              <button
                type="button"
                onClick={handleReset} // **Updated to use handleReset**
                className="w-full md:w-auto px-6 py-4 bg-red-500 text-white rounded-xl shadow-lg hover:bg-red-600 
                  transition duration-300 text-lg md:text-xl font-semibold"
              >
                Back
              </button>
            </div>

            {/* Right Side - Link Processing Component */}
            <div className="w-full md:w-1/2 flex flex-col items-center">
              {/* Header */}
              <h2 className="text-2xl md:text-3xl font-semibold text-purple-600 drop-shadow-md text-center mb-4">
                {displayState === 'spotifyLink' ? 'Enter Spotify Link' : 'Enter YouTube Link'}
              </h2>
              
              {displayState === 'spotifyLink' ? (
                  <SpotifyLinkProcessing onFileUpload={handleFileUpload} />
              ) : (
                  <YoutubeLinkProcessing onFileUpload={handleFileUpload} />
              )}
            </div>
          </div>
        </section>
      )}

      {displayState === 'uploading' && (
        <section className="relative flex flex-col items-center justify-center p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-3xl w-full z-20 border border-white/10 overflow-hidden">
          
          {/* Background Radial Gradient */}
          <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>

          {/* Content Wrapper */}
          <div className="flex flex-col items-center w-full z-10 space-y-6">    
              {/* Loading Indicator */}
              <Loading />
          </div>
        </section>
      )}

      {displayState === 'uploaded' && (
        <section className="relative flex flex-col items-center justify-center p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-3xl w-full z-20 border border-white/10 overflow-hidden">
          
          {/* Background Radial Gradient */}
          <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>

          {/* Content Wrapper */}
          <div className="flex flex-col items-center w-full z-10 space-y-6">    
              {/* Success Message */}
              <p className="text-xl md:text-2xl font-semibold text-purple-600 drop-shadow-md text-center">
                  Uploaded Successfully!
              </p>
          </div>
        </section>
      )}

      {displayState === 'loading' && (
        <section className="relative flex flex-col items-center justify-center p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl max-w-3xl w-full z-20 border border-white/10 overflow-hidden">
          
          {/* Background Radial Gradient */}
          <div className="absolute top-0 left-0 z-[-2] h-full w-full bg-white bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>

          {/* Content Wrapper */}
          <div className="flex flex-col items-center w-full z-10 space-y-6">    
              {/* Loading Indicator */}
              <Loading />
          </div>
        </section>
      )}

      {/* Results State */}
      {displayState === 'results' && uploadedFile && (
        <section className="relative flex flex-col items-center justify-center p-8 md:p-10 bg-white rounded-lg md:rounded-2xl shadow-none max-w-5xl w-full z-20 border border-gray-300 overflow-hidden">
          
          {/* Content Wrapper */}
          <div className="w-full">
            <ResultsDisplay 
              songName={uploadedFile.song_name} 
              artist={uploadedFile.artist} 
              coverImageUrl={uploadedFile.cover_image_url} 
              genres={uploadedFile.genres} 
              filename={uploadedFile.filename}
              handleReset={handleReset} // **Pass handleReset as a prop**
            />
          </div>
        </section>
      )}
    </div>
  );
}

export default UseApp;