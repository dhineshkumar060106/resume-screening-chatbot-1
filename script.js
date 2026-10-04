// script.js - Fixed to prevent auto-execution
console.log("🚀 script.js loading...");

// Auto-detect backend URL
const BACKEND_URL = 'http://127.0.0.1:5000';
console.log("🌐 Backend URL set to:", BACKEND_URL);

// Application state with safety flags
const AppState = {
    currentResume: null,
    analysisResult: null,
    currentController: null,
    isAnalyzing: false,
    isChatProcessing: false
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ DOM ready, initializing...");
    initializeApp();
});

function initializeApp() {
    // Setup all event listeners
    setupEventListeners();
    
    // Test backend connection
    testBackendConnection();
    
    console.log("✅ App initialized - waiting for user input");
}

function setupEventListeners() {
    console.log("🔧 Setting up event listeners...");
    
    // File upload
    setupFileUpload();
    
    // Job description counter
    setupJobDescCounter();
    
    // Analyze button - SAFE VERSION
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (AppState.isAnalyzing) {
                console.log("⚠ Already analyzing, ignoring click");
                return;
            }
            
            console.log("✅ Analyze button clicked manually by user");
            uploadResume();
        });
        
        // Remove any accidental double-click handlers
        analyzeBtn.onclick = null;
    }
    
    // Chat button
    const sendChatBtn = document.getElementById('sendChatBtn');
    if (sendChatBtn) {
        sendChatBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (!AppState.isChatProcessing) {
                askChatbot();
            }
        });
    }
    
    // Chat input enter key
    const chatInput = document.getElementById('chatQuestion');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !AppState.isChatProcessing) {
                e.preventDefault();
                askChatbot();
            }
        });
    }
    
    // Quick buttons
    ['quickBtn1', 'quickBtn2', 'quickBtn3'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
            btn.addEventListener('click', function() {
                const question = this.getAttribute('data-question');
                if (chatInput) {
                    chatInput.value = question;
                    chatInput.focus();
                }
            });
        }
    });
    
    // Footer buttons
    const helpBtn = document.getElementById('helpBtn');
    if (helpBtn) helpBtn.addEventListener('click', showHelp);
    
    const demoBtn = document.getElementById('demoBtn');
    if (demoBtn) demoBtn.addEventListener('click', showDemo);
    
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) resetBtn.addEventListener('click', resetApp);
    
    const saveReportBtn = document.getElementById('saveReportBtn');
    if (saveReportBtn) saveReportBtn.addEventListener('click', saveReport);
    
    const shareReportBtn = document.getElementById('shareReportBtn');
    if (shareReportBtn) shareReportBtn.addEventListener('click', shareReport);
    
    const printBtn = document.getElementById('printBtn');
    if (printBtn) printBtn.addEventListener('click', () => window.print());
    
    // Cancel button
    const cancelBtn = document.getElementById('cancelAnalysisBtn');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', cancelAnalysis);
    }
    
    console.log("✅ Event listeners setup complete");
}

function setupFileUpload() {
    const fileInput = document.getElementById('resumeFile');
    const dropZone = document.getElementById('dropZone');
    
    if (!fileInput || !dropZone) {
        console.error("❌ File upload elements not found");
        return;
    }
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    });
    
    // Drag and drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.style.borderColor = '#1F4ED8';
        dropZone.style.backgroundColor = '#E8EEFF';
    });
    
    dropZone.addEventListener('dragleave', function() {
        dropZone.style.borderColor = '#5B8CFF';
        dropZone.style.backgroundColor = '#F4F6FB';
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.style.borderColor = '#5B8CFF';
        dropZone.style.backgroundColor = '#F4F6FB';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileSelect(file);
            fileInput.files = e.dataTransfer.files;
        } else {
            alert('Please drop a PDF file only.');
        }
    });
    
    // Click drop zone to trigger file input
    dropZone.addEventListener('click', function(e) {
        if (e.target !== fileInput) {
            fileInput.click();
        }
    });
}

