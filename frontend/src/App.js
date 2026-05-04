import React, { useState, useEffect } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Fetch data from the FastAPI backend
    const baseUrl = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000"; // Default to localhost if env var is missing

    fetch(`${baseUrl}/endpoint`) // Fetch from the proper backend URL (make sure /endpoint exists)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setMessage(data.message))
      .catch((err) => {
        console.error("Failed to fetch:", err);
        setMessage("Error: Unable to fetch data from backend. ssssssss"); // Set fallback message
      });
  }, []); // Empty dependency array ensures this runs once when the component loads

  return (
    <div>
      <h1>Frontend + Backend Inteddgration</h1>
      <p>Message from the backend: {message}</p>
    </div>
  );
}


export default App;
