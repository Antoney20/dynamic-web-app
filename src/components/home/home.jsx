// Home javascript

//import './app/App.css'
import React, { useState, useEffect } from 'react';

function ProductList() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/products/')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Product List</h1>
            <ul>
                {products.map(product => (
                    <li key={product.id}>
                        {product.name} - {product.description}
                       <img src= {product.image}  alt='' />
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ProductList;
