// src/App.js

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UseApp from './pages/UseApp';
import AboutModel from './pages/AboutModel';
import AboutUs from './pages/AboutUs';
import Navbar from './pages/components/Navbar'; // Adjusted import path
import BackgroundDivider from './pages/components/BackgroundAnimation'; // Import the background component

function App() {
  return (
    <Router>
      <div className="App relative">
        {/* Background Divider */}
        <BackgroundDivider />

        {/* Navbar */}
        <Navbar />

        {/* Main Content */}
        <main className="relative z-10 w-screen">
          <Routes>
            <Route path="/" element={<UseApp />} />
            <Route path="/about-model" element={<AboutModel />} />
            <Route path="/about-us" element={<AboutUs />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-transparent">
      <h2 className="text-3xl font-bold text-red-600 mb-4">404 - Page Not Found</h2>
      <p className="text-lg text-gray-300">The page you're looking for doesn't exist.</p>
    </div>
  );
}

export default App;
