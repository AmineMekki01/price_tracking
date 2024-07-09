import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import PriceHistoryChart from './../components/PriceHistoryChart';

const Container = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
`;

const PriceList = styled.ul`
    list-style-type: none;
    padding: 0;
`;

const PriceItem = styled.li`
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    margin: 8px 0;
`;

function PriceHistory() {
    const { productId } = useParams();
    const [product, setProduct] = useState(null);
    const [priceHistory, setPriceHistory] = useState([]);

    useEffect(() => {
        const fetchPriceHistory = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/price-history/${productId}`);
                setProduct(response.data.product);
                setPriceHistory(response.data.price_history);
                console.log('Price History Data:', response.data.price_history); // Debugging step
            } catch (error) {
                console.error('Error fetching price history:', error);
            }
        };

        fetchPriceHistory();
    }, [productId]);

    return (
        <Container>
            {product && (
                <>
                    <h2>{product.name}</h2>
                    <img src={product.img} alt={product.name} />
                    <PriceHistoryChart data={priceHistory} />
                </>
            )}
        </Container>
    );
}

export default PriceHistory;