function handleFileSelect(file) {
    console.log("📁 File selected:", file.name);
    
    if (file.type !== 'application/pdf') {
        alert('❌ Please upload a PDF file only.');
        return;
    }
    
    AppState.currentResume = file;
    
    // Update UI
    const dropZone = document.getElementById('dropZone');
    dropZone.innerHTML = `
        <i class="fas fa-check-circle upload-icon" style="color: #4CAF50;"></i>
        <p class="upload-text">${file.name}</p>
        <p class="file-info">${(file.size / 1024).toFixed(1)} KB • Ready to analyze</p>
        <input type="file" id="resumeFile" accept=".pdf" class="file-input">
    `;
    
    // Re-attach event listener
    document.getElementById('resumeFile').addEventListener('change', function(e) {
        const newFile = e.target.files[0];
        if (newFile) handleFileSelect(newFile);
    });
}

function setupJobDescCounter() {
    const textarea = document.getElementById('jobDesc');
    const charCount = document.getElementById('charCount');
    
    if (!textarea || !charCount) return;
    
    textarea.addEventListener('input', function() {
        charCount.textContent = this.value.length;
    });
}

async function uploadResume() {
    console.log("📤 uploadResume called - checking conditions...");
    
    // Safety check - prevent multiple executions
    if (AppState.isAnalyzing) {
        console.log("⚠ Already analyzing, ignoring request");
        return;
    }
    
    // Validation
    if (!AppState.currentResume) {
        alert("❌ Please upload a resume PDF first.");
        return;
    }
    
    const jobDesc = document.getElementById('jobDesc').value.trim();
    if (!jobDesc) {
        alert("❌ Please enter a job description.");
        return;
    }
    
    if (jobDesc.length < 50) {
        alert("⚠ Please provide a more detailed job description (at least 50 characters).");
        return;
    }
    
    // Set analyzing flag
    AppState.isAnalyzing = true;
    
    // Show loading
    showLoading("Analyzing resume...");
    
    // Create form data
    const formData = new FormData();
    formData.append('resume', AppState.currentResume);
    formData.append('job_description', jobDesc);
    
    // Create abort controller for timeout
    AppState.currentController = new AbortController();
    const timeoutId = setTimeout(() => {
        if (AppState.currentController) {
            AppState.currentController.abort();
        }
    }, 60000); // 60 second timeout
    
    try {
        console.log("🔗 Sending request to:", `${BACKEND_URL}/api/upload`);
        
        const response = await fetch(`${BACKEND_URL}/api/upload`, {
            method: 'POST',
            body: formData,
            signal: AppState.currentController.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log("📥 Response status:", response.status);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("✅ Success! Data:", data);
        
        // Store and render results
        AppState.analysisResult = data;
        renderAnalysis(data);
        
    } catch (error) {
        console.error("❌ Upload failed:", error);
        
        if (error.name === 'AbortError') {
            alert("⏰ Request timed out. Please try again.");
        } else {
            alert(`❌ Analysis failed: ${error.message}\n\nUsing demo data instead.`);
            // Load demo data as fallback
            showDemoData();
        }
        
    } finally {
        // Reset analyzing flag
        AppState.isAnalyzing = false;
        hideLoading();
        AppState.currentController = null;
    }
}

function cancelAnalysis() {
    console.log("🛑 Cancelling analysis...");
    
    if (AppState.currentController) {
        AppState.currentController.abort();
        console.log("✅ Analysis cancelled");
    }
    
    AppState.isAnalyzing = false;
    hideLoading();
    
    // Reset button state
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-chart-line"></i> Analyze Resume Match';
    }
}

// ... rest of your existing functions (renderAnalysis, showDemoData, askChatbot, etc.) ...

// Override the global functions
window.uploadResume = uploadResume;
window.cancelAnalysis = cancelAnalysis;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.isAnalyzing = false; // Reset global flag

console.log("✅ script.js loaded successfully - SAFE MODE");