import React from 'react';
import ReactDOM from 'react-dom';
// import './index.css';
import App from './App';
import axios from 'axios';
// import reportWebVitals from './reportWebVitals';


axios.defaults.baseURL = 'http://127.0.0.1:8080';
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);


