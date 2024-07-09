// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchProduct from './pages/SearchProduct';
import TrackedProducts from './pages/TrackedProducts';
import PriceHistory from './pages/PriceHistory';
import DirectLinkSearch from './pages/DirectLinkSearch';
import Navbar from './components/Navbar';

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/search-product" element={<SearchProduct />} />
                <Route path="/tracked-products" element={<TrackedProducts />} />
                <Route path="/price-history/:productId" element={<PriceHistory />} />
                <Route path="/direct-link-search" element={<DirectLinkSearch />} />
            </Routes>
        </Router>
    );
}

export default App;
