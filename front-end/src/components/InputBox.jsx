import { useState } from "react";

function InputBox({ onSend }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <div className="flex p-4 w-full max-w-3xl bg-white shadow-xl">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Ask me something..."
        className="flex-grow p-3 rounded-l-xl border border-gray-300"
      />
      <button
        onClick={handleSend}
        className="bg-indigo-600 text-white px-6 py-3 rounded-r-xl hover:bg-indigo-700"
      >
        Send
      </button>
    </div>
  );
}
export default InputBox;
