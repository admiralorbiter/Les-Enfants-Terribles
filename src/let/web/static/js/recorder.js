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
    } else {
        const predText = document.getElementById('prediction-text');
        const predConcept = document.getElementById('prediction-concept');
        const predConf = document.getElementById('prediction-confidence');
        if (predText && predText.value.trim()) {
            formData.append('prediction_text', predText.value.trim());
        }
        if (predConcept && predConcept.value.trim()) {
            formData.append('prediction_concept', predConcept.value.trim());
        }
        if (predConf && predConf.value.trim()) {
            formData.append('prediction_confidence', predConf.value.trim());
        }
        if (voicePredictionBlob) {
            const predExt = voicePredictionBlob.type.includes('ogg') ? '.ogg' : voicePredictionBlob.type.includes('wav') ? '.wav' : '.webm';
            formData.append('prediction_audio', voicePredictionBlob, `pred_${Date.now()}${predExt}`);
        }
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
            const firstCard = feed.firstElementChild;
            const epId = (firstCard && firstCard.id) ? firstCard.id.replace('episode-', '') : episodeId;
            if (epId) {
                pollTranscriptUntilReady(epId);
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
        clearPrediction();
        if (typeof clearPredictionDraft === 'function') {
            clearPredictionDraft();
        }

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

// ---------------- Active Transcript Polling Watcher ----------------

function pollTranscriptUntilReady(episodeId, maxAttempts = 60) {
    let attempts = 0;
    const interval = setInterval(async () => {
        attempts++;
        const container = document.getElementById(`transcript-container-${episodeId}`);
        if (!container || attempts > maxAttempts) {
            clearInterval(interval);
            return;
        }

        // If it's already ready, stop polling
        if (container.querySelector('.transcript-body') || container.querySelector('.status-ready')) {
            clearInterval(interval);
            return;
        }

        try {
            const res = await fetch(`/episodes/${episodeId}/transcript`);
            if (res.ok) {
                const html = await res.text();
                const temp = document.createElement('div');
                temp.innerHTML = html;
                const newBox = temp.firstElementChild;
                if (newBox && (newBox.querySelector('.transcript-body') || newBox.querySelector('.status-ready') || newBox.querySelector('.transcript-error'))) {
                    container.outerHTML = html;
                    if (window.htmx) {
                        htmx.process(document.getElementById(`transcript-container-${episodeId}`) || document.body);
                    }
                    clearInterval(interval);
                }
            }
        } catch (e) {
            console.error('Transcript polling error:', e);
        }
    }, 1500);
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

// ---------------- Inline Perturbation Voice & Text Answers ----------------

let inlineMediaRecorder = null;
let inlineAudioChunks = [];
let inlineStream = null;
let inlineTimerInterval = null;
let inlineStartTime = null;

async function startInlineVoiceAnswer(episodeId, questionId) {
    const actions = document.getElementById(`actions-${episodeId}-${questionId}`);
    const voiceBox = document.getElementById(`inline-voice-box-${episodeId}-${questionId}`);
    const timerDisplay = document.getElementById(`inline-timer-${episodeId}-${questionId}`);

    try {
        inlineAudioChunks = [];
        inlineStream = await navigator.mediaDevices.getUserMedia({
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
            }
        });

        const mimeType = getSupportedMimeType();
        const options = mimeType ? { mimeType } : {};
        inlineMediaRecorder = new MediaRecorder(inlineStream, options);

        inlineMediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                inlineAudioChunks.push(event.data);
            }
        };

        inlineMediaRecorder.onstop = async () => {
            const mime = inlineMediaRecorder.mimeType || 'audio/webm';
            const audioBlob = new Blob(inlineAudioChunks, { type: mime });
            if (inlineStream) {
                inlineStream.getTracks().forEach(track => track.stop());
            }
            await uploadPerturbationVoiceAnswer(audioBlob, mime, episodeId, questionId);
        };

        inlineMediaRecorder.start(250);

        if (actions) actions.style.display = 'none';
        if (voiceBox) voiceBox.style.display = 'flex';

        inlineStartTime = Date.now();
        if (timerDisplay) timerDisplay.textContent = '00:00';
        inlineTimerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - inlineStartTime) / 1000);
            if (timerDisplay) timerDisplay.textContent = formatDuration(elapsed);
        }, 500);

    } catch (err) {
        console.error('Microphone error on perturbation answer:', err);
        alert(`Microphone access error: ${err.message}`);
    }
}

