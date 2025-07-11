import { useEffect, useRef, useState } from "react";
import bgVideo from "./assets/bg.mp4";

function App() {
  const [messages, setMessages] = useState([]);
  // console.log("messages", messages);
  const [input, setInput] = useState("");
  // console.log("inpp", input);
  const messagesEndRef = useRef(null);
  const [hasStarted, setHasStarted] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom(); // scroll every time messages update
  }, [messages]);

  const getGreeting = async () => {
    const res = await fetch("https://jarvis-0n4q.onrender.com/api/start", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });
    const data = await res.json();
    setMessages([...messages, { user: null, bot: data.response }]);
    setInput("");

    speak(data.response);
  };

  const sendMessage = async () => {
    const res = await fetch("https://jarvis-0n4q.onrender.com/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
      credentials: "include",
    });

    const data = await res.json();
    setMessages([...messages, { user: input, bot: data.response }]);
    setInput("");

    speak(data.response);

    if (data.response.trim() === "Goodbye 👋") {
      setTimeout(() => {
        window.location.reload();
      }, 3000);
      return; // ✅ Stop further execution
    }
  };

  // useEffect(() => {
  //   if (input.toLowerCase() === "exit") {
  //     setHasStarted(false);
  //   }
  // }, [input]);

  // const speak = (text) => {
  //   const utterance = new SpeechSynthesisUtterance(text);
  //   utterance.lang = "en-GB"; // Optional: adjust language/accent

  //   utterance.onstart = () => setIsSpeaking(true);
  //   utterance.onend = () => setIsSpeaking(false);
  //   utterance.onerror = () => setIsSpeaking(false);
  //   window.speechSynthesis.speak(utterance);
  // };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();

    // Find the specific voice by name
    const selectedVoice = voices.find(
      (voice) => voice.name === "Google UK English Male"
    );

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    } else {
      // Fallback
      utterance.lang = "en-US";
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    // console.log("voiceee", speechSynthesis.getVoices());
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    window.speechSynthesis.getVoices(); // Preload voices
  }, []);

  const startChat = () => {
    setHasStarted(true);
    getGreeting();
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <video
        src={bgVideo}
        autoPlay
        loop
        muted
        playsInline
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
      <div className="absolute top-1/12 left-1/4 w-1/2 h-3/4">
        {!hasStarted ? (
          <div className="flex justify-center items-center h-full">
            <button
              onClick={startChat}
              className="bg-black text-green-600 font-mono px-4 py-3 h-fit rounded-2xl shadow-[0_0_15px_3px_rgba(34,197,94,0.8)] hover:shadow-[0_0_25px_5px_rgba(34,197,94,1)] transition"
            >
              Start Jarvis
            </button>
          </div>
        ) : (
          <div className="flex flex-col gap-10 justify-between p-10 w-full h-full">
            <div
              style={{ whiteSpace: "pre-wrap", fontFamily: "monospace" }}
              className="bg-black/10 backdrop-blur-md rounded-lg border border-white/20 h-3/2 py-5 pl-5 overflow-y-scroll customScroll"
            >
              {messages.map((m, i) => (
                <div key={i} className="text-white flex flex-col gap-10">
                  {m.user && (
                    <div className="flex justify-end">
                      <div className="bg-blue-600 text-white text-base px-4 py-2 rounded-lg max-w-[75%] text-right">
                        <strong clas>You:</strong> {m.user}
                      </div>
                    </div>
                  )}
                  <div className="flex justify-start">
                    <div className="bg-black text-green-600 text-base px-4 py-2 rounded-lg max-w-[75%]">
                      <strong>Jarvis:</strong> {m.bot}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
            <div className="flex w-full justify-between bg-black/10 backdrop-blur-md border border-white/20 rounded-lg p-5">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !isSpeaking) {
                    sendMessage();
                  }
                }}
                className="bg-black text-green-600 w-[85%] focus:outline-none py-1 px-5 rounded-2xl font-mono"
              />
              <button
                disabled={isSpeaking}
                onClick={sendMessage}
                className={`bg-black w-[10%] text-green-600 font-mono rounded-2xl transition-opacity duration-200 ${
                  isSpeaking
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:bg-gray-900 cursor-pointer"
                }`}
              >
                Ask
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
