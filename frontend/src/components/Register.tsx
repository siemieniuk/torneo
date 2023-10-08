import React, { useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form"

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  function signUp() {
    let item = { username, email, password, confirmPassword };
    console.log(item)
  }

  return (
    <div>
      <Form>
        <h1>Register page</h1>
        <Form.Group className="mb-3 col-sm-4" controlId="formBasicUsername">
          <Form.Control type="text" placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-sm-4" controlId="formBasicEmail">
          <Form.Control type="text" placeholder="email" onChange={(e) => setEmail(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-sm-4" controlId="formBasicPassword">
          <Form.Control type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-sm-4" controlId="formBasicPassword2">
          <Form.Control type="password" id="formBasicPassword2" placeholder="confirm password" onChange={(e) => setConfirmPassword(e.target.value)} />
        </Form.Group>
        <Button variant="primary" onClick={signUp}>
          Submit
        </Button>
      </Form>
    </div>
  )
}

export default Register;