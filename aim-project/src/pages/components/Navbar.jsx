// src/components/Navbar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full px-6 py-4 flex justify-between items-center bg-transparent z-20">
      {/* Navbar Gradient Background */}
      <div className="absolute top-0 left-0 h-full w-full bg-neutral-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))] z-10"></div>

      {/* Navbar Content */}
      <NavLink to="/" end className="text-white text-4xl font-bold tracking-wide relative z-20 hover:none">
        Classif<span className="text-primary">.ai</span>
      </NavLink>
      <div className="flex space-x-4 relative z-20">
        {/* About the Model Link */}
        <NavLink to="/about-model">
          {({ isActive }) => (
            <div className="relative group">
              <span
                className={`text-lg font-medium px-4 py-2 rounded-lg transition-all ${
                  isActive
                    ? "text-primary bg-gray-800"
                    : "text-gray-300 hover:text-primary hover:bg-gray-700"
                }`}
              >
                About the Model
              </span>
              {/* Glowing Border */}
              {!isActive && (
                <span className="absolute inset-0 border-2 border-transparent rounded-lg group-hover:border-primary opacity-0 group-hover:opacity-100 transition-opacity duration-300 animate-pulseGlow"></span>
              )}
            </div>
          )}
        </NavLink>

        {/* About Us Link */}
        <NavLink to="/about-us">
          {({ isActive }) => (
            <div className="relative group">
              <span
                className={`text-lg font-medium px-4 py-2 rounded-lg transition-all ${
                  isActive
                    ? "text-primary bg-gray-800"
                    : "text-gray-300 hover:text-primary hover:bg-gray-700"
                }`}
              >
                About Us
              </span>

              {/* Glowing Border */}
              {!isActive && (
                <span className="absolute inset-0 border-2 border-transparent rounded-lg group-hover:border-primary opacity-0 group-hover:opacity-100 transition-opacity duration-300 animate-pulseGlow"></span>
              )}
            </div>
          )}
        </NavLink>
      </div>
    </nav>
  );
}

export default Navbar;
