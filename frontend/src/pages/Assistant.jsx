import { useState, useRef, useEffect } from "react";
import { Send, Sparkles } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { chatbotRules } from "../mock/mockData";
import PulseDivider from "../components/common/PulseDivider";
import { sendChatMessage } from "../api/chatbotApi";

const SUGGESTIONS = ["I have a fever", "What does my CBC report mean?", "Headache for 2 days", "Book an appointment"];

function getReply(text) {
  const lower = text.toLowerCase();
  const match = chatbotRules.find((rule) => rule.keywords.some((kw) => lower.includes(kw)));
  if (match) return match.reply;
  return "I don't have specific guidance on that yet, but I'd recommend discussing it with your doctor directly. You can also search relevant reports or prescriptions from the sidebar.";
}

export default function Assistant() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([
    { from: "bot", text: `Hi ${user?.name?.split(" ")[0]}, I'm the MediCore Assistant. Ask me about symptoms, reports, or how to use the portal. I'm not a substitute for medical advice.` },
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const send = async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    setMessages((prev) => [...prev, { from: "user", text: trimmed }]);
    setInput("");
    setTyping(true);
    try {
      const res = await sendChatMessage(trimmed);
      setMessages((prev) => [...prev, { from: "bot", text: res.data.reply }]);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setMessages((prev) => [...prev, { from: "bot", text: detail || "Sorry, I couldn't reach the assistant right now. Please try again." }]);
    } finally {
      setTyping(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    send(input);
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">{user?.role === "doctor" ? "Doctor Portal" : "Patient Portal"}</span>
        <h1>Assistant</h1>
        <p>Ask general health questions or get help navigating MediCore.</p>
      </div>
      <PulseDivider active />

      <div className="chat-wrap">
        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.from}`}>
              {m.from === "bot" && (
                <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4, fontSize: 11, fontWeight: 700, color: "var(--primary)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  <Sparkles size={12} /> Assistant
                </div>
              )}
              {m.text}
            </div>
          ))}
          {typing && (
            <div className="chat-bubble bot" style={{ color: "var(--ink-faint)" }}>typing…</div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-suggestions">
          {SUGGESTIONS.map((s) => (
            <button key={s} type="button" className="chat-suggestion-btn" onClick={() => send(s)}>
              {s}
            </button>
          ))}
        </div>

        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your symptom or ask a question…"
          />
          <button className="btn btn-primary" type="submit" disabled={!input.trim()}>
            <Send size={16} />
          </button>
        </form>
        <p className="chat-disclaimer">
          This assistant gives general information only and does not replace professional medical advice. In an emergency, contact emergency services directly.
        </p>
      </div>
    </div>
  );
}