// GraphyBOOK - Auto Demo with Real Videos
// Automatically cycles through prompts and shows corresponding videos

// Demo videos and their corresponding prompts
const demoSequence = [
    {
        video: 'derivatives.mov',
        prompt: 'Create an animation showing the concept of derivatives in calculus. Show a curve with a tangent line that moves along the curve, demonstrating how the slope changes at different points.'
    },
    {
        video: 'linear_alzebra.mov', 
        prompt: 'Animate linear algebra concepts including vector transformations, matrix operations, and eigenvalue decomposition with visual representations.'
    },
    {
        video: 'quantum_wave_function.mov',
        prompt: 'Visualize quantum wave functions showing probability distributions, wave packet evolution, and the uncertainty principle in quantum mechanics.'
    }
];

class GraphyBOOKDemo {
    constructor() {
        this.currentMode = 'prompt';
        this.isProcessing = false;
        this.demoIndex = 0;
        this.isTyping = false;
        this.isDemoRunning = false;
        
        this.initializeElements();
        this.bindEvents();
        this.updateUI();
        
        // Start auto demo after 3 seconds
        setTimeout(() => this.startAutoDemo(), 3000);
    }

    initializeElements() {
        // Mode elements
        this.modeButtons = document.querySelectorAll('.mode-btn');
        this.promptMode = document.getElementById('prompt-mode');
        this.codeMode = document.getElementById('code-mode');
        
        // Input elements
        this.physicsPrompt = document.getElementById('physics-prompt');
        this.manualCode = document.getElementById('manual-code');
        this.generateBtn = document.getElementById('generate-btn');
        this.executeBtn = document.getElementById('execute-btn');
        
        // Status elements
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = this.statusIndicator.querySelector('.status-text');
        this.progressBar = document.getElementById('progress-bar');
        this.progressFill = this.progressBar.querySelector('.progress-fill');
        
        // Video elements
        this.videoContainer = document.getElementById('video-container');
        this.videoPlaceholder = document.getElementById('video-placeholder');
        this.animationVideo = document.getElementById('animation-video');
        this.videoControls = document.getElementById('video-controls');
        this.animationInfo = document.getElementById('animation-info');
        this.downloadBtn = document.getElementById('download-btn');
        this.fullscreenBtn = document.getElementById('fullscreen-btn');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingText = document.getElementById('loading-text');
    }

