// App.js
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UseApp from './pages/UseApp';
import AboutModel from './pages/AboutModel';
import AboutUs from './pages/AboutUs';
import Navbar from './pages/components/Navbar';

function App() {
  return (
    <>
      <Router>
        <div className="App">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<UseApp />} />
              <Route path="/about-model" element={<AboutModel />} />
              <Route path="/about-us" element={<AboutUs />} />
              {/* Optional: Add a 404 Not Found page */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
      </Router>
    </>
  );
}

function NotFound() {
  return (
    <div className="not-found">
      <h2>404 - Page Not Found</h2>
      <p>The page you're looking for doesn't exist.</p>
    </div>
  );
}

export default App;