function stopInlineVoiceAnswer(episodeId, questionId) {
    if (inlineTimerInterval) clearInterval(inlineTimerInterval);
    if (inlineMediaRecorder && inlineMediaRecorder.state === 'recording') {
        inlineMediaRecorder.stop();
    }
}

async function uploadPerturbationVoiceAnswer(blob, mimeType, episodeId, questionId) {
    const ext = mimeType.includes('ogg') ? '.ogg' : mimeType.includes('wav') ? '.wav' : '.webm';
    const formData = new FormData();
    formData.append('audio', blob, `answer_${Date.now()}${ext}`);

    try {
        const res = await fetch(`/api/episodes/${episodeId}/perturbations/${questionId}/answer`, {
            method: 'POST',
            body: formData,
            headers: {
                'HX-Request': 'true'
            }
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: 'Upload failed' }));
            throw new Error(err.error || 'Server rejected voice answer');
        }

        const html = await res.text();
        const container = document.getElementById(`analysis-container-${episodeId}`);
        if (container) {
            container.outerHTML = html;
            if (window.htmx) {
                htmx.process(document.getElementById(`analysis-container-${episodeId}`) || document.body);
            }
        }
    } catch (err) {
        console.error('Voice answer save error:', err);
        alert(`Failed to save voice answer: ${err.message}`);
    }
}

function toggleInlineTextAnswer(episodeId, questionId) {
    const form = document.getElementById(`inline-text-form-${episodeId}-${questionId}`);
    const actions = document.getElementById(`actions-${episodeId}-${questionId}`);
    if (form) {
        const isHidden = form.style.display === 'none';
        form.style.display = isHidden ? 'block' : 'none';
        if (actions) actions.style.display = isHidden ? 'none' : 'flex';
        if (isHidden) {
            const textarea = form.querySelector('textarea');
            if (textarea) textarea.focus();
        }
    }
}
function togglePredictionCard() {
    const card = document.getElementById('prediction-card');
    const toggleBtn = document.getElementById('toggle-prediction-btn');
    const toggleLabel = document.getElementById('toggle-prediction-label');
    if (!card) return;
    if (card.style.display === 'none' || !card.style.display) {
        card.style.display = 'block';
        if (toggleBtn) toggleBtn.classList.add('open');
        if (toggleLabel) toggleLabel.textContent = 'Collapse Pre-Session Prediction';
        const textInput = document.getElementById('prediction-text');
        if (textInput) textInput.focus();
    } else {
        card.style.display = 'none';
        if (toggleBtn) toggleBtn.classList.remove('open');
        if (toggleLabel) toggleLabel.textContent = 'Add Pre-Session Prediction (Calibration)';
    }
}

function selectConceptChip(chipText) {
    const conceptInput = document.getElementById('prediction-concept');
    const textInput = document.getElementById('prediction-text');
    if (conceptInput) {
        conceptInput.value = chipText;
    }
    // Highlight active chip
    document.querySelectorAll('.concept-chip').forEach(el => {
        if (el.textContent.trim() === chipText.trim()) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });
    if (textInput && !textInput.value.trim()) {
        textInput.focus();
    }
    savePredictionDraft();
}

function setConfidence(level) {
    const confInput = document.getElementById('prediction-confidence');
    if (confInput) confInput.value = level;
    document.querySelectorAll('.confidence-pill').forEach(el => {
        if (el.getAttribute('data-level') === level) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });
    savePredictionDraft();
}

function clearPrediction() {
    const textInput = document.getElementById('prediction-text');
    const conceptInput = document.getElementById('prediction-concept');
    if (textInput) textInput.value = '';
    if (conceptInput) conceptInput.value = '';
    document.querySelectorAll('.concept-chip').forEach(el => el.classList.remove('active'));
    setConfidence('medium');
    clearVoicePrediction();
    clearPredictionDraft();
}

function updateDomainChips(domain) {
    const container = document.getElementById('concept-chips-container');
    if (!container || !window.DOMAIN_PALETTES) return;
    const chips = window.DOMAIN_PALETTES[domain] || window.DOMAIN_PALETTES['general'] || [];
    container.innerHTML = '';
    
    const conceptInput = document.getElementById('prediction-concept');
    const currentConcept = conceptInput ? conceptInput.value.trim() : '';

    chips.forEach(chip => {
        const btn = document.createElement('button');
        btn.type = 'button';
        const isMatch = (chip.trim() === currentConcept);
        btn.className = 'concept-chip' + (isMatch ? ' active' : '');
        btn.textContent = chip;
        btn.onclick = () => selectConceptChip(chip);
        container.appendChild(btn);
    });

    savePredictionDraft();
}