    bindEvents() {
        // Mode switching
        this.modeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.switchMode(btn.dataset.mode));
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => this.generateAnimation());
        
        // Execute button
        this.executeBtn.addEventListener('click', () => this.executeCode());
        
        // Video controls
        this.downloadBtn.addEventListener('click', () => this.downloadVideo());
        this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        
        // Video end event for auto-continuation
        this.animationVideo.addEventListener('ended', () => this.handleVideoEnd());
        
        // Input validation
        this.physicsPrompt.addEventListener('input', () => this.validateInput());
        this.manualCode.addEventListener('input', () => this.validateInput());
    }

    async startAutoDemo() {
        this.isDemoRunning = true;
        this.updateStatus('🎬 Starting automatic demo...', 'info');
        await this.sleep(1000);
        this.runDemoSequence();
    }

    async runDemoSequence() {
        if (!this.isDemoRunning) return;
        
        if (this.demoIndex >= demoSequence.length) {
            // Reset and start over
            this.demoIndex = 0;
            await this.sleep(2000);
            this.updateStatus('🔄 Demo complete! Restarting...', 'success');
            await this.sleep(1000);
        }
        
        const currentDemo = demoSequence[this.demoIndex];
        
        // Clear previous content and hide video
        this.physicsPrompt.value = '';
        this.hideVideo();
        
        // Type the prompt
        await this.typePrompt(currentDemo.prompt);
        
        // Immediately show video after typing (no wait)
        this.updateStatus('🎬 Animation ready! Playing now...', 'success');
        this.showVideoResult(currentDemo.video);
        
        this.demoIndex++;
    }

    async typePrompt(text) {
        if (this.isTyping) return;
        
        this.isTyping = true;
        this.physicsPrompt.value = '';
        this.updateStatus(`⌨️ Typing prompt ${this.demoIndex + 1} of ${demoSequence.length}...`, 'processing');
        
        // Type character by character with realistic speed
        for (let i = 0; i < text.length; i++) {
            if (!this.isDemoRunning) break;
            this.physicsPrompt.value += text[i];
            await this.sleep(30 + Math.random() * 40); // Realistic typing speed with variation
        }
        
        this.isTyping = false;
        this.updateStatus('✅ Prompt complete! Generating animation...', 'processing');
    }

    handleVideoEnd() {
        if (this.isDemoRunning) {
            // When current video ends, move to next demo after 2 seconds
            setTimeout(() => this.runDemoSequence(), 2000);
        }
    }

    showVideoResult(videoPath) {
        // Hide placeholder and show video
        this.videoPlaceholder.style.display = 'none';
        this.animationVideo.style.display = 'block';
        this.videoControls.style.display = 'flex';
        this.animationInfo.style.display = 'block';
        
        // Set video source
        this.animationVideo.src = videoPath;
        this.animationVideo.load();
        
        // Update animation info
        document.getElementById('duration-info').textContent = 'Auto';
        document.getElementById('quality-info').textContent = '720p';
        document.getElementById('animation-status').textContent = 'Playing';
        
        // Auto-play the video
        this.animationVideo.play().catch(e => {
            console.log('Auto-play prevented by browser:', e);
        });
        
        this.updateStatus(`🎬 Playing animation ${this.demoIndex} of ${demoSequence.length}`, 'success');
    }

    hideVideo() {
        this.videoPlaceholder.style.display = 'block';
        this.animationVideo.style.display = 'none';
        this.videoControls.style.display = 'none';
        this.animationInfo.style.display = 'none';
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Update button states
        this.modeButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
        
        // Update input modes
        this.promptMode.classList.toggle('active', mode === 'prompt');
        this.codeMode.classList.toggle('active', mode === 'code');
        
        this.validateInput();
        this.updateStatus('Ready for ' + (mode === 'prompt' ? 'AI generation' : 'code execution'));
    }

    validateInput() {
        const isPromptMode = this.currentMode === 'prompt';
        const promptText = this.physicsPrompt.value.trim();
        const codeText = this.manualCode.value.trim();
        
        const isValid = isPromptMode ? promptText.length > 0 : codeText.length > 0;
        
        this.generateBtn.disabled = !isValid || this.isProcessing;
        this.executeBtn.disabled = !isValid || this.isProcessing;
    }

    updateStatus(message, type = 'info') {
        this.statusText.textContent = message;
        this.statusIndicator.className = `status-indicator ${type}`;
    }

    setProgress(percentage) {
        this.progressFill.style.width = `${percentage}%`;
    }

    updateUI() {
        this.validateInput();
        this.updateStatus('🚀 GraphyBOOK Demo Ready - Auto demo starting soon...', 'info');
    }

    async generateAnimation() {
        // Stop demo if user manually generates
        this.isDemoRunning = false;
        
        const prompt = this.physicsPrompt.value.trim();
        if (!prompt || this.isProcessing) return;

        this.startProcessing();
        this.updateStatus('🧠 Understanding your physics concept...', 'processing');
        this.setProgress(10);

        // Simulate generation process
        const steps = [
            { message: '🎨 Planning the visualization...', progress: 30, delay: 1000 },
            { message: '🚀 Generating Manim code...', progress: 50, delay: 1500 },
            { message: '🤖 Compiling animation...', progress: 70, delay: 2000 },
            { message: '🎬 Rendering video...', progress: 90, delay: 3000 }
        ];

        for (const step of steps) {
            await this.sleep(step.delay);
            this.updateStatus(step.message, 'processing');
            this.setProgress(step.progress);
        }

        this.setProgress(100);
        this.updateStatus('🎉 Animation generated successfully!', 'success');
        this.showVideoResult('vids/derivatives.mov'); // Default to first video
        this.stopProcessing();
    }

    async executeCode() {
        // Stop demo if user manually executes
        this.isDemoRunning = false;
        
        const code = this.manualCode.value.trim();
        if (!code || this.isProcessing) return;

        this.startProcessing();
        this.updateStatus('⚡ Executing your code...', 'processing');
        this.setProgress(20);

        // Simulate execution
        await this.sleep(3000);
        this.setProgress(100);
        this.updateStatus('✅ Code executed successfully!', 'success');
        this.showVideoResult('vids/linear_alzebra.mov'); // Default to second video
        this.stopProcessing();
    }

    startProcessing() {
        this.isProcessing = true;
        this.validateInput();
    }

    stopProcessing() {
        this.isProcessing = false;
        this.validateInput();
    }

    downloadVideo() {
        if (this.animationVideo.src) {
            const link = document.createElement('a');
            link.href = this.animationVideo.src;
            link.download = 'physics-animation.mp4';
            link.click();
        }
    }

    toggleFullscreen() {
        if (this.animationVideo.requestFullscreen) {
            this.animationVideo.requestFullscreen();
        } else if (this.animationVideo.webkitRequestFullscreen) {
            this.animationVideo.webkitRequestFullscreen();
        } else if (this.animationVideo.msRequestFullscreen) {
            this.animationVideo.msRequestFullscreen();
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the demo when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.graphybook = new GraphyBOOKDemo();
    console.log('🎬 GraphyBOOK Auto Demo initialized!');
});