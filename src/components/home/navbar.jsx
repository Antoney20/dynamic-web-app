import React from 'react';
import {Button ,Container, Form, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import './style.css'

function Topnavbar() {
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container fluid>
        <Navbar.Brand href="#home">React-shopify</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#action1">Home</Nav.Link>
            <Nav.Link href="#action2">Products</Nav.Link>
            <Nav.Link href="#action2">Promotions</Nav.Link>
            <Nav.Link href="#action2">Brands</Nav.Link>
            <Nav.Link href="#action2">Blog</Nav.Link>
            <NavDropdown title="Support" id="navbarScrollingDropdown">
              <NavDropdown.Item href="#action3">About us</NavDropdown.Item>
              <NavDropdown.Item href="#action4">
                Contact us
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action5">
                Privacy policy
              </NavDropdown.Item>
              <NavDropdown.Item href="#action5">
                FAQs
              </NavDropdown.Item>
            </NavDropdown>
    
          </Nav>
          <Form className="d-flex">
            <Form.Control  type="search" placeholder="Search" className="me-2" aria-label="Search" />
            <Button variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
        
           <Nav.Link  className="Login" href="#login">Login</Nav.Link>
            <Nav.Link className='cart' href="#cart">cart</Nav.Link>
      </Container>
    </Navbar>
  );
}

export default Topnavbar;