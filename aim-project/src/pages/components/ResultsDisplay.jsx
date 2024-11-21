// src/pages/components/ResultsDisplay.jsx

import React, { useState } from 'react';
import GenreChart from './GenreChart';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import PropTypes from 'prop-types';

const DEFAULT_COVER_IMAGE = "https://via.placeholder.com/300?text=No+Cover+Image";

const ResultsDisplay = ({
  songName = "Unknown Song",
  artist = "Unknown Artist",
  coverImageUrl = DEFAULT_COVER_IMAGE,
  genres = [],
  filename = null,
  handleReset
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = () => {
    setIsOpen(prevState => !prevState);
  };

  const audioSrc = filename ? `http://127.0.0.1:5001/uploads/${filename}` : null;

  // Function to Generate PDF
  const generatePDF = async () => {
    try {
      const doc = new jsPDF('p', 'mm', 'a4');
      const margin = 10;
      let y = margin;

      // Add Song Metadata
      doc.setFontSize(20);
      doc.text(songName, margin, y);
      y += 10;
      doc.setFontSize(16);
      doc.setTextColor(100);
      doc.text(`Artist: ${artist}`, margin, y);
      y += 10;

      // Add Cover Image
      try {
        const img = await getImageDataUrl(coverImageUrl);
        doc.addImage(img, 'JPEG', margin, y, 50, 50);
      } catch (error) {
        console.error("Failed to load cover image for PDF:", error);
        doc.setFontSize(12);
        doc.setTextColor(255, 0, 0); // Red color for error message
        doc.text("Cover image not available.", margin, y + 25);
      }
      y += 60;

      // Add Genre List
      if (genres.length > 0) {
        doc.setFontSize(16);
        doc.setTextColor(0);
        doc.text('Predicted Genres:', margin, y);
        y += 10;
        genres.forEach((genre, index) => {
          doc.setFontSize(12);
          doc.text(`${index + 1}. ${genre.name} (${genre.confidence}%)`, margin + 5, y);
          y += 7;
        });
      } else {
        doc.setFontSize(12);
        doc.setTextColor(255, 0, 0);
        doc.text("No genre data available.", margin, y);
        y += 10;
      }

      // Add Genre Chart using html2canvas
      const chartElement = document.getElementById('genre-chart');
      if (chartElement) {
        try {
          const canvas = await html2canvas(chartElement, { scale: 2 });
          const chartImg = canvas.toDataURL('image/png');
          doc.addImage(chartImg, 'PNG', margin, y, 190, 100);
          y += 110;
        } catch (error) {
          console.error("Failed to capture genre chart:", error);
          doc.setFontSize(12);
          doc.setTextColor(255, 0, 0); // Red color for error message
          doc.text("Genre chart not available.", margin, y + 100);
        }
      }

      // Save the PDF
      doc.save(`${songName}_classification.pdf`);
    } catch (error) {
      console.error("PDF generation failed:", error);
      alert("Failed to generate PDF. Please try again.");
    }
  };

  // Helper function to convert image URL to data URL
  const getImageDataUrl = (url) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.setAttribute('crossOrigin', 'anonymous');
      img.onload = () => {
        const canvas = document.createElement('canvas');
        // Resize image if necessary
        const maxWidth = 300;
        const scale = Math.min(maxWidth / img.width, 1);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');
        resolve(dataURL);
      };
      img.onerror = (err) => {
        reject(err);
      };
      img.src = url;
    });
  };

  return (
    <div className="w-full p-4">
      {/* Container with responsive grid layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Left Column: Title, Artist, Cover Image */}
        <div className="flex flex-col items-center justify-start space-y-2">
          <h2 className="text-2xl leading-5 text-center font-bold text-purple-600">{songName}</h2>
          <p className="text-purple-400 leading-5 text-center">by {artist}</p>
          <div className="w-full max-w-xs bg-gray-200 rounded-lg overflow-hidden">
            <img 
              src={coverImageUrl} 
              alt={`${songName} cover`} 
              className="w-full h-auto object-cover"
              onError={(e) => { e.target.src = DEFAULT_COVER_IMAGE; }}
            />
          </div>
        </div>

        {/* Right Column: Genre Chart, Buttons */}
        <div className="flex flex-col items-center justify-start space-y-4">
          {genres.length > 0 && (
            <div className="w-full">
              <h3 className="text-2xl text-center font-bold text-purple-600">Genre Distribution</h3>
              <div id="genre-chart" className="items-center">
                <GenreChart genres={genres} />
              </div>
            </div>
          )}

          <div className="flex flex-row flex-wrap justify-center space-x-4">
            {/* Open Song Button */}
            {filename && (
              <button 
                onClick={handleOpen} 
                className="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 m-1"
                aria-pressed={isOpen}
                aria-label={isOpen ? 'Close Song' : 'Open Song'}
              >
                {isOpen ? 'Close Song' : 'Open Song'}
              </button>
            )}

            {/* Download PDF Button */}
            <button
              onClick={generatePDF}
              className="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-lg hover:from-purple-600 hover:to-purple-800 transition duration-300 m-1"
              aria-label="Download Results as PDF"
            >
              Download Results
            </button>

            {/* Start Over Button */}
              <button
                onClick={handleReset}
                className="py-2 bg-gradient-to-r from-purple-500 
                  to-purple-700 text-white rounded-lg hover:from-purple-600 
                  hover:to-purple-800 transition duration-300 text-md md:text-lg font-semibold m-1"
                aria-label="Start Over"
              >
                Start Over
              </button>
          </div>

          {/* Audio Player and Download Link */}
          {isOpen && audioSrc && (
            <div className="flex flex-col items-center mt-6 w-full">
              <audio controls className="w-5/6">
                <source src={audioSrc} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
              <a 
                href={audioSrc} 
                download 
                className="text-purple-500 hover:underline mt-2"
                aria-label="Download Audio File"
              >
                Download File
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

ResultsDisplay.propTypes = {
  songName: PropTypes.string,
  artist: PropTypes.string,
  coverImageUrl: PropTypes.string,
  genres: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      confidence: PropTypes.number.isRequired,
    })
  ),
  filename: PropTypes.string,
  handleReset: PropTypes.func.isRequired,
};

export default ResultsDisplay;