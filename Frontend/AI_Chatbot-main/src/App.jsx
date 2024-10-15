import { useState, useEffect, useRef } from "react";
import "./App.css";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [conversation]);

  async function generateAnswer(e) {
    e.preventDefault();
    setGeneratingAnswer(true);

    const newConversation = [
      ...conversation,
      { type: "question", text: question },
    ];
    setConversation(newConversation);
    setQuestion("");

    setConversation((prev) => [...prev, { type: "answer", text: "..." }]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/query", {
        prompt: question,
      });

      if (response.data.error) {
        console.error(response.data.error);
        setConversation((prev) =>
          prev.map((msg, i) =>
            i === prev.length - 1
              ? {
                  ...msg,
                  text: "Sorry - Something went wrong. Please try again!",
                }
              : msg
          )
        );

        // Send the prompt to Gemini API as a fallback
        const geminiResponse = await axios.post(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${
            import.meta.env.VITE_API_GENERATIVE_LANGUAGE_CLIENT
          }`,
          {
            contents: [{ parts: [{ text: question }] }],
          }
        );

        const answerText =
          geminiResponse["data"]["candidates"][0]["content"]["parts"][0][
            "text"
          ];
        setConversation((prev) =>
          prev.map((msg, i) =>
            i === prev.length - 1 ? { ...msg, text: answerText } : msg
          )
        );
      } else {
        // Handle the received JSON data
        const formattedData = response.data;

        // Extract and display the relevant data from the response
        const groundwaterData = formattedData.groundwater_data;
        const weatherData = formattedData.weather_data;

        let responseText = "";

        if (groundwaterData && weatherData) {
          responseText = `**Groundwater Data:**\n${JSON.stringify(
            groundwaterData,
            null,
            2
          )}\n\n**Weather Data:**\n${JSON.stringify(weatherData, null, 2)}`;
        } else if (groundwaterData) {
          responseText = `**Groundwater Data:**\n${JSON.stringify(
            groundwaterData,
            null,
            2
          )}`;
        } else if (weatherData) {
          responseText = `**Weather Data:**\n${JSON.stringify(
            weatherData,
            null,
            2
          )}`;
        } else {
          responseText = "Sorry, I couldn't find any data for your query.";
        }

        setConversation((prev) =>
          prev.map((msg, i) =>
            i === prev.length - 1 ? { ...msg, text: responseText } : msg
          )
        );
      }
    } catch (error) {
      console.error(error);
      setConversation((prev) =>
        prev.map((msg, i) =>
          i === prev.length - 1
            ? {
                ...msg,
                text: "Sorry - Something went wrong. Please try again!",
              }
            : msg
        )
      );
    } finally {
      setGeneratingAnswer(false);
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (question.trim() !== "") {
        generateAnswer(e);
      }
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-blue-100 h-screen flex flex-col justify-between">
      <div className="flex-grow overflow-y-auto p-4 mb-20">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`flex my-2 ${
              msg.type === "question" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-3xl shadow-md max-w-[70%] ${
                msg.type === "question"
                  ? "bg-gradient-to-r from-blue-500 to-blue-400 text-white animate-fade-in-right"
                  : "bg-gray-100 text-black animate-fade-in-left"
              }`}
            >
              <ReactMarkdown>{msg.text}</ReactMarkdown>

              {msg.text === "..." && (
                <div className="flex items-center justify-start">
                  <div className="spinner-border animate-spin inline-block w-4 h-4 border-4 rounded-full border-t-blue-400 border-blue-300"></div>
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <form
        onSubmit={generateAnswer}
        className="w-full bg-white py-3 mt-5 fixed bottom-0 left-0 flex items-center justify-center"
      >
        <textarea
          required
          className="border border-gray-300 rounded-full w-11/12 h-10 px-4 pt-1 transition-all duration-300 focus:border-blue-400 focus:shadow-lg"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
          rows={2}
        ></textarea>
        <button
          type="submit"
          className={`bg-blue-500 text-white p-3 rounded-full ml-3 hover:bg-blue-600 transition-all duration-300 ${
            generatingAnswer ? "opacity-50 cursor-not-allowed" : ""
          }`}
          disabled={generatingAnswer}
        >
          {generatingAnswer ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}

export default App;
