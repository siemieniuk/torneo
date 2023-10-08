import React, { useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form"

function Login(): JSX.Element {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function signUp() {
    let item = { username, password };
    console.log(item)
  }

  return (
    <Form className="mb-3">
      <h1>Login page</h1>
      <Form.Group className="mb-3 col-sm-4" controlId="formBasicUsername">
        <Form.Control type="text" placeholder="username" onChange={(e) => setUsername(e.target.value)} />
      </Form.Group>
      <Form.Group className="mb-3 col-sm-4" controlId="formBasicPassword">
        <Form.Control type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
      </Form.Group>
      <Button variant="primary" onClick={signUp}>
        Login
      </Button>
    </Form>
  )
}

export default Login;