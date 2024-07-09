import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import ProductCard from './../components/ProductCard';
const Container = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
`;

const ProductLink = styled(Link)`
    display: block;
    margin: 8px 0;
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    text-decoration: none;
    color: #333;

    &:hover {
        background-color: #f0f0f0;
    }
`;

function TrackedProducts() {
    const [trackedProducts, setTrackedProducts] = useState([]);

    useEffect(() => {
        const fetchTrackedProducts = async () => {
            console.log('Fetching tracked products');
            try {
                const response = await axios.get('http://localhost:8000/api/tracked-products');
                setTrackedProducts(response.data);
            } catch (error) {
                console.error('Error fetching tracked products:', error);
            }
        };

        fetchTrackedProducts();
    }, []);

    return (
        <Container>
            <h2>Tracked Products</h2>
            {trackedProducts.map(product => (
                <ProductCard key={product.id} product={product} TrackOrHistory="history"/>
             
            ))}
        </Container>
    );
}

export default TrackedProducts;
