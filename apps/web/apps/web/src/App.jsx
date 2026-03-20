import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    setInput('');

    try {
      const { data } = await axios.post('http://localhost:8000/chat', { message: input });
      setMessages(prev => [...prev, { role: 'bot', text: data.response, title: data.title }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'error', text: "Failed to connect to Professor." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#1e1e1e', color: '#d4d4d4', minHeight: '100vh', padding: '40px', fontFamily: 'monospace' }}>
      <header style={{ borderBottom: '1px solid #333', marginBottom: '20px' }}>
        <h1 style={{ color: '#4ec9b0' }}>🎓 ScholarOS _</h1>
      </header>

      <main style={{ maxWidth: '900px', margin: '0 auto' }}>
        <div style={{ height: '60vh', overflowY: 'auto', marginBottom: '20px', border: '1px solid #333', padding: '20px' }}>
          {messages.map((m, i) => (
            <div key={i} style={{ marginBottom: '20px', borderLeft: m.role === 'user' ? '3px solid #569cd6' : '3px solid #ce9178', paddingLeft: '15px' }}>
              <div style={{ color: m.role === 'user' ? '#569cd6' : '#ce9178', fontWeight: 'bold' }}>
                {m.role === 'user' ? '> USER' : `> PROFESSOR [${m.title || 'LOG'}]`}
              </div>
              <p style={{ lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>{m.text}</p>
            </div>
          ))}
          {loading && <div style={{ color: '#608b4e' }}>📡 Researching ArXiv... [WAITING]</div>}
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <span style={{ color: '#4ec9b0', alignSelf: 'center' }}>$</span>
          <input 
            style={{ flex: 1, background: '#252526', border: '1px solid #333', color: 'white', padding: '10px', outline: 'none' }}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask your research question..."
          />
          <button onClick={sendMessage} style={{ background: '#333', color: 'white', border: 'none', padding: '0 20px', cursor: 'pointer' }}>EXECUTE</button>
        </div>
      </main>
    </div>
  );
}

export default App;