let voicePredictionBlob = null;
let voicePredRecorder = null;
let voicePredChunks = [];
let voicePredInterval = null;
let voicePredStartTime = null;

async function toggleVoicePredictionRecording() {
    const btn = document.getElementById('voice-pred-btn');
    const label = document.getElementById('voice-pred-label');
    const icon = document.getElementById('voice-pred-icon');
    const timer = document.getElementById('voice-pred-timer');
    const preview = document.getElementById('voice-pred-preview');
    const audioEl = document.getElementById('voice-pred-audio');
    const durationEl = document.getElementById('voice-pred-duration');
    const progressEl = document.getElementById('voice-pred-progress');
    const playIcon = document.getElementById('voice-pred-play-icon');

    if (!voicePredRecorder || voicePredRecorder.state === 'inactive') {
        try {
            voicePredChunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mimeType = getSupportedMimeType();
            const options = mimeType ? { mimeType } : {};
            voicePredRecorder = new MediaRecorder(stream, options);

            voicePredRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) voicePredChunks.push(e.data);
            };

            voicePredRecorder.onstop = () => {
                const mime = voicePredRecorder.mimeType || 'audio/webm';
                voicePredictionBlob = new Blob(voicePredChunks, { type: mime });
                stream.getTracks().forEach(t => t.stop());
                
                if (audioEl) {
                    audioEl.src = URL.createObjectURL(voicePredictionBlob);
                    audioEl.onloadedmetadata = () => {
                        if (durationEl && isFinite(audioEl.duration)) {
                            durationEl.textContent = formatDuration(Math.round(audioEl.duration));
                        }
                    };
                    audioEl.ontimeupdate = () => {
                        if (audioEl.duration && progressEl) {
                            const pct = (audioEl.currentTime / audioEl.duration) * 100;
                            progressEl.style.width = `${pct}%`;
                        }
                    };
                    audioEl.onended = () => {
                        if (playIcon) playIcon.textContent = '▶';
                        if (progressEl) progressEl.style.width = '0%';
                    };
                }
                
                if (preview) preview.style.display = 'inline-flex';
                if (timer) timer.style.display = 'none';
                if (label) label.textContent = 'Speak Prediction';
                if (icon) icon.textContent = '🎙️';
                if (btn) {
                    btn.classList.remove('recording');
                    btn.style.display = 'none';
                }
                savePredictionDraft();
            };

            voicePredRecorder.start(250);
            voicePredStartTime = Date.now();
            if (label) label.textContent = 'Finish Voice Prediction';
            if (icon) icon.textContent = '■';
            if (btn) btn.classList.add('recording');
            if (timer) {
                timer.textContent = '● 00:00';
                timer.style.display = 'inline-flex';
            }
            if (preview) preview.style.display = 'none';

            voicePredInterval = setInterval(() => {
                const elapsedSec = Math.floor((Date.now() - voicePredStartTime) / 1000);
                if (timer) timer.textContent = `● ${formatDuration(elapsedSec)}`;
            }, 500);

        } catch (err) {
            console.error('Microphone access error for voice prediction:', err);
            alert(`Unable to access microphone: ${err.message}`);
        }
    } else if (voicePredRecorder.state === 'recording') {
        if (voicePredInterval) clearInterval(voicePredInterval);
        voicePredRecorder.stop();
    }
}

function toggleVoicePredictionPlay() {
    const audioEl = document.getElementById('voice-pred-audio');
    const playIcon = document.getElementById('voice-pred-play-icon');
    if (!audioEl) return;

    if (audioEl.paused) {
        audioEl.play().then(() => {
            if (playIcon) playIcon.textContent = '⏸';
        }).catch(err => console.error('Audio play error:', err));
    } else {
        audioEl.pause();
        if (playIcon) playIcon.textContent = '▶';
    }
}

function seekVoicePrediction(e) {
    const audioEl = document.getElementById('voice-pred-audio');
    const track = e.currentTarget;
    if (!audioEl || !track || !audioEl.duration) return;

    const rect = track.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const pct = Math.max(0, Math.min(1, clickX / rect.width));
    audioEl.currentTime = pct * audioEl.duration;
}

