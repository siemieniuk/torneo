import React, { useEffect, useState } from "react";
import axios from "axios";

function Home(): JSX.Element {
  const [message, setMessage] = useState("")

  const fetchHelloMessage = () => {
    axios.get("http://localhost:8000/auth")
      .then(response => {
        console.log(response.data)
      })
  }

  useEffect(() => {
    fetchHelloMessage()
  }, [])
  return (
    <div className="App">
      <div className="container-fluid">
        <h1>Hello {localStorage.getItem("sub")}</h1>
        <p>{localStorage.getItem("access-token")}</p>
        <p>{message}</p>
      </div>
    </div>
  );
}

export default Home;