import axios from "axios";
import { useState,useEffect } from "react";

const useForm=(callback, validate) => {
    const [values, setValues]= useState({
        // username: '',
        email: '',
        password: '',
        password2: ''
    });
    const [errors, setErrors]= useState({});
    const[isSubmitting, setIsSubmitting] = useState(false);

    const handleChange = e=> {
        const { name, value}=e.target;
        setValues({
            ...values,
            [name]: value
        });
    };

    const handleSubmit= e => {
        e.preventDefault();

        setErrors(validate(values));
        setIsSubmitting(true);
        // console.log(e)

        const data =  {
            email : values.email,
            password : values.password
        }

        axios.post('/auth/signup', data)
            .then(res => {
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
        
    };

    useEffect( () => {
        if(Object.keys(errors).length === 0 &&
        isSubmitting){
            callback();
        }
    },
    [errors]
    );
    return {handleChange, handleSubmit, values, errors };
};
export default useForm;