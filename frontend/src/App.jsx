import React, { useState } from 'react';
import axios from 'axios';
import { Copy, Link, Wand2, Hash, Check, Share2, ExternalLink } from 'lucide-react';
import './App.css';

const API_BASE = window.location.origin.includes('localhost:5173')
  ? 'http://localhost:8000'
  : '/api';

function App() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [useCustomAlias, setUseCustomAlias] = useState(false);
  const [customAlias, setCustomAlias] = useState('');
  const [loading, setLoading] = useState(false);
  const [shortData, setShortData] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const shareUrl = async (url) => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Shortened URL',
          text: 'Check out this short link!',
          url: url,
        });
      } catch (err) {
        console.error('Error sharing:', err);
      }
    } else {
      // Fallback: Copy to clipboard if Share API isn't supported
      copyToClipboard(url);
      alert("Link copied to clipboard (Share not supported in this browser)");
    }
  };

  const shortenUrl = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setShortData(null);
    setCopied(false);

    try {
      const response = await axios.post(`${API_BASE}/shorten`, {
        original_url: originalUrl,
        custom_alias: useCustomAlias ? (customAlias || null) : null,
      });

      setShortData(response.data);
    } catch (err) {
      console.error(err);
      if (err.response) {
        setError(err.response.data.detail || "Something went wrong. Please check your URL.");
      } else {
        setError("Failed to connect to the backend server.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCustom = (e) => {
    setUseCustomAlias(e.target.checked);
    if (!e.target.checked) setCustomAlias('');
  };

  const copyToClipboard = (text) => {
    if (text) {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="card">
      <div className="header">
        <h1>Shorter.</h1>
        <p>Shorten your URLs in a snap</p>
      </div>

      <form onSubmit={shortenUrl}>
        <div className="form-group">
          <label><Link size={14} style={{ marginRight: 4 }} /> Long URL</label>
          <div className="input-container">
            <input
              type="url"
              placeholder="https://example.com/very-long-url"
              required
              value={originalUrl}
              onChange={(e) => setOriginalUrl(e.target.value)}
            />
          </div>
        </div>

        <div className="toggle-group" style={{ gap: '16px' }}>
          <label className="switch">
            <input
              type="checkbox"
              checked={useCustomAlias}
              onChange={handleToggleCustom}
            />
            <span className="slider round"></span>
          </label>
          <span className="toggle-label">
            Custom Alias
          </span>
        </div>

        {useCustomAlias && (
          <div className="form-group anim-fade-in">
            <label><Hash size={14} style={{ marginRight: 4 }} /> Custom Link (Alias or URL)</label>
            <div className="input-container">
              <input
                type="text"
                placeholder="e.g. yoursite.com/my-link or 'my-name'"
                value={customAlias}
                onChange={(e) => setCustomAlias(e.target.value)}
                required={useCustomAlias}
              />
            </div>
          </div>
        )}

        <button className="btn" type="submit" disabled={loading}>
          {loading ? (
            "Shortening..."
          ) : (
            <>
              <Wand2 size={18} /> Shorten URL
            </>
          )}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {shortData && (
        <div className="result-card">
          <label className="result-label">
            <Check size={12} style={{ marginRight: 4 }} />
            Test Link (Clickable)
          </label>
          <span className="result-url">
            <a href={shortData.short_url} target="_blank" rel="noreferrer">{shortData.short_url}</a>
          </span>

          {shortData.custom_domain_url && (
            <>
              <label className="result-label" style={{ marginTop: 12 }}>
                <Wand2 size={12} style={{ marginRight: 4 }} />
                Intended Custom Link
              </label>
              <span className="result-url" style={{ opacity: 0.7 }}>
                {shortData.custom_domain_url}
              </span>
            </>
          )}

          <div className="action-row">
            <button className="copy-btn" onClick={() => copyToClipboard(shortData.short_url)}>
              {copied ? (
                <>
                  <Check size={14} /> Copied!
                </>
              ) : (
                <>
                  <Copy size={14} /> Copy
                </>
              )}
            </button>

            <a href={shortData.short_url} target="_blank" rel="noreferrer" className="action-btn">
              <ExternalLink size={14} /> Visit
            </a>

            <button className="action-btn" onClick={() => shareUrl(shortData.short_url)}>
              <Share2 size={14} /> Share
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
