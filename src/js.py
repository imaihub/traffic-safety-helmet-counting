script_new = """
    function connectWebSocket() {
        var ws;
        var imgElement = null;
        var connectionTimeout = 5000; // Timeout in milliseconds
        var requestInterval = 20;
        var isRequestPending = false;
        const videoOutElement = document.getElementById('video_out');
        
        if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
            console.log("WebSocket connection attempt is already underway.");
            return;
        }

        ws = new WebSocket('ws://localhost:5678');
        let hasConnected = false; // Flag to indicate if connection was successful
            
        // Set up a timeout to check if the connection is taking too long
        const timeoutId = setTimeout(() => {
            if (!hasConnected) {
                console.log(`WebSocket connection timed out after ${connectionTimeout} ms.`);
                ws.close(); // Attempt to close the connection if in CONNECTING state
            }
        }, connectionTimeout);

        ws.onopen = function() {
            hasConnected = true; // Set the flag to indicate successful connection
            clearTimeout(timeoutId); // Clear the timeout
            console.log("WebSocket connection established.");
        };

        ws.onmessage = function(event) {
            const frameBase64 = event.data;
            if (frameBase64 === "finished") {
                let videoOutElement = document.getElementById('video_out')[1];
                let videoDiv = videoOutElement.getElementsByTagName("div");
                while(videoDiv.firstChild) { 
                    videoDiv.removeChild(videoDiv.firstChild);
                }
                imgElement = null;
                return
            }
            if (!imgElement) {
                imgElement = document.createElement('img');
                imgElement.style.maxWidth = '100%';
            
                if (videoOutElement) {
                    const videoDiv = videoOutElement.getElementsByTagName("div")[1];
                    videoDiv.appendChild(imgElement);
                }
            }
            imgElement.src = `data:image/jpeg;base64,${frameBase64}`;
        };

        ws.onclose = function() {
            console.log("WebSocket connection closed. Attempting to reconnect...");
            setTimeout(connectWebSocket, 1000); // Retry connection after a short delay
        };

        ws.onerror = function(error) {
            console.error("WebSocket error:", error);
            ws.close(); // Close the WebSocket connection on error
        };
    }
"""
