import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './components/FileUpload'
import FileUpload from './components/FileUpload'
import ResultsDisplay from './components/ResultsDisplay'

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
      <FileUpload/>

      <div className="loading-placeholder">
        <p>[Loading indicator placeholder]</p>
      </div>

      <div className="results-placeholder">
        <p>[Results display placeholder]</p>
      </div>
      <ResultsDisplay/>


    </>
  )
}

export default App
