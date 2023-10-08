import React, { useEffect, useState } from "react";
import axios from "axios";

function Home(): JSX.Element {
  const [message, setMessage] = useState("")

  const fetchHelloMessage = () => {
    axios.get("http://localhost:8000/auth")
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

export default Home;