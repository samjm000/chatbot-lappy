import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/chat/', { question });
            setResponse(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
            <h1>AI Chatbot</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question..."
                    style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
                />
                <button type="submit" style={{ padding: '10px 20px' }}>Ask</button>
            </form>
            {response && (
                <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
                    <h2>Response:</h2>
                    {response.answers && response.answers.length > 0 ? (
                        <p>{response.answers[0].answer}</p>
                    ) : (
                        <p>No answer found.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Chatbot;
