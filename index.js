import React from 'react';
import { createRoot } from 'react-dom/client';
class MyStyling extends React.Component{
  render(){
    const myheader={
      color:"green",
      backgroundColor:"black"
    };
    const mystyle={
      color:"blue",
      backgroundColor:"yellow"
    };
    return(
      <div>
        <h1 style={myheader}>Hello</h1>
        <p style={mystyle}>Hi</p>
      </div>
    );
  }
}
const container=document.getElementById("root");
const root=createRoot(container);
root.render(<MyStyling/>);
