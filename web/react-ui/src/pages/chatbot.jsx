import React, { useState, useEffect, useRef } from "react";
import API from "../app/api";
import ReactMarkdown from "react-markdown";
import { Send, Sparkles, Brain, Activity, Zap, Home, Trash2 } from "lucide-react";

const Chatbot = () => {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, isTyping]);

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const send = async () => {
    if (!msg.trim()) return;

    const userMessage = msg;
    setMsg("");
    setChat([...chat, { user: userMessage, bot: null, timestamp: new Date() }]);
    setIsTyping(true);
    setLoading(true);

    try {
      const res = await API.post("/ai/chat", {
        message: userMessage,
        user_id: "frontend_user",
      });

      const botReply = res.data?.response?.reply || res.data?.reply || "No response from AI";

      setChat(prev => [...prev.slice(0, -1), { 
        user: userMessage, 
        bot: botReply,
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error("Chatbot error:", error);
      setChat(prev => [...prev.slice(0, -1), { 
        user: userMessage, 
        bot: "❌ Error connecting to AI. Please check if backend is running.",
        timestamp: new Date()
      }]);
    } finally {
      setIsTyping(false);
      setLoading(false);
    }
  };

  const clearChat = () => setChat([]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      e.preventDefault();
      send();
    }
  };

  const suggestedQuestions = [
    "What should I eat for breakfast?",
    "How can I lose weight safely?",
    "Best exercises for beginners?",
    "High protein foods list"
  ];

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
      
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div 
          className="absolute w-96 h-96 bg-purple-500/30 rounded-full blur-3xl animate-pulse"
          style={{ top: '10%', left: '10%', transform: `translate(${mousePos.x}px, ${mousePos.y}px)` }}
        />
        <div 
          className="absolute w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse"
          style={{ top: '60%', right: '10%', transform: `translate(${-mousePos.x}px, ${-mousePos.y}px)`, animationDelay: '1s' }}
        />
        <div 
          className="absolute w-96 h-96 bg-pink-500/30 rounded-full blur-3xl animate-pulse"
          style={{ bottom: '10%', left: '50%', transform: `translate(${mousePos.y}px, ${mousePos.x}px)`, animationDelay: '2s' }}
        />
        <div className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }}
        />
      </div>

      {/* Floating particles */}
      <div className="fixed inset-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-white/20 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `float ${5 + Math.random() * 10}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 5}s`
            }}
          />
        ))}
      </div>

      <div className="relative z-10 h-screen flex flex-col">
        {/* Header */}
        <div className="backdrop-blur-xl bg-white/5 border-b border-white/10 px-6 py-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-purple-500/50 animate-pulse">
                  <Brain className="w-8 h-8 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-900 animate-pulse" />
              </div>
              <div>
                <h1 className="text-2xl font-black bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                  AI Health Assistant
                </h1>
                <p className="text-sm text-gray-400 flex items-center gap-2">
                  <Activity className="w-3 h-3 animate-pulse text-green-400" />
                  Online & Ready to Help
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={clearChat} className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all group" title="Clear Chat">
                <Trash2 className="w-5 h-5 group-hover:text-red-400" />
              </button>
              <button
                onClick={() => window.history.back()}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105 transition-all shadow-lg flex items-center gap-2 font-bold"
              >
                <Home className="w-5 h-5" />
                Dashboard
              </button>
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          <div className="max-w-4xl mx-auto space-y-6">
            
            {/* Welcome Screen */}
            {chat.length === 0 && (
              <div className="text-center space-y-8 py-12">
                <div className="relative inline-block">
                  <div className="w-32 h-32 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-full flex items-center justify-center shadow-2xl animate-bounce">
                    <Sparkles className="w-16 h-16 text-white" />
                  </div>
                </div>
                <div>
                  <h2 className="text-4xl font-black mb-3 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                    Welcome to AI Health Chat
                  </h2>
                  <p className="text-xl text-gray-400">
                    Powered by Gemini AI - Your 24/7 intelligent health companion
                  </p>
                </div>
                
                {/* Suggested Questions */}
                <div className="grid md:grid-cols-2 gap-4 mt-8">
                  {suggestedQuestions.map((q, i) => (
                    <button
                      key={i}
                      onClick={() => setMsg(q)}
                      className="p-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:scale-105 transition-all text-left group"
                    >
                      <div className="flex items-start gap-3">
                        <Zap className="w-5 h-5 text-yellow-400 mt-1 group-hover:animate-pulse" />
                        <span className="text-gray-300">{q}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Chat Messages */}
            {chat.map((c, i) => (
              <div key={i} className="space-y-4">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="max-w-[70%]">
                    <div className="flex items-end gap-2 justify-end mb-1">
                      <span className="text-xs text-gray-500">
                        {c.timestamp?.toLocaleTimeString()}
                      </span>
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-xs font-bold">
                        You
                      </div>
                    </div>
                    <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-3xl rounded-tr-sm p-4 shadow-2xl shadow-blue-500/30">
                      <p className="text-white">{c.user}</p>
                    </div>
                  </div>
                </div>

                {/* Bot Message with Markdown Rendering */}
                {c.bot && (
                  <div className="flex justify-start">
                    <div className="max-w-[70%]">
                      <div className="flex items-end gap-2 mb-1">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/50">
                          <Brain className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-xs text-gray-500">AI Assistant</span>
                      </div>
                      <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-purple-500/30 rounded-3xl rounded-tl-sm p-4 shadow-2xl shadow-purple-500/20">
                        {/* ✅ MARKDOWN RENDERING HERE */}
                        <div className="prose prose-invert prose-sm max-w-none">
                          <ReactMarkdown
                            components={{
                              // Custom styles for markdown elements
                              p: ({node, ...props}) => <p className="text-gray-100 leading-relaxed mb-3" {...props} />,
                              strong: ({node, ...props}) => <strong className="text-white font-bold" {...props} />,
                              ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-2 my-3" {...props} />,
                              ol: ({node, ...props}) => <ol className="list-decimal list-inside space-y-2 my-3" {...props} />,
                              li: ({node, ...props}) => <li className="text-gray-100" {...props} />,
                              h1: ({node, ...props}) => <h1 className="text-xl font-bold text-white mb-3" {...props} />,
                              h2: ({node, ...props}) => <h2 className="text-lg font-bold text-white mb-2" {...props} />,
                              h3: ({node, ...props}) => <h3 className="text-base font-bold text-white mb-2" {...props} />,
                              code: ({node, inline, ...props}) => 
                                inline ? 
                                <code className="bg-slate-700 px-1.5 py-0.5 rounded text-green-400" {...props} /> :
                                <code className="block bg-slate-700 p-3 rounded my-2 text-green-400" {...props} />,
                              blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-purple-500 pl-4 italic my-3" {...props} />
                            }}
                          >
                            {c.bot}
                          </ReactMarkdown>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start">
                <div className="flex items-end gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/50 animate-pulse">
                    <Brain className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-slate-800 border border-purple-500/30 rounded-3xl rounded-tl-sm p-4 shadow-xl">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="backdrop-blur-xl bg-white/5 border-t border-white/10 px-6 py-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <textarea
                className="flex-1 p-4 rounded-2xl bg-slate-800/50 border-2 border-purple-500/30 focus:border-purple-500 outline-none text-white placeholder-gray-500 resize-none backdrop-blur-sm"
                placeholder="Ask anything about health, diet, or fitness..."
                value={msg}
                onChange={(e) => setMsg(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                rows="2"
              />
              <button
                onClick={send}
                disabled={loading || !msg.trim()}
                className="px-8 rounded-2xl bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-2xl shadow-purple-500/50 flex items-center justify-center gap-2 font-bold"
              >
                {loading ? (
                  <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <span className="hidden sm:inline">Send</span>
                    <Send className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
            <div className="mt-3 flex items-center justify-center gap-4 text-xs text-gray-500">
              <span>Press Enter to send</span>
              <span>•</span>
              <span>Powered by Gemini AI</span>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </div>
  );
};

export default Chatbot;