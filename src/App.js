// App.js
import React from 'react';
import ProductList from './components/home/home.jsx'; 
import Header from './components/home/header.jsx';
import Footer from './components/home/footer.jsx';


function App() {
  return (
    <div className="App">
    <Header/>
      <h1>Product App</h1>

      <ProductList />
      <Footer />
    </div>
  );
}

export default App;