function clearVoicePrediction() {
    voicePredictionBlob = null;
    const preview = document.getElementById('voice-pred-preview');
    const audioEl = document.getElementById('voice-pred-audio');
    const label = document.getElementById('voice-pred-label');
    const icon = document.getElementById('voice-pred-icon');
    const timer = document.getElementById('voice-pred-timer');
    const btn = document.getElementById('voice-pred-btn');
    const playIcon = document.getElementById('voice-pred-play-icon');
    const progressEl = document.getElementById('voice-pred-progress');

    if (audioEl) {
        audioEl.pause();
        audioEl.src = '';
    }
    if (playIcon) playIcon.textContent = '▶';
    if (progressEl) progressEl.style.width = '0%';
    if (preview) preview.style.display = 'none';
    if (timer) timer.style.display = 'none';
    if (label) label.textContent = 'Speak Prediction';
    if (icon) icon.textContent = '🎙️';
    if (btn) {
        btn.classList.remove('recording');
        btn.style.display = 'inline-flex';
    }
    savePredictionDraft();
}

// ==========================================================================
// IndexedDB + LocalStorage Draft Persistence for Pre-Session Predictions
// ==========================================================================

const DRAFT_DB_NAME = 'LET_Drafts_DB';
const DRAFT_STORE_NAME = 'prediction_drafts';
const DRAFT_KEY = 'active_prediction_draft';
const DRAFT_LS_KEY = 'let_prediction_draft_meta';

