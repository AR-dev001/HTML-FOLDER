import React, { useRef, useState } from "react";
function App() {
  const input1Ref = useRef();
  const input2Ref = useRef();
  const [result, setResult] = useState(null);
  const handleMultiply = () => {
    const num1 = parseFloat(input1Ref.current.value);
    const num2 = parseFloat(input2Ref.current.value);
    if (!isNaN(num1) && !isNaN(num2)) {
      setResult(num1 * num2);
    } else {
      setResult("Invalid input");
    }
  };
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Multiplication App</h1>
      <div>
        <label>Operand 1:</label>
        <input type="number" ref={input1Ref} placeholder="Enter first number" />
      </div>
      <div>
        <label>Operand 2:</label>
        <input type="number" ref={input2Ref} placeholder="Enter second number" />
      </div>
      <button onClick={handleMultiply}>Multiply</button>
      {result !== null && (
        <div>
          <h3>Result: {result}</h3>
        </div>
      )}
    </div>
  );
}
export default App;
