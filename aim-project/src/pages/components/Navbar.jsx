//components/Navbar.jsx
import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-name">
        <Link>
          <NavLink to="/" end activeClassName="active">
            <h1>Classif.ai</h1>
          </NavLink>
        </Link>
      </div>
      <div className="navbar-links">
        <Link>
          <NavLink to="/about-model" activeClassName="active">
            About the Model
          </NavLink>
        </Link>
        <Link>
          <NavLink to="/about-us" activeClassName="active">
            About Us
          </NavLink>
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
