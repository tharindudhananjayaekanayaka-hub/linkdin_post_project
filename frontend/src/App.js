import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Send, Loader2, Share2, Sparkles, Terminal, 
  Image as ImageIcon, ExternalLink, Moon, Sun, Languages 
} from 'lucide-react';

function App() {
  const [topic, setTopic] = useState('');
  const [post, setPost] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('Sinhala'); // Default language
  const [darkMode, setDarkMode] = useState(true); // Default Dark Mode

  // Dark Mode Logic
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const generatePost = async () => {
    if (!topic) return alert("කරුණාකර මාතෘකාවක් ඇතුළත් කරන්න!");
    
    setLoading(true);
    setPost('');
    setImageUrl('');
    
    try {
      // Backend එකට topic එක සහ language එක යැවීම
      const response = await axios.post('http://127.0.0.1:8000/generate-post', { 
        topic: topic,
        language: language
      });
      
      if (response.data && response.data.status === "success") {
        setPost(response.data.post);
        setImageUrl(response.data.image_url);
      }
    } catch (error) {
      console.error("Error details:", error);
      alert("වැරදීමක් සිදු විය! Backend එක run වෙනවාදැයි පරීක්ෂා කරන්න.");
    }
    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(post);
    alert("Post එක copy කරගත්තා!");
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'} flex flex-col items-center p-6 md:p-12 font-sans`}>
      
      {/* Settings Bar (Dark Mode & Language) */}
      <div className="w-full max-w-2xl flex justify-between items-center mb-8">
        <button 
          onClick={() => setDarkMode(!darkMode)}
          className="p-3 rounded-2xl bg-white dark:bg-slate-800 shadow-md hover:scale-110 transition-all text-blue-600"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        <div className="flex bg-white dark:bg-slate-800 p-1.5 rounded-2xl shadow-md border border-slate-200 dark:border-slate-700">
          <button 
            onClick={() => setLanguage('Sinhala')}
            className={`px-4 py-1.5 rounded-xl text-sm font-bold transition-all ${language === 'Sinhala' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-500'}`}
          >
            සිංහල
          </button>
          <button 
            onClick={() => setLanguage('English')}
            className={`px-4 py-1.5 rounded-xl text-sm font-bold transition-all ${language === 'English' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-500'}`}
          >
            English
          </button>
        </div>
      </div>

      {/* Header Section */}
      <header className="mb-10 text-center">
        <div className="inline-flex items-center justify-center p-3 bg-blue-100 dark:bg-blue-900/30 rounded-2xl text-blue-600 mb-4 animate-bounce">
          <Sparkles size={32} />
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight">
          LinkedIn <span className="text-blue-600">AI Factory</span>
        </h1>
        <p className="text-slate-500 dark:text-slate-400 mt-2 text-lg italic">
          {language === 'Sinhala' ? 'AI Agents මගින් ඔබේ පෝස්ට් එක විනාඩියෙන්' : 'Power your LinkedIn with AI Agents'}
        </p>
      </header>

      {/* Main Input Card */}
      <main className="w-full max-w-2xl bg-white dark:bg-slate-900 rounded-3xl shadow-2xl p-8 border border-slate-200 dark:border-slate-800 transition-all">
        <div className="flex flex-col gap-5">
          <div>
            <label className="block text-sm font-semibold mb-2 ml-1 opacity-80">
              {language === 'Sinhala' ? 'මාතෘකාව ඇතුළත් කරන්න' : 'What is the topic?'}
            </label>
            <input 
              type="text" 
              placeholder={language === 'Sinhala' ? "උදා: AI වල අනාගතය..." : "e.g. Future of Generative AI..."}
              className="w-full p-4 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-lg"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          
          <button 
            onClick={generatePost}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-2xl flex items-center justify-center gap-3 shadow-lg shadow-blue-400/20 transition-all active:scale-95 disabled:opacity-70"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" />
                {language === 'Sinhala' ? 'Agents වැඩ කරමින් පවතී...' : 'Agents are thinking...'}
              </>
            ) : (
              <>
                <Terminal size={20} />
                {language === 'Sinhala' ? 'පෝස්ට් එක සාදන්න' : 'Generate Post'}
              </>
            )}
          </button>
        </div>

        {/* Result Area */}
        {(post || imageUrl) && (
          <div className="mt-10 space-y-8 animate-in fade-in slide-in-from-bottom-5 duration-700">
            
            {/* Post Text Section */}
            {post && (
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    {language === 'Sinhala' ? 'ඔබේ පෝස්ට් එක:' : 'Generated Post:'}
                  </h3>
                  <button 
                    onClick={copyToClipboard}
                    className="text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 px-3 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1.5 transition-colors border border-blue-100 dark:border-blue-900/50"
                  >
                    <Share2 size={16} /> Copy
                  </button>
                </div>
                <div className="bg-slate-900 rounded-2xl p-6 shadow-inner border border-slate-800">
                  <pre className="whitespace-pre-wrap text-slate-200 leading-relaxed font-mono text-sm">
                    {post}
                  </pre>
                </div>
              </div>
            )}

            {/* Image Section */}
            {imageUrl && (
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold flex items-center gap-2">
                    <ImageIcon size={18} className="text-blue-600" />
                    AI Image:
                  </h3>
                  <a 
                    href={imageUrl} 
                    target="_blank" 
                    rel="noreferrer"
                    className="text-slate-500 hover:text-blue-600 text-xs flex items-center gap-1 underline"
                  >
                    Download HD <ExternalLink size={12} />
                  </a>
                </div>
                <div className="overflow-hidden rounded-2xl border-4 border-white dark:border-slate-800 shadow-2xl bg-slate-200 dark:bg-slate-800">
                  <img 
                    src={imageUrl} 
                    alt="AI Visual" 
                    className="w-full h-auto object-cover hover:scale-[1.02] transition-transform duration-500"
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="mt-auto pt-10 text-slate-400 text-sm flex flex-col items-center gap-2">
        <p>Built with FastAPI, React & CrewAI</p>
        <div className="flex gap-4 opacity-50">
           <span className="h-1 w-1 bg-slate-400 rounded-full"></span>
           <span className="h-1 w-1 bg-slate-400 rounded-full"></span>
           <span className="h-1 w-1 bg-slate-400 rounded-full"></span>
        </div>
      </footer>
    </div>
  );
}

export default App;