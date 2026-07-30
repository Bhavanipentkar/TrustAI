function InputBox({ value, onChange }) {
  return (
    <textarea
      value={value}
      onChange={(event) => onChange(event.target.value)}
      placeholder="Enter the text you want TrustAI to analyze..."
      style={styles.textarea}
    />
  );
}

const styles = {
  textarea: {
    width: "100%",
    minHeight: "140px",
    padding: "16px",
    fontSize: "16px",
    borderRadius: "12px",
    border: "1px solid #cbd5e1",
    resize: "vertical",
  },
};

export default InputBox;
