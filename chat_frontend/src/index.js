import React from 'react';
import ReactDom from 'react-dom';
import App from './app';

ReactDom.render(<div>
    <h1>Hello Chat Parrot</h1>
    <h4>Frontend with React</h4>
    <App />
</div>, 
document.getElementById("root")
);