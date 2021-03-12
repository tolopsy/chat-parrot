import React, {useState} from 'react';

const App = () => {
    const [valA, setValA] =  useState("");
    const [valB, setValB] = useState("");

    return (
        <div>
            <input value={valA} onChange={(e) => {
                setValA(e.target.value);
            }} />

            <input value={valB} onChange={(e) => {
                setValB(e.target.value);
            }} />

            <Result vA={valA} vB={valB} />
        </div>
    );
}

export default App;

const Result = (props) => {
    const [result, setResult] = useState("")
    return (
        <div>
            <h4>Result: {result}</h4>

            <button onClick={() => {
                var finalVal = parseFloat(props.vA) + parseFloat(props.vB);
                setResult(finalVal);
            }}>
                Calculate
            </button>
        </div>
    )
}