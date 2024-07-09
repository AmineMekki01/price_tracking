// DirectLinkSearch.js
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

function DirectLinkSearch() {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);

    const handleSearch = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/search-product-url', {
                url: url
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error searching for product:', error);
        }
    };

    return (
        <Container>
            <Input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="Enter product URL" 
            />
            <SearchButton onClick={handleSearch}>Search</SearchButton>
            <Results>
                {result && <ProductCard product={result} TrackOrHistory="history" />}
            </Results>
        </Container>
    );
}

export default DirectLinkSearch;
