const WebSocket = require('ws');

const PORT = 5000;

//start server
const wsServer = new WebSocket.Server({
    port: PORT
});
console.log( (new Date()) + ": [INFO] Starting WebSocket server on port " + PORT);


// callback function upon establishing connection
wsServer.on('connection', function(socket) {
    const ip = console.log(socket.remoteAddress);
    console.log( (new Date()) + ": [INFO] Client connection established with IP: " + ip);

    socket.on('message', function(msg) {
        console.log( (new Date()) + ": [INFO] Received message from client: " + msg);

        //Broadcast to all connected clients
        wsServer.clients.forEach(function(client) {
            client.send("[SERVER] The following message was received from a client: " + msg)
        });
    });
});