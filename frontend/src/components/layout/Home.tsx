import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import { GlobalContext } from "../../App";
import isAuthenticated from "../../context/isAuthenticated";

function Home(): React.JSX.Element {
  const [name, setName] = useState("")
  const fetchHelloMessage = () => {
    axios.get("http://localhost:8000/api/v1/auth")
      .then(response => {
        console.log(response.data)
      })
  }

  if (isAuthenticated()) {
    const token = localStorage.getItem("access-token")
    const options = {
      method: "GET",
      url: "http://localhost:8000/api/v1/auth/me",
      headers: {
        "Authorization": `Bearer ${token}`,
        "accept": "application/json",
      }
    }

    axios(options)
      .then(response => {
        setName(response.data.first_name)
      })
  }

  useEffect(() => {
    fetchHelloMessage()
  }, [])
  return (
    <div className="App">
      <div className="container-fluid">
        <h1>Hello {name}</h1>
        {isAuthenticated() && (
          <>
            <h2>Your tournaments</h2>
            <em>Empty</em>
          </>
        )}
      </div>
    </div>
  );
}

export default Home;