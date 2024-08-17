

//below is the working code before the mapping was created
document.addEventListener('DOMContentLoaded', () => {
    const recordIcon = document.getElementById('record-icon');
    const transcription = document.getElementById('transcription');

    let isRecording = false;
    let recognition;
    let mediaRecorder;
    let audioChunks = [];

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
                console.log(event.results[i][0].transcript);

                    // Fetch the text output from the Flask route
                    fetch('/get_text_output', {
                        method: 'GET',
                    }).then(response => {
                        if (response.ok) {
                            return response.text(); // Convert the response to text
                        } else {
                            console.error('Failed to fetch the text output');
                        }
                    }).then(text => {
                        // Clean the text: remove non-alphabetical characters and spaces
                        transcription.innerHTML = text;
                        const cleanedText = text.replace(/[^a-zA-Z0-9 ]/g, '').toUpperCase();

                        // Convert cleaned text to an array of characters
                        const charArray = cleanedText.split('');

                        // Load and play videos in sequence based on the characters
                        playCharacterVideos(charArray);
                    }).catch(error => {
                        console.error('Error fetching the text output:', error);
                    });

                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event);
        };

        recognition.onend = async () => {
            isRecording = false;
            recordIcon.classList.remove('active');

            // Stop the audio recording and send the audio data
            mediaRecorder.stop();
        };
    } else {
        alert('Your browser does not support speech recognition.');
    }

    recordIcon.addEventListener('click', () => {
        if (isRecording) {
            recognition.stop();
        } else {
            // Start speech recognition
            recognition.start();

            // Start audio recording
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.wav');

                    // Send audio data to Flask
                    fetch('/save_audio', {
                        method: 'POST',
                        body: formData,
                    }).then(response => {
                        if (response.ok) {
                            console.log('Audio saved successfully');
                        }
                    }).catch(error => {
                        console.error('Error saving audio:', error);
                    });
                    audioChunks = [];
                };
            });
        }
    });
});




function playCharacterVideos(charArray) {
    const videoPlayer = document.getElementById('video-player');
    let currentCharIndex = 0;

    // Function to load and play the next video
    const playNextVideo = () => {
        if (currentCharIndex < charArray.length) {
            const currentChar = charArray[currentCharIndex];
            console.log(currentChar, 'current_character')
            if (currentChar === ' ') {
                // If the current character is a space, add a delay before playing the next video
                setTimeout(() => {
                    currentCharIndex++;
                    playNextVideo();
                }, 700); // Adjust the delay (in milliseconds) as needed
            } else {
                const videoPath = `static/Alphabets/${currentChar}.mp4`;

                videoPlayer.src = videoPath;
                videoPlayer.play();

                // When the current video ends, move to the next character's video
                videoPlayer.onended = () => {
                    currentCharIndex++;
                    playNextVideo();
                };
            }
        }
    };

    // Start playing the first video
    playNextVideo();
}







/* this code is for speech mic and upload section */

document.getElementById('file-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file && file.type === 'audio/wav') {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                console.log('File uploaded successfully');
                // You can also display a message or update the UI here
            } else {
                console.error('Failed to upload the file');
            }
        }).catch(error => {
            console.error('Error uploading the file:', error);
        });

        console.log('finished upload')
                    fetch('/get_text_output', {
                        method: 'GET',
                    }).then(response => {
                        if (response.ok) {
                            console.log('text outputttt')
                            return response.text(); // Convert the response to text
                        } else {
                            console.error('Failed to fetch the text output');
                        }
                    }).then(text => {
                        // Clean the text: remove non-alphabetical characters and spaces
                        transcription.innerHTML = text;
                        const cleanedText = text.replace(/[^a-zA-Z0-9 ]/g, '').toUpperCase();

                        // Convert cleaned text to an array of characters
                        const charArray = cleanedText.split('');

                        // Load and play videos in sequence based on the characters
                        playCharacterVideos(charArray);
                    }).catch(error => {
                        console.error('Error fetching the text output:', error);
                    });
    } else {
        alert('Please upload a valid WAV file.');
    }
});









