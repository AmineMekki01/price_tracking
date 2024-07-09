import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const Card = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 300px;
    margin: 16px;
    background-color: #fff;
`;

const Image = styled.img`
    max-width: 100%;
    border-radius: 8px;
`;

const Details = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 16px;
`;

const Name = styled.h3`
    font-size: 1.2em;
    margin: 0 0 8px 0;
    text-align: center;
`;

const Price = styled.p`
    font-size: 1em;
    margin: 0 0 16px 0;
    color: #888;
`;

const Button = styled.button`
    padding: 8px 16px;
    font-size: 1em;
    color: #fff;
    background-color: #007BFF;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;

    &:hover {
        background-color: #0056b3;
    }
`;

function ProductCard({ product, onTrack, TrackOrHistory }) {
    return (
        <Card>
            <Image src={product.img} alt={product.name} />
            <Details>
                <Name>{product.product_name}</Name>
                <Price>{product.price} {product.currency}</Price>
                {TrackOrHistory === "track" && (
                    <Button onClick={() => onTrack(product.id)}>Track</Button>
                )}
                {TrackOrHistory === "history" && (
                    <Link to={`/price-history/${product.id}`}>
                        <Button>Price History</Button>
                    </Link>
                )}
            </Details>
        </Card>
    );
}

export default ProductCard;
