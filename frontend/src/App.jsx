import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_REACT_APP_API_URL;

function App() {
  const [ingestUrl, setIngestUrl] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleIngest = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const urls = ingestUrl.split(',').map(url => url.trim());
      await axios.post(`${API_URL}/api/ingest`, { urls });
      alert('Documents ingested successfully!');
    } catch (err) {
      setError('Failed to ingest documents.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await axios.post(`${API_URL}/api/query`, { query });
      setResponse(res.data);
    } catch (err) {
      setError('Failed to get a response from the agent.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Math Agentic-RAG System</h1>
      </header>
      <main>
        <section className="ingestion-section">
          <h2>Ingest Documents</h2>
          <form onSubmit={handleIngest}>
            <input
              type="text"
              value={ingestUrl}
              onChange={(e) => setIngestUrl(e.target.value)}
              placeholder="Enter comma-separated PDF URLs"
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Ingesting...' : 'Ingest'}
            </button>
          </form>
        </section>

        <hr />

        <section className="query-section">
          <h2>Ask a Question</h2>
          <form onSubmit={handleQuery}>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., How much payout for a 46-year-old male with a 3-month-old policy?"
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Thinking...' : 'Get Decision'}
            </button>
          </form>
        </section>

        <hr />
        
        <section className="response-section">
          <h2>Agent Response</h2>
          {loading && <p>Loading...</p>}
          {error && <p className="error">{error}</p>}
          {response && (
            <div className="response-container">
              <h3>Decision: {response.decision}</h3>
              <p><strong>Amount:</strong> {response.amount !== null ? `$${response.amount.toFixed(2)}` : 'N/A'}</p>
              <p><strong>Justification:</strong> {response.justification}</p>
              <p><strong>Clauses Used:</strong></p>
              <ul>
                {response.clauses_used.map((clause, index) => (
                  <li key={index}>{clause}</li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
