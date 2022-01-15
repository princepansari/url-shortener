import React from 'react'

import useForm from './LoginUseForm'
import validate from '../validateInfo'
import Form from '../SignUp/Form';
import './Form.css';
import { Link } from 'react-router-dom';




const Formsignup = (submitForm) => {

    const {handleChange, values, handleSubmit, errors} 
    = useForm(
        submitForm,
        validate
        );

    return (
       <div className='form-content-right'>
           <form className='form' onSubmit={handleSubmit}>
               <h1>Login Your account by filling 
                   out the information below.
               </h1>
               <div className='form-inputs'>
                   <label htmlFor='email'
                   className='form-label'>
                       Email
                   </label>
                   <input 
                       id='email' 
                       type='text'
                       name='email'
                       className='form-input'
                       placeholder='Enter your email'
                       value={values.Email}
                       onChange={handleChange}
                       />
                       {errors.email && <p>{errors.email}</p>}
               </div>
               <div className='form-inputs'>
                   <label htmlFor='password'
                   className='form-label'>
                       Password
                   </label>
                   <input 
                       id='password' 
                       type='password' 
                       name='password'
                       className='form-input'
                       placeholder='Enter your password'
                       value={values.password}
                       onChange={handleChange}
                       />
                       {errors.password && <p>{errors.password}</p>}
               </div>
               <button className='form-input-btn'
               type='submit'>
                   Log In
               </button>
               <span className='form-input-login'>
                   New User? SignUp
                   <Link to="/SignUp">here</Link>
               </span>
           </form>
       </div>

    )
}

export default Formsignup
