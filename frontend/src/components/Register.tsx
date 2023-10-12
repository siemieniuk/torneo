import axios from "axios";
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form"
import { useNavigate } from "react-router-dom";

function Register(): React.JSX.Element {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [validationErrors, setValidationErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const signUp = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    let payload = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      password2: password2,
    };
    axios.post('http://localhost:8000/auth/register', payload)
      .then((r) => {
        setIsSubmitting(false);
        navigate("/login")
      })
      .catch((e) => {
        setIsSubmitting(false);
        if (e.response.data.errors != undefined) {
          setValidationErrors(e.response.data.errors);
        }
      })
    console.log(payload);
  }

  useEffect(() => {
    if (localStorage.getItem("token") != "" &&
      localStorage.getItem("token") != null) {

      navigate("/")
    }
  }, []);

  return (
    <div>
      <Form onSubmit={signUp}>
        <h1>Register page</h1>
        <Form.Group className="mb-3 col-lg-4" controlId="formBasicFirstName">
          <Form.Control
            required
            type="text"
            placeholder="First name"
            onChange={(e) => setFirstName(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-lg-4" controlId="formBasicLastName">
          <Form.Control
            required
            type="text"
            placeholder="Last name"
            onChange={(e) => setFirstName(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-lg-4" controlId="formBasicEmail">
          <Form.Control
            required
            type="email"
            placeholder="email"
            onChange={(e) => setEmail(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-lg-4" controlId="formBasicPassword">
          <Form.Control
            required
            type="password"
            placeholder="password"
            minLength={8}
            maxLength={30}
            onChange={(e) => setPassword(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3 col-lg-4" controlId="formBasicPassword2">
          <Form.Control
            required
            type="password"
            id="formBasicPassword2" placeholder="confirm password"
            minLength={8}
            maxLength={30}
            onChange={(e) => setPassword2(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
  )
}

export default Register;