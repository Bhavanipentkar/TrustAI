function ResultCard({ result }) {
  const { trust_score, verdict, summary, results } = result;

  const verdictColor = {
    Reliable: "#16a34a",
    Uncertain: "#d97706",
    Unreliable: "#dc2626",
  }[verdict] || "#2563eb";

  return (
    <div style={{ ...styles.card, borderColor: verdictColor }}>
      <div style={styles.topRow}>
        <div>
          <h2>Trust Score</h2>
          <p style={{ ...styles.score, color: verdictColor }}>{trust_score}</p>
          <p style={{ ...styles.verdict, color: verdictColor }}>{verdict}</p>
        </div>
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      </div>

      <div style={styles.claimSection}>
        <h3>Claim Analysis</h3>
        {results.length === 0 ? (
          <p>No claims were detected in the text.</p>
        ) : (
          results.map((item, index) => (
            <div key={index} style={styles.claimItem}>
              <p style={styles.claimText}>{item.claim}</p>
              <div style={styles.claimTags}>
                <span style={styles.tag}>Status: {item.status}</span>
                <span style={styles.tag}>Risk: {item.hallucination}</span>
              </div>
              <p>{item.explanation}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

const styles = {
  card: {
    marginTop: "24px",
    padding: "20px",
    borderRadius: "14px",
    border: "3px solid",
    backgroundColor: "#f8fafc",
  },
  topRow: {
    display: "flex",
    justifyContent: "space-between",
    gap: "24px",
    flexWrap: "wrap",
  },
  score: {
    fontSize: "48px",
    margin: "0",
  },
  verdict: {
    fontWeight: "700",
    marginTop: "4px",
  },
  claimSection: {
    marginTop: "20px",
  },
  claimItem: {
    backgroundColor: "#ffffff",
    padding: "14px",
    borderRadius: "12px",
    border: "1px solid #cbd5e1",
    marginBottom: "12px",
  },
  claimText: {
    fontWeight: "600",
    marginBottom: "8px",
  },
  claimTags: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
    marginBottom: "8px",
  },
  tag: {
    backgroundColor: "#e2e8f0",
    borderRadius: "9999px",
    padding: "6px 10px",
    fontSize: "14px",
  },
};

export default ResultCard;
