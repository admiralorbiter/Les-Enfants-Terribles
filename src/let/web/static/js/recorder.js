// Les Enfants Terribles — In-Browser Audio Capture & Bridge Controller

let mediaRecorder = null;
let audioChunks = [];
let recordTimerInterval = null;
let recordStartTime = null;
let audioStream = null;
let lastFailedCapture = null;

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
                if (audioStream) {
                    audioStream.getTracks().forEach(track => track.stop());
                }
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
    const recoveryBanner = document.getElementById('capture-recovery-banner');

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
            feed.insertAdjacentHTML('afterbegin', html);
            if (window.htmx) {
                htmx.process(feed);
            }
        } else if (episodeId) {
            window.location.reload();
        }

        statusText.textContent = 'Capture securely preserved on disk.';
        timerDisplay.textContent = '00:00';
        if (titleInput) titleInput.value = '';

        if (recoveryBanner) {
            recoveryBanner.style.display = 'none';
        }
        lastFailedCapture = null;

        setTimeout(() => {
            statusText.textContent = 'Ready to capture';
        }, 3000);

    } catch (err) {
        console.error('Save error:', err);
        lastFailedCapture = { blob, mimeType, episodeId };
        statusText.textContent = `Save failed: ${err.message}`;
        showEmergencyRecoveryUI(err.message);
    }
}

function showEmergencyRecoveryUI(errorMessage) {
    let banner = document.getElementById('capture-recovery-banner');
    if (!banner) {
        banner = document.createElement('div');
        banner.id = 'capture-recovery-banner';
        banner.className = 'recovery-banner';
        const controlPanel = document.querySelector('.capture-controls') || document.body;
        controlPanel.insertAdjacentElement('afterend', banner);
    }

    banner.style.display = 'block';
    banner.innerHTML = `
        <div style="background: #2a1b1b; border: 1px solid #ff4444; border-radius: 6px; padding: 12px 16px; margin: 12px 0; color: #ffcccc;">
            <p style="margin: 0 0 8px 0; font-weight: bold;">⚠️ Upload failed: ${errorMessage}</p>
            <p style="margin: 0 0 10px 0; font-size: 0.9em;">Your raw audio is safe in browser memory. You can retry the upload or download a backup copy immediately:</p>
            <div style="display: flex; gap: 8px;">
                <button type="button" onclick="retryLastCapture()" style="background: #ff5555; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer;">Retry Upload</button>
                <button type="button" onclick="downloadEmergencyAudio()" style="background: #444; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer;">Emergency Download (.webm)</button>
            </div>
        </div>
    `;
}

async function retryLastCapture() {
    if (!lastFailedCapture) return;
    const { blob, mimeType, episodeId } = lastFailedCapture;
    await uploadRecording(blob, mimeType, episodeId);
}

function downloadEmergencyAudio() {
    if (!lastFailedCapture || !lastFailedCapture.blob) {
        alert('No capture available in memory.');
        return;
    }
    const url = URL.createObjectURL(lastFailedCapture.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `emergency_capture_${Date.now()}.webm`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ---------------- Global Audio Seeking ----------------

function seekAudio(artifactId, seconds) {
    // Look for specific player first, fallback to generic
    let player = document.getElementById(`audio-player-${artifactId}`);
    if (!player) {
        player = document.getElementById('audio-player-main') || document.querySelector('audio');
    }
    if (player) {
        player.currentTime = parseFloat(seconds);
        player.play().catch(() => {});
    }
}

// ---------------- Mission Brief & Analysis Bridge Helpers ----------------

async function copyMissionBrief(episodeId) {
    const btn = document.getElementById(`copy-brief-btn-${episodeId}`);
    try {
        const res = await fetch(`/episodes/${episodeId}/brief`);
        if (!res.ok) throw new Error('Could not fetch Mission Brief');
        const briefMarkdown = await res.text();

        await navigator.clipboard.writeText(briefMarkdown);
        if (btn) {
            const origText = btn.innerHTML;
            btn.innerHTML = '✓ Brief Copied to Clipboard!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.innerHTML = origText;
                btn.classList.remove('copied');
            }, 3000);
        }
    } catch (err) {
        console.error('Clipboard copy error:', err);
        alert('Failed to copy brief to clipboard: ' + err.message);
    }
}

async function copySummaryText(episodeId) {
    const btn = document.getElementById(`copy-summary-btn-${episodeId}`);
    const contentElem = document.getElementById(`synthesis-text-${episodeId}`);
    if (!contentElem) return;

    try {
        await navigator.clipboard.writeText(contentElem.innerText.trim());
        if (btn) {
            const origText = btn.innerHTML;
            btn.innerHTML = '✓ Summary Copied!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.innerHTML = origText;
                btn.classList.remove('copied');
            }, 2500);
        }
    } catch (err) {
        alert('Failed to copy summary: ' + err.message);
    }
}

function openImportModal(episodeId) {
    const modal = document.getElementById(`import-modal-${episodeId}`);
    if (modal) {
        if (typeof modal.showModal === 'function') {
            modal.showModal();
        } else {
            modal.setAttribute('open', 'true');
        }
    }
}

function closeImportModal(episodeId) {
    const modal = document.getElementById(`import-modal-${episodeId}`);
    if (modal) {
        if (typeof modal.close === 'function') {
            modal.close();
        } else {
            modal.removeAttribute('open');
        }
    }
}

async function submitAnalysisImport(event, episodeId) {
    event.preventDefault();
    const providerSelect = document.getElementById(`provider-select-${episodeId}`);
    const responseText = document.getElementById(`response-text-${episodeId}`);
    const submitBtn = document.getElementById(`import-submit-btn-${episodeId}`);

    if (!responseText || !responseText.value.trim()) {
        alert('Please paste the AI response text');
        return;
    }

    if (submitBtn) {
        submitBtn.textContent = 'Importing & Verifying...';
        submitBtn.disabled = true;
    }

    try {
        const formData = new FormData();
        formData.append('response_text', responseText.value.trim());
        formData.append('provider', providerSelect ? providerSelect.value : 'manual');

        const res = await fetch(`/api/episodes/${episodeId}/import_analysis`, {
            method: 'POST',
            body: formData,
            headers: {
                'HX-Request': 'true'
            }
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: 'Import failed' }));
            throw new Error(err.error || 'Server rejected import');
        }

        const html = await res.text();
        const container = document.getElementById(`analysis-container-${episodeId}`);
        if (container) {
            container.outerHTML = html;
            if (window.htmx) {
                htmx.process(document.getElementById(`analysis-container-${episodeId}`) || document.body);
            }
        }

        closeImportModal(episodeId);
    } catch (err) {
        console.error('Import error:', err);
        alert('Failed to import analysis: ' + err.message);
    } finally {
        if (submitBtn) {
            submitBtn.textContent = 'Save Derived Analysis';
            submitBtn.disabled = false;
        }
    }
}