function openDraftDB() {
    return new Promise((resolve, reject) => {
        if (!window.indexedDB) {
            reject(new Error('IndexedDB not supported'));
            return;
        }
        const req = indexedDB.open(DRAFT_DB_NAME, 1);
        req.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains(DRAFT_STORE_NAME)) {
                db.createObjectStore(DRAFT_STORE_NAME);
            }
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}

async function savePredictionDraft() {
    const textInput = document.getElementById('prediction-text');
    const conceptInput = document.getElementById('prediction-concept');
    const confInput = document.getElementById('prediction-confidence');
    const domainSelect = document.getElementById('episode-domain');
    const draftIndicator = document.getElementById('draft-indicator');

    const meta = {
        text: textInput ? textInput.value : '',
        concept: conceptInput ? conceptInput.value : '',
        confidence: confInput ? confInput.value : 'medium',
        domain: domainSelect ? domainSelect.value : 'general',
        hasAudio: !!voicePredictionBlob,
        updatedAt: Date.now()
    };

    if (!meta.text.trim() && !meta.concept && !voicePredictionBlob) {
        await clearPredictionDraft();
        return;
    }

    // 1. Synchronously save metadata to LocalStorage
    try {
        localStorage.setItem(DRAFT_LS_KEY, JSON.stringify(meta));
    } catch (e) {}

    // 2. Asynchronously save full draft including audio blob to IndexedDB
    try {
        const db = await openDraftDB();
        const tx = db.transaction(DRAFT_STORE_NAME, 'readwrite');
        const draft = { ...meta, audioBlob: voicePredictionBlob };
        tx.objectStore(DRAFT_STORE_NAME).put(draft, DRAFT_KEY);
    } catch (err) {
        console.warn('Could not auto-save prediction draft to IndexedDB:', err);
    }

    if (draftIndicator) {
        draftIndicator.textContent = '● Draft Saved';
        draftIndicator.style.display = 'inline-block';
        draftIndicator.style.color = '#10b981';
        draftIndicator.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        draftIndicator.style.background = 'rgba(16, 185, 129, 0.12)';
    }
}

async function loadPredictionDraft() {
    // 1. Synchronously restore metadata from LocalStorage first for instant UI response
    try {
        const rawMeta = localStorage.getItem(DRAFT_LS_KEY);
        if (rawMeta) {
            const meta = JSON.parse(rawMeta);
            applyDraftMetaToUI(meta);
        }
    } catch (e) {}

    // 2. Load audio blob and authoritative draft from IndexedDB
    try {
        const db = await openDraftDB();
        const tx = db.transaction(DRAFT_STORE_NAME, 'readonly');
        const req = tx.objectStore(DRAFT_STORE_NAME).get(DRAFT_KEY);
        req.onsuccess = () => {
            const draft = req.result;
            if (!draft) return;
            applyDraftMetaToUI(draft);

            if (draft.audioBlob) {
                voicePredictionBlob = draft.audioBlob;
                const audioEl = document.getElementById('voice-pred-audio');
                const preview = document.getElementById('voice-pred-preview');
                const btn = document.getElementById('voice-pred-btn');
                const durationEl = document.getElementById('voice-pred-duration');

                if (audioEl) {
                    audioEl.src = URL.createObjectURL(draft.audioBlob);
                    audioEl.onloadedmetadata = () => {
                        if (durationEl && isFinite(audioEl.duration)) {
                            durationEl.textContent = formatDuration(Math.round(audioEl.duration));
                        }
                    };
                }
                if (preview) preview.style.display = 'inline-flex';
                if (btn) btn.style.display = 'none';
            }
        };
    } catch (err) {
        console.warn('Could not load prediction draft from IndexedDB:', err);
    }
}

function applyDraftMetaToUI(draft) {
    if (!draft) return;
    if (!draft.text && !draft.concept && !draft.hasAudio && !draft.audioBlob) return;

    const card = document.getElementById('prediction-card');
    const toggleBtn = document.getElementById('toggle-prediction-btn');
    const toggleLabel = document.getElementById('toggle-prediction-label');
    const textInput = document.getElementById('prediction-text');
    const domainSelect = document.getElementById('episode-domain');
    const draftIndicator = document.getElementById('draft-indicator');

    if (card) card.style.display = 'block';
    if (toggleBtn) toggleBtn.classList.add('open');
    if (toggleLabel) toggleLabel.textContent = 'Collapse Pre-Session Prediction';

    if (draft.domain && domainSelect) {
        domainSelect.value = draft.domain;
        // Populate chips for domain without resetting text/audio
        const container = document.getElementById('concept-chips-container');
        if (container && window.DOMAIN_PALETTES) {
            const chips = window.DOMAIN_PALETTES[draft.domain] || window.DOMAIN_PALETTES['general'] || [];
            container.innerHTML = '';
            chips.forEach(chip => {
                const btn = document.createElement('button');
                btn.type = 'button';
                const isMatch = (draft.concept && chip.trim() === draft.concept.trim());
                btn.className = 'concept-chip' + (isMatch ? ' active' : '');
                btn.textContent = chip;
                btn.onclick = () => selectConceptChip(chip);
                container.appendChild(btn);
            });
        }
    }

    if (draft.concept) {
        const conceptInput = document.getElementById('prediction-concept');
        if (conceptInput) conceptInput.value = draft.concept;
        document.querySelectorAll('.concept-chip').forEach(el => {
            if (el.textContent.trim() === draft.concept.trim()) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });
    }

    if (draft.confidence) {
        setConfidence(draft.confidence);
    }
    if (draft.text && textInput) {
        textInput.value = draft.text;
    }

    if (draftIndicator) {
        draftIndicator.textContent = '● Staged Draft Restored';
        draftIndicator.style.display = 'inline-block';
        draftIndicator.style.color = '#f59e0b';
        draftIndicator.style.borderColor = 'rgba(245, 158, 11, 0.3)';
        draftIndicator.style.background = 'rgba(245, 158, 11, 0.12)';
    }
}

async function clearPredictionDraft() {
    try {
        localStorage.removeItem(DRAFT_LS_KEY);
    } catch (e) {}

    try {
        const db = await openDraftDB();
        const tx = db.transaction(DRAFT_STORE_NAME, 'readwrite');
        tx.objectStore(DRAFT_STORE_NAME).delete(DRAFT_KEY);
    } catch (err) {
        console.warn('Could not delete prediction draft from IndexedDB:', err);
    }

    const draftIndicator = document.getElementById('draft-indicator');
    if (draftIndicator) draftIndicator.style.display = 'none';
}

// Initialize draft loading and auto-save input listeners on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPredictionDraftListeners);
} else {
    initPredictionDraftListeners();
}

function initPredictionDraftListeners() {
    loadPredictionDraft();
    const textInput = document.getElementById('prediction-text');
    if (textInput) {
        textInput.addEventListener('input', () => {
            savePredictionDraft();
        });
    }
    const domainSelect = document.getElementById('episode-domain');
    if (domainSelect) {
        domainSelect.addEventListener('change', () => {
            savePredictionDraft();
        });
    }
}






