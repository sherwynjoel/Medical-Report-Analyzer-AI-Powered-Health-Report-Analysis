// Medical Report Analyzer - Frontend JavaScript

const API_BASE_URL = window.location.origin;

// File upload handling
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        uploadAndAnalyze(file);
    }
});

// Drag and drop functionality
const uploadBox = document.getElementById('uploadBox');
uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#2563eb';
    uploadBox.style.background = '#f9fafb';
});

uploadBox.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#e5e7eb';
    uploadBox.style.background = '#f3f4f6';
});

uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#e5e7eb';
    uploadBox.style.background = '#f3f4f6';
    
    const file = e.dataTransfer.files[0];
    const allowedTypes = ['application/pdf', 'text/plain', 'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
    if (file && allowedTypes.includes(file.type)) {
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        uploadAndAnalyze(file);
    } else {
        showError('Please upload a PDF, TXT file, or Image (JPG, PNG, etc.)');
    }
});

// Upload and analyze file
async function uploadAndAnalyze(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults(data.analysis);
        } else {
            showError(data.error || 'Failed to analyze file');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

// Analyze text directly
async function analyzeText() {
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    
    if (text.length < 10) {
        showError('Please enter at least 10 characters of text');
        return;
    }
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults(data.analysis);
        } else {
            showError(data.error || 'Failed to analyze text');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

// Display analysis results
function displayResults(analysis) {
    if (analysis.error) {
        showError(analysis.error);
        return;
    }
    
    // Hide upload section and show results
    document.querySelector('.upload-section').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Update risk indicator
    const riskCircle = document.getElementById('riskCircle');
    const riskText = document.getElementById('riskText');
    const riskLabel = document.getElementById('riskLabel');
    
    riskCircle.className = `risk-circle ${analysis.risk_level}`;
    riskText.textContent = analysis.risk_level.charAt(0).toUpperCase() + analysis.risk_level.slice(1) + ' Risk';
    riskLabel.textContent = 'Overall Health Status';
    
    // Display summary
    document.getElementById('summaryText').textContent = analysis.summary || 'No summary available';
    if (analysis.analysis_date) {
        const date = new Date(analysis.analysis_date);
        document.getElementById('analysisDate').textContent = `Analyzed on: ${date.toLocaleString()}`;
    }
    
    // Display findings
    displayFindings(analysis.findings || {});
}

// Display findings in cards
function displayFindings(findings) {
    const findingsGrid = document.getElementById('findingsGrid');
    findingsGrid.innerHTML = '';
    
    if (Object.keys(findings).length === 0) {
        findingsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #6b7280;">No specific findings detected in the report.</p>';
        return;
    }
    
    for (const [condition, data] of Object.entries(findings)) {
        const card = document.createElement('div');
        card.className = `finding-card ${data.status}`;
        
        const conditionName = condition.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        card.innerHTML = `
            <h3>${conditionName}</h3>
            <div class="finding-value">${data.value}</div>
            <div class="finding-range">Normal Range: ${data.normal_range[0]} - ${data.normal_range[1]}</div>
            <span class="finding-status ${data.status}">${data.status.toUpperCase()}</span>
        `;
        
        findingsGrid.appendChild(card);
    }
}

// Reset analysis
function resetAnalysis() {
    document.querySelector('.upload-section').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('fileInput').value = '';
    document.getElementById('textInput').value = '';
    document.getElementById('fileName').textContent = '';
    hideError();
}

// Utility functions
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.querySelector('.upload-section').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Check API health on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.warn('Could not connect to API:', error);
    }
});

