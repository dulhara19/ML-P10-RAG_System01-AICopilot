import { useState } from "react";



import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";
import MessegeBubble from "../components/MessageBubble";

function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi! I'm your University Copilot 🤖. Ask me anything!" }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async (userInput) => {
    const userMsg = { role: "user", text: userInput };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", text: data.response }]);
    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "⚠️ I'm offline right now. Here's a fallback answer." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    
    
    <div className="flex flex-col h-screen items-center justify-center">
      <Header />
      <ChatWindow messages={messages} isTyping={isTyping} />
      <InputBox onSend={sendMessage} />
    </div>
  );
}
export default ChatPage;
