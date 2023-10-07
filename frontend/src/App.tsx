import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState("")

  const fetchHelloMessage = () => {
    axios.get("http://localhost:8000/")
      .then(response => {
        setMessage(response.data.message)
      })
  }

  useEffect(() => {
    fetchHelloMessage()
  }, [])

  return (
    <div className="App">
      <div className="container-fluid">
        <p>{message}</p>
      </div>
    </div>
  );
}

export default App;
