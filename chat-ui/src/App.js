import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [dark, setDark] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [messages]);

  useEffect(() => {
    document.body.className = dark ? "dark" : "";
  }, [dark]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { from: "user", text: input }]);
    setInput("");
    try {
      const backendUrl = process.env.CHAT_SERVER_URL || "http://localhost:8000";
      const res = await fetch(backendUrl + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();
      setMessages((msgs) => [...msgs, { from: "bot", text: data.answer }]);
    } catch {
      setMessages((msgs) => [
        ...msgs,
        { from: "bot", text: "Error de conexión con el servidor." },
      ]);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <span>💻 Computer Comparison Chat</span>
        <button
          className="theme-toggle"
          onClick={() => setDark((d) => !d)}
          title={dark ? "Modo claro" : "Modo oscuro"}
        >
          {dark ? "🌙" : "☀️"}
        </button>
      </div>
      <div className="chatBox" ref={chatRef}>
        {messages.length === 0 && (
          <div style={{ color: "#aaa", textAlign: "center", marginTop: 40 }}>
            Hello! Ask me about computers and I'll help you compare them.
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className="messageRow"
            style={{
              justifyContent: msg.from === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div className={msg.from === "user" ? "userMsg" : "botMsg"}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div className="inputArea">
        <input
          className="input"
          value={input}
          placeholder="Type your message..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="button" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;