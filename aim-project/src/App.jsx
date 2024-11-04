import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './components/FileUpload'
import FileUpload from './components/FileUpload'

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
     
      <FileUpload/>
      <Loading/>

      <div className="results-placeholder">
        <p>[Results display placeholder]</p>
      </div>

     
    </>
  )
}

export default App
