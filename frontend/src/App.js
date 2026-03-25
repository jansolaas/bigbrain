import React, { useState, useEffect } from "react";

console.log("Backend API:", process.env.REACT_APP_API_BASE_URL);

function App() {
  const [message, setMessage] = useState("");

  fetch(`${process.env.REACT_APP_API_BASE_URL}/endpoint`) // Ensure BASE_URL points to your FastAPI server
    .then((response) => response.json())
    .then((data) => console.log(data.message))
    .catch((err) => console.error("Error:", err));


  useEffect(() => {
    // Fetch data from the FastAPI backend
    fetch("http://127.0.0.1:8000/") // Make sure this URL matches your backend
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error("Failed to fetch:", err));
  }, []);

  return (
    <div>
      <h1>Frontend + Backends Integration</h1>
      <p>Message from the backend: {message}</p>
    </div>
  );
}

export default App;
