import React, {useState} from 'react'
import FormSignup from './FormSignup';
import FormSuccess from './FormSuccess';
import './Form.css';
import Otp from '..//OtpPage/OtpForm';




function Form() {
    // const [step,setStep]=useState(0)
    
    
    
    const [isSubmitted, setIsSubmitted] = useState(false)
    function submitForm() {
        setIsSubmitted(true)
    }
    return (
        <>
        <div className='form-container'>
            <span className='close-btn'>x</span>
            <div className='form-content-left'>
                <img src='img/img-2.svg' alt='spaceship'
                className='form-img'/>
            </div>
            {!isSubmitted ? (
            <FormSignup submitForm={submitForm}/> 
            ) : 
               ( // <FormSuccess />
                <Otp />)
            }
        </div>
        </>
    )
            
};

export default Form
