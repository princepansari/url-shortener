import React, {useState} from 'react'
import FormSignup from './OtpFormSignup';
import FormSuccess from './OtpFormSuccess';
import './Form.css';

function Form() {
    const [isSubmitted, setIsSubmitted] = useState(false)
    function submitForm() {
        setIsSubmitted(true)
    }
    return (
        <>
        <div className='form-container'>
            <span className='close-btn'>x</span>
            <div className='form-content-left'>
                {/* <img src='img/img-2.svg' alt='spaceship'
                className='form-img'/> */}
                <img src={process.env.PUBLIC_URL + '/img/img-2.svg'} alt='spaceship'
                className='form-img'/>
            </div>
            {!isSubmitted ? (
            <FormSignup submitForm={submitForm}/> 
            ):( <FormSuccess />)}
        </div>
        </>
    )
            
};

export default Form
