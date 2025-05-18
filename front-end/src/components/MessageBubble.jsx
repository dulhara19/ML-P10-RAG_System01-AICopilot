function MessageBubble({ role, text, time }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div
        className={`
          max-w-[75%]
          px-4 py-3 rounded-xl
          ${isUser ? "bg-blue-500 text-white rounded-br-none" : "bg-gray-200 text-gray-800 rounded-bl-none"}
          shadow-md
          whitespace-pre-line
        `}
      >
        <p className="text-sm">{text}</p>
        {time && (
          <p className="text-[10px] mt-1 text-right text-gray-400">{time}</p>
        )}
      </div>
    </div>
  );
}

export default MessageBubble;
