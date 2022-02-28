import {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

import FormSubmission from './components/FormSubmission'

import Header from './components/Header';

function App() {
  // const [customers, setCustomers] = useState([]);

  // useEffect(() => {
  //   const loadData = () => {
  //     fetch('http://localhost:8000/api/get')
  //     .then(response => response.json())
  //     .then(data => setCustomers(data))
  //   }
  //   loadData();
  // }, [])

  return (
    <div className='App'>
      <Header/>
      <FormSubmission/>
    </div>
    // <div className="App">
    //   <header className="App-header">
    //     {
    //       customers.map(
    //         customer =>(
    //           <h1 key={customer.id}> <img src={"data:image/jpeg;base64, "+customer.poster_b64} alt="" />{customer.title}</h1>
    //         )
    //       )
    //     }
        

    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>
    //       Edit <code>src/App.js</code> and save to reload.
    //     </p>
    //   </header>
    // </div>
  );
}

export default App;
