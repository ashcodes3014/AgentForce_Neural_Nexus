import { useState, useRef, useEffect } from 'react';
import {
  FileText,
  Mail,
  User,
  LogOut,
  Upload,
  History,
  Menu,
  X,
  ChevronRight,
} from 'lucide-react';
import { backend1Client } from './axiosClient';
import {useSelector} from "react-redux"
import {getAuth, signOut } from 'firebase/auth';
import {db} from './firebaseConfig'


const HomePage = () => {
  const [activeTab, setActiveTab] = useState('analyze');
  const [pdfFile, setPdfFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const userId = useSelector((state)=>state.slice1.userId)
  const [coverLetterHistory, setCoverLetterHistory] = useState([
    { id: 1, title: 'Software Engineer at Google', date: '2023-05-15' },
    { id: 2, title: 'Frontend Developer at Meta', date: '2023-04-22' },
    { id: 3, title: 'Full Stack Engineer at Netflix', date: '2023-03-10' },
  ]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const auth = getAuth();
  const [isGenerating, setIsGenerating] = useState(false);
  const [letterForm, setLetterForm] = useState({
    recipientName: '',
    recipientEmail: '',
    senderName: '',
    senderEmail: '',
    jobPosition: '',
    selectedHistoryId: '',
  });

  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
    } else {
      alert('Please upload a PDF file');
    }
  };

  const handleAnalyzeResume = async () => {
    setIsAnalyzing(true);
    setAnalysisResult(null);
    console.log(userId)
    const formData = new FormData();
    formData.append('file', pdfFile);
    formData.append('job_title', jobTitle);
    formData.append('user_id', jobTitle);
    formData.append('user_id', userId);

    const response = await backend1Client.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(response.data)
    setAnalysisResult(response.data) ;
};

  const handleAnalyzeAnother = () => {
    setPdfFile(null);
    setJobTitle('');
    setAnalysisResult(null);
    setIsAnalyzing(false);
  };

  const handleLetterFormChange = (e) => {
    const { name, value } = e.target;
    setLetterForm((prev) => ({ ...prev, [name]: value }));
  };

  const loggedOut = async () => {
    await signOut(auth);
    setIsLoggedIn(false);
  };

  useEffect(()=>{
    const getHistory = async () => {
    const docRef = doc(db, "users", userId);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      console.log("User Data:", docSnap.data());
      const data =  docSnap.data();
      console.log(data.history)
      setCoverLetterHistory(data.history)
    }

    getHistory();
  }
  },[])

  const handleGenerateLetter = () => {
    if (
      !letterForm.recipientName ||
      !letterForm.recipientEmail ||
      !letterForm.senderName ||
      !letterForm.senderEmail ||
      !letterForm.jobPosition ||
      !letterForm.selectedHistoryId
    ) {
      alert('Please fill in all fields and select a history item.');
      return;
    }

    setIsGenerating(true);

    setTimeout(() => {
      alert('Cover letter generated successfully!');
      setIsGenerating(false);
    }, 2500);
  };

  return (
    <div className="flex min-h-screen bg-gray-900 text-gray-100">
      {/* Sidebar */}
      <aside
        className={`flex flex-col bg-gray-800 border-r border-gray-700 transition-all duration-300 ease-in-out ${
          sidebarOpen ? 'w-64' : 'w-16'
        }`}
      >
        {/* Top header with toggle */}
        <div className="flex items-center justify-between h-20 border-b border-gray-700 px-4">
          {sidebarOpen && (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-blue-500 flex items-center justify-center">
                <span className="text-white font-bold text-xl">E</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent select-none">
                Elevatr
              </span>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen((open) => !open)}
            className="p-2 rounded-md hover:bg-gray-700 transition-colors"
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex flex-col mt-6 flex-grow px-1">
          {[
            { id: 'analyze', icon: <FileText size={20} />, label: 'Analyze Resume' },
            { id: 'getletter', icon: <Mail size={20} />, label: 'Generate Letter' },
            { id: 'history', icon: <History size={20} />, label: 'History' },
          ].map(({ id, icon, label }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center space-x-3 rounded-md px-3 py-3 my-1 mx-1 transition-colors ${
                activeTab === id
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 shadow-lg text-white'
                  : 'hover:bg-gray-700 text-gray-300'
              }`}
              title={!sidebarOpen ? label : undefined}
            >
              <span>{icon}</span>
              {sidebarOpen && <span className="font-semibold">{label}</span>}
            </button>
          ))}
        </nav>

        {/* User/Login controls pinned at bottom */}
        <div className="border-t border-gray-700 p-4 mt-auto flex flex-col space-y-3 sticky bottom-0 bg-gray-800 z-10">
          {isLoggedIn ? (
            <div className="flex flex-col space-y-2">
              <button
                className="flex items-center justify-center space-x-3 rounded-md px-3 py-3 hover:bg-gray-700 transition-colors text-gray-300"
                title={!sidebarOpen ? 'Profile' : undefined}
              >
                <User size={20} />
                {sidebarOpen && <span>Profile</span>}
              </button>
              <button
                className="flex items-center justify-center space-x-3 rounded-md px-3 py-3 text-red-500 transition-colors"
                onClick={() => loggedOut()}
                title={!sidebarOpen ? 'Logout' : undefined}
              >
                <LogOut size={20} />
                {sidebarOpen && <span>Logout</span>}
              </button>
            </div>
          ) : (
            <button
              onClick={() => setIsLoggedIn(true)}
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-md font-semibold hover:opacity-90 transition-opacity flex justify-center items-center"
              title={!sidebarOpen ? 'Profile' : undefined}
            >
              <User size={20} />
              {sidebarOpen && <span className="ml-2">User</span>}
            </button>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main
        className={`flex-1 p-8 overflow-auto transition-all duration-300 ease-in-out ${
          sidebarOpen ? 'ml-0' : 'ml-0'
        }`}
      >
        {/* Breadcrumb + Title */}
        <div className="flex items-center mb-8 space-x-3 text-gray-400 text-sm select-none">
          <span>Home</span>
          <ChevronRight size={14} />
          <span className="text-white font-semibold capitalize">{activeTab}</span>
        </div>

        {/* Content Panels */}
        {activeTab === 'analyze' && (
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Show loader only if analyzing and no result yet */}
            {isAnalyzing && !analysisResult ? (
              <div className="flex flex-col items-center justify-center p-12 bg-gray-800 rounded-xl border border-gray-700 shadow-md">
                <svg
                  className="animate-spin h-12 w-12 text-blue-400 mb-4"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8H4z"
                  ></path>
                </svg>
                <p className="text-gray-300 text-lg font-semibold">Analyzing your resume...</p>
              </div>
            ) : analysisResult ? (
              // Show analysis result & Analyze Another button
              <section className="bg-gray-800 rounded-xl border border-blue-500 p-6 shadow-lg">
                <h3 className="text-2xl font-semibold text-blue-400 mb-4">Analysis Result</h3>
                <p className="mb-5 font-bold text-lg">Score: {analysisResult.keyword_match_score}%</p>
                <h3 className="text-2xl font-semibold text-blue-400 mb-4">strengths</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-300 mb-6">
                  {analysisResult.suggestion.strengths.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
                <h3 className="text-2xl font-semibold text-blue-400 mb-4">areas_of_improvement</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-300 mb-6">
                  {analysisResult.suggestion.areas_of_improvement.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
                <button
                  onClick={handleAnalyzeAnother}
                  className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold hover:opacity-90 transition-opacity"
                >
                  Analyze Another
                </button>
              </section>
            ) : (
              // Show input form & analyze button if no analysis in progress/result
              <section className="bg-gray-800 rounded-xl border border-gray-700 p-8 shadow-md">
                <h2 className="text-3xl font-bold mb-6">Analyze Your Resume</h2>

                <div className="space-y-6">
                  <div>
                    <label className="block text-gray-300 mb-2 font-semibold">Job Title</label>
                    <input
                      type="text"
                      value={jobTitle}
                      onChange={(e) => setJobTitle(e.target.value)}
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g. Senior Frontend Developer"
                      disabled={isAnalyzing}
                    />
                  </div>

                  <div
                    className="bg-gray-900 border-2 border-dashed border-gray-600 rounded-lg p-12 text-center cursor-pointer hover:border-blue-500 transition-colors"
                    onClick={() => !isAnalyzing && fileInputRef.current.click()}
                  >
                    {pdfFile ? (
                      <div className="flex flex-col items-center space-y-3">
                        <FileText size={56} className="text-blue-400" />
                        <p className="text-gray-300 font-mono">{pdfFile.name}</p>
                        <button
                          className="px-5 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            setPdfFile(null);
                          }}
                          disabled={isAnalyzing}
                        >
                          Change File
                        </button>
                      </div>
                    ) : (
                      <>
                        <Upload size={56} className="mx-auto text-gray-500 mb-4" />
                        <p className="text-gray-400 mb-4">Upload your resume PDF</p>
                        <button
                          className="px-5 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                          disabled={isAnalyzing}
                        >
                          Select PDF
                        </button>
                      </>
                    )}
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={handleFileUpload}
                      accept="application/pdf"
                      className="hidden"
                      disabled={isAnalyzing}
                    />
                  </div>

                  <button
                    onClick={handleAnalyzeResume}
                    disabled={!pdfFile || !jobTitle || isAnalyzing}
                    className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 flex justify-center items-center space-x-3"
                  >
                    {isAnalyzing && (
                      <svg
                        className="animate-spin h-6 w-6 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8v8H4z"
                        ></path>
                      </svg>
                    )}
                    <span>{isAnalyzing ? 'Analyzing...' : 'Analyze Resume'}</span>
                  </button>
                </div>
              </section>
            )}
          </div>
        )}

        {activeTab === 'getletter' && (
          <div className="max-w-4xl mx-auto space-y-8">
            <section className="bg-gray-800 rounded-xl border border-gray-700 p-8 shadow-md">
              <h2 className="text-3xl font-bold mb-6">Generate Cover Letter</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-gray-300 mb-2 font-semibold">Recipient Name</label>
                  <input
                    type="text"
                    name="recipientName"
                    value={letterForm.recipientName}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g. John Doe"
                    disabled={isGenerating}
                  />
                </div>
                <div>
                  <label className="block text-gray-300 mb-2 font-semibold">Recipient Email</label>
                  <input
                    type="email"
                    name="recipientEmail"
                    value={letterForm.recipientEmail}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g. john.doe@example.com"
                    disabled={isGenerating}
                  />
                </div>
                <div>
                  <label className="block text-gray-300 mb-2 font-semibold">Sender Name</label>
                  <input
                    type="text"
                    name="senderName"
                    value={letterForm.senderName}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your Name"
                    disabled={isGenerating}
                  />
                </div>
                <div>
                  <label className="block text-gray-300 mb-2 font-semibold">Sender Email</label>
                  <input
                    type="email"
                    name="senderEmail"
                    value={letterForm.senderEmail}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="your.email@example.com"
                    disabled={isGenerating}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-gray-300 mb-2 font-semibold">Job Position</label>
                  <input
                    type="text"
                    name="jobPosition"
                    value={letterForm.jobPosition}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Job position for the cover letter"
                    disabled={isGenerating}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-gray-300 mb-2 font-semibold">Select History to Use</label>
                  <select
                    name="selectedHistoryId"
                    value={letterForm.selectedHistoryId}
                    onChange={handleLetterFormChange}
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={isGenerating}
                  >
                    <option value="">-- Select a cover letter history --</option>
                    {coverLetterHistory.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.title} ({item.date})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <button
                onClick={handleGenerateLetter}
                disabled={isGenerating}
                className="w-full mt-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 flex justify-center items-center space-x-3"
              >
                {isGenerating && (
                  <svg
                    className="animate-spin h-6 w-6 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v8H4z"
                    ></path>
                  </svg>
                )}
                <span>{isGenerating ? 'Generating...' : 'Generate Letter'}</span>
              </button>
            </section>

          </div>
        )}

        {activeTab === 'history' && (
          <section className="max-w-4xl mx-auto bg-gray-800 rounded-xl border border-gray-700 p-8 shadow-md">
            <h2 className="text-3xl font-bold mb-6">Your History</h2>

            {coverLetterHistory.length > 0 ? (
              <div className="divide-y divide-gray-700">
                {coverLetterHistory.map((item) => (
                  <div
                    key={item.id}
                    className="flex justify-between items-center py-4 hover:bg-gray-700 rounded-lg px-4 cursor-pointer transition-colors"
                  >
                    <div>
                      <h3 className="font-semibold text-lg">{item.title}</h3>
                      <p className="text-sm text-gray-400">{item.date}</p>
                    </div>
                    <button className="text-blue-400 hover:text-blue-300 font-semibold">View</button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16 text-gray-500">
                <History size={56} className="mx-auto mb-4" />
                No history available yet
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
};

export default HomePage;
