import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './components/FileUpload'
import FileUpload from './components/FileUpload'
import Loading from './components/Loading'

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
      <ResultsDisplay/>
     
    </>
  )
}

export default App
