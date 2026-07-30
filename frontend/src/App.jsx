import { useState } from "react";
import InputBox from "./components/InputBox";
import ResultCard from "./components/ResultCard";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeText = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Failed to contact the TrustAI backend.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err?.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const canAnalyze = text.trim().length > 0 && !loading;

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1>TrustAI – AI Trust Score Engine</h1>
        <p>Paste text to analyze trustworthiness, hallucination risk, and claim accuracy.</p>

        <InputBox value={text} onChange={setText} />

        <button style={styles.button} onClick={analyzeText} disabled={!canAnalyze}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        {error && <p style={styles.error}>{error}</p>}
        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#f2f7ff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "24px",
  },
  card: {
    width: "100%",
    maxWidth: "760px",
    backgroundColor: "#ffffff",
    borderRadius: "16px",
    boxShadow: "0 20px 50px rgba(0,0,0,0.08)",
    padding: "32px",
  },
  button: {
    marginTop: "16px",
    padding: "12px 24px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    fontSize: "16px",
  },
  error: {
    marginTop: "16px",
    color: "#b91c1c",
  },
};

export default App;
