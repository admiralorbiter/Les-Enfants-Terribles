// Les Enfants Terribles — In-Browser Audio Capture Controller

let mediaRecorder = null;
let audioChunks = [];
let recordTimerInterval = null;
let recordStartTime = null;
let audioStream = null;

function getSupportedMimeType() {
    const types = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/mp4',
        'audio/wav'
    ];
    for (const type of types) {
        if (MediaRecorder.isTypeSupported(type)) {
            return type;
        }
    }
    return '';
}

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

async function toggleRecording(episodeId = null) {
    const recordBtn = document.getElementById('record-btn');
    const timerDisplay = document.getElementById('timer-display');
    const statusText = document.getElementById('recorder-status');

    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        // Start Recording
        try {
            audioChunks = [];
            audioStream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });

            const mimeType = getSupportedMimeType();
            const options = mimeType ? { mimeType } : {};
            mediaRecorder = new MediaRecorder(audioStream, options);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                const mime = mediaRecorder.mimeType || 'audio/webm';
                const audioBlob = new Blob(audioChunks, { type: mime });
                audioStream.getTracks().forEach(track => track.stop());
                await uploadRecording(audioBlob, mime, episodeId);
            };

            mediaRecorder.start(250); // Slice data every 250ms

            // UI State updates
            recordBtn.classList.add('recording');
            statusText.textContent = 'Recording in progress... Click to finish';
            recordStartTime = Date.now();
            timerDisplay.textContent = '00:00';

            recordTimerInterval = setInterval(() => {
                const elapsedSec = Math.floor((Date.now() - recordStartTime) / 1000);
                timerDisplay.textContent = formatDuration(elapsedSec);
            }, 500);

        } catch (err) {
            console.error('Microphone access error:', err);
            statusText.textContent = 'Microphone permission denied or unavailable';
            alert(`Unable to access microphone: ${err.message}`);
        }
    } else if (mediaRecorder.state === 'recording') {
        // Stop Recording
        clearInterval(recordTimerInterval);
        statusText.textContent = 'Saving raw audio atomically...';
        recordBtn.classList.remove('recording');
        mediaRecorder.stop();
    }
}

async function uploadRecording(blob, mimeType, episodeId = null) {
    const statusText = document.getElementById('recorder-status');
    const timerDisplay = document.getElementById('timer-display');
    const titleInput = document.getElementById('episode-title');
    const domainInput = document.getElementById('episode-domain');
    const modeInput = document.getElementById('episode-mode');

    const formData = new FormData();
    const ext = mimeType.includes('ogg') ? '.ogg' : mimeType.includes('wav') ? '.wav' : '.webm';
    formData.append('audio', blob, `capture_${Date.now()}${ext}`);

    if (titleInput && titleInput.value.trim()) {
        formData.append('title', titleInput.value.trim());
    }
    if (domainInput) {
        formData.append('domain', domainInput.value);
    }
    if (modeInput) {
        formData.append('mode', modeInput.value);
    }
    if (episodeId) {
        formData.append('episode_id', episodeId);
    }

    try {
        const response = await fetch('/api/capture/audio', {
            method: 'POST',
            body: formData,
            headers: {
                'HX-Request': 'true'
            }
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({ error: 'Upload failed' }));
            throw new Error(err.error || 'Server rejected audio save');
        }

        const html = await response.text();
        const feed = document.getElementById('episodes-feed');
        const emptyState = document.getElementById('empty-feed-state');

        if (emptyState) {
            emptyState.remove();
        }

        if (feed) {
            // Prepend new episode card
            feed.insertAdjacentHTML('afterbegin', html);
        } else if (episodeId) {
            // We are in episode detail, reload to see newly attached artifact
            window.location.reload();
        }

        statusText.textContent = 'Capture securely preserved on disk.';
        timerDisplay.textContent = '00:00';
        if (titleInput) titleInput.value = '';

        setTimeout(() => {
            statusText.textContent = 'Ready to capture';
        }, 3000);

    } catch (err) {
        console.error('Save error:', err);
        statusText.textContent = `Save failed: ${err.message}`;
        alert(`Failed to persist raw capture: ${err.message}`);
    }
}
