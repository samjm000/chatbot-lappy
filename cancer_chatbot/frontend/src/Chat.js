import React, { useState } from 'react';
import axios from 'axios';
import './Chat.css';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 60000, // 60 seconds
});

function Chat() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState("");

    const handleSend = async () => {
        const eventSource = new EventSource(`http://127.0.0.1:8000/chat/?prompt=${encodeURIComponent(input)}`);
        
        eventSource.onmessage = (event) => {
            const newMessage = JSON.parse(event.data).response;
            setCurrentMessage(prev => prev + newMessage);
        };

        eventSource.onerror = () => {
            console.error("Error receiving events");
            eventSource.close();
        };

        eventSource.onopen = () => {
            console.log("Connection opened");
        };

        eventSource.onend = () => {
            console.log("Connection ended");
            setMessages([...messages, { user: input, bot: currentMessage }]);
            setCurrentMessage("");
            setInput("");
            eventSource.close();
        };
    };

    return (
        <div className="chat-container">
            <div>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.user ? "user-message" : "bot-message"}`}>
                        <p><strong>You:</strong> {msg.user}</p>
                        <p><strong>Bot:</strong> {msg.bot}</p>
                    </div>
                ))}
                {currentMessage && (
                    <div className="message bot-message">
                        <p><strong>Bot:</strong> {currentMessage}</p>
                    </div>
                )}
            </div>
            <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="How can I help you today?..."
            />
            <button onClick={handleSend}>Send</button>
        </div>
    );
}

export default Chat;
