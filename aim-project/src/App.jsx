import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className = "navbar">
        <ul>
          <li>Use our App</li>
          <li>About the model</li>
          <li>About us</li>
        </ul>
      </div>
      <section id="upload" className="upload-section">
        <h2>Upload Your File</h2>
        <p>[File upload placeholder]</p>
      </section>

      <div className="loading-placeholder">
        <p>[Loading indicator placeholder]</p>
      </div>

      <div className="results-placeholder">
        <p>[Results display placeholder]</p>
      </div>

      <footer className="landing-footer">
        <p>© 2024 Your Company. All rights reserved.</p>
      </footer>
    </>
  )
}

export default App
