const WebSocket = require('ws');

//localhost:PORT
const serverAddress = "ws://127.0.0.1:5000";

const ws = new WebSocket(serverAddress);

//if not using localhost, uncomment below with wanted browser
// const ws = new WebSocket(serverAddress, {
//     headers: {
//         "user-agent": "Mozilla"
//     }
// });


ws.on('open', function() {
    ws.send("[CLIENT] Hello Server!");
})

ws.on('message', function(msg) {
    console.log( (new Date()) + ": Message from server: " + msg);
})