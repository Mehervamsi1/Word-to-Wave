document.addEventListener('DOMContentLoaded', () => {
    const recordIcon = document.getElementById('record-icon');
    const transcription = document.getElementById('transcription');

    let isRecording = false;
    let recognition;

    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onstart = () => {
            isRecording = true;
            recordIcon.classList.add('active');
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    transcription.innerHTML = event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event);
        };

        recognition.onend = () => {
            isRecording = false;
            recordIcon.classList.remove('active');
        };
    } else {
        alert('Your browser does not support speech recognition.');
    }

    recordIcon.addEventListener('click', () => {
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });
});
