const WebSocket = require('ws');
const { v4: uuidv4 } = require("uuid");
const WeakMap = require("weak-map");

<<<<<<< Updated upstream:archived/network/server-echo/server.js
const PORT = 5002;
=======
const PORT = 5050;
>>>>>>> Stashed changes:network/server-echo/server.js
const socketMap = new WeakMap();

//start server
const wsServer = new WebSocket.Server({ port: PORT });
console.log( (new Date()) + ": [INFO] Starting WebSocket server on port " + PORT);


// callback function upon establishing connection
wsServer.on('connection', function(socket, req) {
    // assign uuid to connecting client
    socket.uuid = uuidv4();
    socketMap.set(socket, socket.uuid);

    const ip = req.socket.remoteAddress
    console.log( (new Date()) + ": [INFO] Client connection established with IP: " + ip);

    socket.on('message', function(msg) {
        console.log( (new Date()) + ": [INFO] Message received from client: " + msg);
        console.log((new Date()) + ": [INFO] Session id: " + socket.uuid);
        //Broadcast to all connected clients
        wsServer.clients.forEach(function(client) {
            client.send(msg)
        });
        // TODO : Get the client message, check if it for broadcast or unicast, check client ID and send
        // the message to only that client. This means all packages coming to the server must have the 
        // first value as either 'unicast' or 'multicast'
    });
});


// PASS MESSAGE TO SPECIFIC CLIENTS
// const wss = new WebSocket.Server({ port: 8080 });
// const idMap = new Map();

// wss.on('connection', function connection(ws) {
//     // create uuid and add to the idMap
//     ws.uuid = uuid();
//     idMap.add(ws.uuid, ws);

//     ws.on('close', function() {
//         // remove from the map
//         idMap.delete(ws.uuid);
//     });

//     ws.on('message', function(info) {
//         try {
//             info = JSON.parse(info);
//             if (info.action = "send") {
//                 let dest = idMap.get(info.targetId);
//                 if (dest) {
//                     dest.send(JSON.stringify({action: "message", sender: ws.uuid, data: info.message}));
//                 }
//             }
//         } catch(e) {
//             console.log("Error processing incoming message", e);
//         }
//     });
// });