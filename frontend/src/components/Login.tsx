import axios from "axios";
import React, { useContext, useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form"
import { useNavigate } from "react-router-dom";
import qs from "qs"

import { GlobalContext } from "../App";

function Login(): JSX.Element {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validationErrors, setValidationErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { isAuthenticated, setIsAuthenticated } = useContext(GlobalContext);

  useEffect(() => {
    console.log(localStorage.getItem("token"));
    if (localStorage.getItem("token") != "" && localStorage.getItem("token") != null) {
      navigate("/");
    }
  }, []);

  const signUp = (e: React.FormEvent<HTMLFormElement>) => {
    setValidationErrors({});
    e.preventDefault();
    setIsSubmitting(true);

    let payload = {
      username: email,
      password: password,
    };

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: qs.stringify(payload),
      url: "http://localhost:8000/api/v1/auth/token"
    };

    axios(options)
      .then((r) => {
        setIsSubmitting(false);
        localStorage.setItem("access-token", r.data.access_token);
        localStorage.setItem("sub", r.data.sub);
        setIsAuthenticated(true);
        navigate("/")
      })
      .catch((e) => {
        setIsSubmitting(false)
        if (e.response.data.errors != undefined) {
          setValidationErrors(e.response.data.errors);
        }
        if (e.response.data.error != undefined) {
          setValidationErrors(e.response.data.error);
        }
      })
  }

  return (
    <Form className="mb-3" onSubmit={signUp}>
      {Object.keys(validationErrors).length != 0 &&
        <p className='text-center '><small className='text-danger'>Incorrect Email or Password</small></p>
      }
      <h1>Login page</h1>
      <Form.Group className="mb-3 col-lg-4" controlId="formBasicEmail">
        <Form.Control required type="email" placeholder="email" onChange={(e) => setEmail(e.target.value)} />
      </Form.Group>
      <Form.Group className="mb-3 col-lg-4" controlId="formBasicPassword">
        <Form.Control required type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
      </Form.Group>
      <Button variant="primary" type="submit">
        Login
      </Button>
    </Form>
  )
}

export default Login;