import { BrowserRouter, Route, Link,  Routes } from "react-router-dom"; //import the package
// import SignIn from "../SignIn" //import your signIn page
// import SignUp from "./Components/SignUp/Form" //import your signUp page
import './App.css';
// import Form from './Form';
import SignIn from './Components/LoginPage/LoginForm';
import SignUp from './Components/SignUp/Form';
import OTP from './Components/OtpPage/OtpForm';
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        {/* <Form /> */}
        <Routes>
          <Route path="/" element={<SignIn/>} />
          <Route path="/SignUp" element={<SignUp/>} />
          <Route path="/otp" element={<OTP/>} />
        </Routes>
      </BrowserRouter>
      
    </div>
  );
}

export default App;
