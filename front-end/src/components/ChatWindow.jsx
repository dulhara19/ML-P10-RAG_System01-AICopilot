function ChatWindow({ messages, isTyping }) {
  return (
    <div className="flex flex-col gap-2 overflow-y-auto w-full max-w-3xl p-4 h-[70vh] bg-white shadow-lg rounded-lg">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`p-3 rounded-xl max-w-[75%] ${msg.role === "user" ? "ml-auto bg-blue-200" : "mr-auto bg-gray-100"}`}
        >
          {msg.text}
        </div>
      ))}
      {isTyping && (
        <div className="mr-auto p-3 bg-gray-200 rounded-xl animate-pulse">
          University Copilot is typing...
        </div>
      )}
    </div>
  );
}
export default ChatWindow;
