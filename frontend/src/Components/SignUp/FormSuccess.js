import React from 'react'
import { Link } from 'react-router-dom';
import './Form.css';

const formSuccess = () => {
    return (
        
        <div className='form-content-right'>
            <div className='form-success'>We have received your request!</div>
            <img src='img/img-3.svg' alt='success-image' className='form-img-2'  />
        </div>
    );
};

export default formSuccess
