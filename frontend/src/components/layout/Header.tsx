import React from "react";
import Nav from "react-bootstrap/Nav"
import Navbar from "react-bootstrap/Navbar"
import Container from "react-bootstrap/Container"

import isAuthenticated from "../../context/isAuthenticated";

function Header(): React.JSX.Element {

  function logout() {
    localStorage.clear();
    window.location.href = "/";
  }

  return (
    <Navbar bg="primary" variant="light" expand="lg" fixed="top">
      <Container>
        <Navbar.Brand href="/">
          <img src="/logo_big.png"
            height="30"
            className="d-inline-block align-top"
            alt="Torneo logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link className="navbar-link" href="/">Home</Nav.Link>
            {isAuthenticated() ?
              <>
                <Nav.Link onClick={logout}>Logout</Nav.Link>
              </> :
              <>
                <Nav.Link href="/register/">Register</Nav.Link>
                <Nav.Link href="/login/">Login</Nav.Link>
              </>
            }
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Header;