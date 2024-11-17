Module.register("MMM-FaceRecognition", {
    defaults: {},

    start: function() {
        console.log("MMM-FaceRecognition: Starting module");
        document.addEventListener('keydown', this.handleKeyPress.bind(this)); // Bind the event listener
    },

    getDom: function() {
        const wrapper = document.createElement("div");
    
        // Clear previous content (if necessary) and set styles if needed
        wrapper.style.fontSize = "18px"; // Example style, adjust as needed
        wrapper.style.color = "white"; // Change text color if needed
        wrapper.style.padding = "10px"; // Add padding for better readability
    
        // Create message elements
        const message1 = document.createElement("div");
        message1.textContent = "Press 'f' to run the face recognition.";
        
        const message2 = document.createElement("div");
        message2.textContent = "Press 'o' to run object detection.";

        const message3 = document.createElement("div");
        message3.textContent = "Press 'p' to run youtube video.";
    
        const message4 = document.createElement("div");
        message4.textContent = "Press 'q' to quit.";
        // Append messages to the wrapper
        wrapper.appendChild(message1);
        wrapper.appendChild(message2);
        wrapper.appendChild(message3);
        wrapper.appendChild(message4);
    
        return wrapper;
    },

    handleKeyPress: function(event) {
        console.log(`Key pressed: ${event.key}`); // Log the key pressed
        if (event.key === "f") { // If "s" is pressed
            this.runFaceRecognitionScript(); // Call the function to run the face recognition script
            this.hideMirror();
        }
        if (event.key === "o") { // If "s" is pressed
            this.runobjectdetectionScript(); // Call the function to run the face recognition script
            this.hideMirror();
        }
    },

    runFaceRecognitionScript: function() {
        // Hide the MagicMirror screen
        this.hideMirror();

        // Send a notification to the Node helper to run the Python script
        this.sendSocketNotification('RUN_SCRIPT');
    },
    runobjectdetectionScript: function() {
        // Hide the MagicMirror screen
        this.hideMirror();

        // Send a notification to the Node helper to run the Python script
        this.sendSocketNotification('RUN_SCRIPT2');
    },


    hideMirror: function() {
        const mirrorContainer = document.querySelector(".mirror-container");
        if (mirrorContainer) {
            mirrorContainer.style.display = "none"; // Hide the mirror container
            console.log("Mirror hidden."); // Log when the mirror is hidden
        }
    },

    showMirror: function() {
        const mirrorContainer = document.querySelector(".mirror-container");
        if (mirrorContainer) {
            mirrorContainer.style.display = "block"; // Show the mirror container
            console.log("Mirror shown."); // Log when the mirror is shown
        }
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === 'SCRIPT_COMPLETED') {
            // Show the MagicMirror screen again
            this.showMirror();
        }
    },
});


// Module.register("MMM-FaceRecognition", {
//     defaults: {
//         wsUrl: "ws://localhost:8888" // WebSocket server address (Python script WebSocket server)
//     },

//     start: function() {
//         console.log("MMM-FaceRecognition: Starting module");
//         document.addEventListener('keydown', this.handleKeyPress.bind(this)); // Bind the event listener
//         this.connectWebSocket(); // Establish WebSocket connection
//     },

//     getDom: function() {
//         const wrapper = document.createElement("div");
//         wrapper.innerHTML = `
//             <p>Press 's' to run the face recognition script.</p>
//             <div id="video-container" style="display:none;">
//                 <img id="video-feed" style="width:100%;height:auto;"/>
//             </div>
//         `;
//         return wrapper;
//     },

//     handleKeyPress: function(event) {
//         console.log(`Key pressed: ${event.key}`); // Log the key pressed
//         if (event.key === "s") { // If "s" is pressed
//             this.runFaceRecognitionScript(); // Call the function to run the face recognition script
//         }
//     },

//     runFaceRecognitionScript: function() {
//         // Hide the MagicMirror screen and show the video feed
//         this.hideMirror();
//         this.showVideoFeed();

//         // Send a notification to the Node helper to run the Python script
//         this.sendSocketNotification('RUN_SCRIPT');
//     },

//     hideMirror: function() {
//         const mirrorContainer = document.querySelector(".mirror-container");
//         if (mirrorContainer) {
//             mirrorContainer.style.display = "none"; // Hide the mirror container
//             console.log("Mirror hidden."); // Log when the mirror is hidden
//         }
//     },

//     showMirror: function() {
//         const mirrorContainer = document.querySelector(".mirror-container");
//         if (mirrorContainer) {
//             mirrorContainer.style.display = "block"; // Show the mirror container
//             console.log("Mirror shown."); // Log when the mirror is shown
//         }

//         // Hide the video feed when showing the mirror again
//         this.hideVideoFeed();
//     },

//     showVideoFeed: function() {
//         const videoContainer = document.getElementById("video-container");
//         if (videoContainer) {
//             videoContainer.style.display = "block"; // Show the video feed
//             console.log("Video feed shown.");
//         }
//     },

//     hideVideoFeed: function() {
//         const videoContainer = document.getElementById("video-container");
//         if (videoContainer) {
//             videoContainer.style.display = "none"; // Hide the video feed
//             console.log("Video feed hidden.");
//         }
//     },

//     connectWebSocket: function() {
//         const socket = new WebSocket(this.config.wsUrl);

//         // Event listener for WebSocket open event
//         socket.onopen = () => {
//             console.log("WebSocket connection established.");
//         };

//         // Event listener for WebSocket message event (receiving the video frame)
//         socket.onmessage = (event) => {
//             const imageElement = document.getElementById("video-feed");
//             if (imageElement) {
//                 imageElement.src = `data:image/jpeg;base64,${event.data}`; // Set the received base64 image as source
//             }
//         };

//         // Event listener for WebSocket close event
//         socket.onclose = () => {
//             console.log("WebSocket connection closed.");
//         };

//         // Event listener for WebSocket error event
//         socket.onerror = (error) => {
//             console.error("WebSocket error:", error);
//         };
//     },

//     socketNotificationReceived: function(notification, payload) {
//         if (notification === 'SCRIPT_COMPLETED') {
//             // Show the MagicMirror screen again after the script completes
//             this.showMirror();
//         }
//     },
// });

