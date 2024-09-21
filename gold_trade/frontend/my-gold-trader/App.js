import React from 'react';
import Register from './Register';
import Login from './Login';
import GoldPrice from './GoldPrice';
import Trade from './Trade';

function App() {
    return (
        <div>
            <h1>Gold Trading App</h1>
            <Register />
            <Login />
            <GoldPrice />
            <Trade />
        </div>
    );
}

export default App;
