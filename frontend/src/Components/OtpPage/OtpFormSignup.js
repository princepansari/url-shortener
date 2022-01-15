import React from 'react'
import useForm from './OtpUseForm'
import validate from '../validateInfo'
import './Form.css';
import { Link } from 'react-router-dom';




const Formsignup = ({submitForm}) => {

    const {handleChange, values, handleSubmit, errors} 
    = useForm(
        submitForm,
        validate
        );

    return (
       <div className='form-content-right'>
           <form className='form' onSubmit={handleSubmit}>
               <h1>Enter otp below which is sended on 
                   your Email ID.
               </h1>
               
               <div className='form-inputs'>
                   <label htmlFor='password'
                   className='form-label'>
                       OTP
                   </label>
                   <input 
                       id='password' 
                       type='text' 
                       name='password'
                       className='form-input'
                       placeholder='Enter OTP'
                       value={values.password}
                       onChange={handleChange}
                       />
                       {errors.password && <p>{errors.password}</p>}
               </div>
               <span className='form-input-login'>
                   Did not get OTP
                   <a href='<Form />'>Resend</a>
               </span>
               <button className='form-input-btn'
               type='submit'>
                   Validate
               </button>
               <span className='form-input-login'>
                   <Link to="/">SignIn</Link>
                   /
                   <Link to="/SignUp">SignUp</Link>
               </span>
               
           </form>
       </div>

    )
}

export default Formsignup
