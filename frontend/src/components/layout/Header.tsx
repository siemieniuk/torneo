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
    <Navbar expand="lg" className="bg-body-tertiary" fixed="top">
      <Container>
        <Navbar.Brand href="#home"></Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
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