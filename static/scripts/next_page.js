//document.addEventListener('DOMContentLoaded', () => {
//    const recordIcon = document.getElementById('record-icon');
//    const transcription = document.getElementById('transcription');
//
//    let isRecording = false;
//    let recognition;
//
//    if ('webkitSpeechRecognition' in window) {
//        recognition = new webkitSpeechRecognition();
//        recognition.continuous = true;
//        recognition.interimResults = true;
//        recognition.lang = 'en-US'; // Ensure the correct language is set
//
//        recognition.onstart = () => {
//            isRecording = true;
//            recordIcon.classList.add('active');
//        };
//
//        recognition.onresult = (event) => {
//            let interimTranscript = '';
//            for (let i = event.resultIndex; i < event.results.length; ++i) {
//                if (event.results[i].isFinal) {
//                    transcription.textContent = event.results[i][0].transcript; // Use textContent instead of innerHTML
//                } else {
//                    interimTranscript += event.results[i][0].transcript;
//                }
//            }
//        };
//
//        recognition.onerror = (event) => {
//            console.error('Speech recognition error', event);
//        };
//
//        recognition.onend = () => {
//            isRecording = false;
//            recordIcon.classList.remove('active');
//        };
//    } else {
//        alert('Your browser does not support speech recognition.');
//    }
//
//    recordIcon.addEventListener('click', () => {
//        if (isRecording) {
//            recognition.stop();
//        } else {
//            recognition.start();
//        }
//    });
//});



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
//                    transcription.innerHTML = event.results[i][0].transcript;
//                    transcription.innerHTML = "Hello how are you doing?";

//                    input_file_path = 'Recordings/recording.wav'

//                    fetch('/get_text_output', {
//                        method: 'GET',
//                    }).then(response => {
//                        if (response.ok) {
//                            return response.text(); // Convert the response to text
//                        } else {
//                            console.error('Failed to fetch the text output');
//                        }
//                    }).then(text => {
//                        transcription.innerHTML = text; // Set the transcription content with the fetched text
//                    }).catch(error => {
//                        console.error('Error fetching the text output:', error);
//                    });


//with animation

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
                        const cleanedText = text.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();

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


// Function to play videos based on character array
function playCharacterVideos(charArray) {
    const videoPlayer = document.getElementById('video-player');
    let currentCharIndex = 0;

    // Function to load and play the next video
    const playNextVideo = () => {
        if (currentCharIndex < charArray.length) {
            const currentChar = charArray[currentCharIndex];
            console.log(currentChar, 'sajks')
            const videoPath = `static/Alphabets/${currentChar}.mp4`;

            videoPlayer.src = videoPath;
            videoPlayer.play();

            // When the current video ends, move to the next character's video
            videoPlayer.onended = () => {
                currentCharIndex++;
                playNextVideo();
            };
        }
    };

    // Start playing the first video
    playNextVideo();
}


////below is the code after adding mapping
//
//document.addEventListener('DOMContentLoaded', () => {
//    const recordIcon = document.getElementById('record-icon');
//    const transcription = document.getElementById('transcription');
//    const videoPlayer = document.getElementById('video-player');
//
//    let isRecording = false;
//    let recognition;
//
//    const videoMapping = {
//        'A': 'static/Alphabets/A.mp4',
//        'B': 'static/Alphabets/B.mp4',
//        'C': 'static/Alphabets/C.mp4',
//        'D': 'static/Alphabets/D.mp4',
//        'E': 'static/Alphabets/E.mp4',
//        'F': 'static/Alphabets/F.mp4',
//        'G': 'static/Alphabets/G.mp4',
//        'H': 'static/Alphabets/H.mp4',
//        'I': 'static/Alphabets/I.mp4',
//        'J': 'static/Alphabets/J.mp4',
//        'K': 'static/Alphabets/K.mp4',
//        'L': 'static/Alphabets/L.mp4',
//        'M': 'static/Alphabets/M.mp4',
//        'N': 'static/Alphabets/N.mp4',
//        'O': 'static/Alphabets/O.mp4',
//        'P': 'static/Alphabets/P.mp4',
//        'Q': 'static/Alphabets/Q.mp4',
//        'R': 'static/Alphabets/R.mp4',
//        'S': 'static/Alphabets/S.mp4',
//        'T': 'static/Alphabets/T.mp4',
//        'U': 'static/Alphabets/U.mp4',
//        'V': 'static/Alphabets/V.mp4',
//        'W': 'static/Alphabets/W.mp4',
//        'X': 'static/Alphabets/X.mp4',
//        'Y': 'static/Alphabets/Y.mp4',
//        'Z': 'static/Alphabets/Z.mp4',
//        '1': 'static/Alphabets/1.mp4',
//        '2': 'static/Alphabets/2.mp4',
//        '3': 'static/Alphabets/3.mp4',
//        '4': 'static/Alphabets/4.mp4',
//        '5': 'static/Alphabets/5.mp4',
//        '6': 'static/Alphabets/6.mp4',
//        '7': 'static/Alphabets/7.mp4',
//        '8': 'static/Alphabets/8.mp4',
//        '9': 'static/Alphabets/9.mp4'
//    };
//
//    const playVideosForText = (text) => {
//        const cleanText = text.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
//        const videosToPlay = cleanText.split('').map(char => videoMapping[char]);
//
//        let currentVideoIndex = 0;
//
//        const playNextVideo = () => {
//            if (currentVideoIndex < videosToPlay.length) {
//                videoPlayer.src = videosToPlay[currentVideoIndex];
//                videoPlayer.play();
//                currentVideoIndex++;
//            }
//        };
//
//        videoPlayer.addEventListener('ended', playNextVideo);
//
//        playNextVideo(); // Start playing the first video
//    };
//
//    if ('webkitSpeechRecognition' in window) {
//        recognition = new webkitSpeechRecognition();
//        recognition.continuous = true;
//        recognition.interimResults = true;
//
//        recognition.onstart = () => {
//            isRecording = true;
//            recordIcon.classList.add('active');
//        };
//
//        recognition.onresult = (event) => {
//            let interimTranscript = '';
//            for (let i = event.resultIndex; i < event.results.length; ++i) {
//                if (event.results[i].isFinal) {
//                    const finalTranscript = event.results[i][0].transcript;
//                    transcription.innerHTML = finalTranscript;
//                    playVideosForText(finalTranscript);
//                } else {
//                    interimTranscript += event.results[i][0].transcript;
//                }
//            }
//        };
//
//        recognition.onerror = (event) => {
//            console.error('Speech recognition error', event);
//        };
//
//        recognition.onend = () => {
//            isRecording = false;
//            recordIcon.classList.remove('active');
//        };
//    } else {
//        alert('Your browser does not support speech recognition.');
//    }
//
//    recordIcon.addEventListener('click', () => {
//        if (isRecording) {
//            recognition.stop();
//        } else {
//            recognition.start();
//        }
//    });
//});
