import React from "react";
import "./style.css";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';


const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
      <div className="row">
      <div className="col-md-6">
        <div>
          <h2>A Marketplace for Your Goods</h2>
        </div>
      </div>

      <div className="col-md-6 col3">
        <ul className="list-unstyled d-flex">
          <li className="me-3" href="#">Home</li>
          <li className="me-3" href="#">Products</li>
          <li className="me-3" href="#">Promotions</li>
          <li className="me-3" href="#">About us</li>
          <li className="me-3" href="#">Brands</li>   
        </ul>
      </div>
    </div><hr/>
    <p>Privacy | Policy<span>Antony web design @2023</span><span><Button variant="outline-primary">thumbs up</Button></span></p>  
    </div>
    </footer>
  );
};

export default Footer;


