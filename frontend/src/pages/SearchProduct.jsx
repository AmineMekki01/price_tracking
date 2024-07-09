import React, { useState } from 'react';
import axios from 'axios';
import ProductCard from './../components/ProductCard';
import styled from 'styled-components';

const Container = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
`;

const Input = styled.input`
    width: 80%;
    padding: 8px;
    margin: 16px 0;
    font-size: 1em;
`;

const SearchButton = styled.button`
    padding: 8px 16px;
    font-size: 1em;
    color: #fff;
    background-color: #007BFF;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
        background-color: #0056b3;
    }
`;

const Results = styled.div`
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
`;

function SearchProduct() {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/search', {
                params: {
                    product_name: searchTerm,
                    platforms: ['amazon']
                }
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error searching for products:', error);
        }
    };

    const handleTrack = async (productId) => {
        console.log('Tracking:', productId);
        try {
            const response = await axios.post('http://localhost:8000/api/track', { product_id: productId, search_text: searchTerm});
            alert('Tracking started for selected products');
        } catch (error) {
            console.error('Error tracking product:', error);
        }
    };

    return (
        <Container>
            <Input 
                type="text" 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
                placeholder="Search for products" 
            />
            <SearchButton onClick={handleSearch}>Search</SearchButton>
            <Results>
                {results.map(product => (
                    <ProductCard key={product.id} product={product} onTrack={() => handleTrack(product.id)} TrackOrHistory="track" />
                ))}
            </Results>
        </Container>
    );
}

export default SearchProduct;
