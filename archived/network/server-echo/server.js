const WebSocket = require("ws");
const { v4: uuidv4 } = require("uuid");
const WeakMap = require("weak-map");
const { uuid } = require("uuidv4");

const PORT = 5050;
const socketMap = new WeakMap();

//start server
const wsServer = new WebSocket.Server({ port: PORT });
console.log(new Date() + ": [INFO] Starting WebSocket server on port " + PORT);

const client_uuids = {};

// callback function upon establishing connection
wsServer.on("connection", function (socket, req) {
  // assign uuid to connecting client
  socket.uuid = uuidv4();

  const ip = req.socket.remoteAddress;
  console.log(
    new Date() + ": [INFO] Client connection established with IP: " + ip
  );
  socketMap.set(socket, socket.uuid);

  var i = 0;
  wsServer.clients.forEach(function (client) {
    console.log(
      new Date() + ": [INFO] Client " + i + " | UUID : " + client.uuid
    );
    client_uuids.i = client.uuid;
    i = i + 1;
  });
  console.log(client_uuids);

  socket.on("message", function (msg) {
    console.log(
      new Date() + ": [INFO] Message received from Client ID: " + socket.uuid
    );
    console.log(new Date() + ": [INFO] Message:\n\n" + msg + "\n\n");
    //Broadcast to all connected clients
    wsServer.clients.forEach(function (client) {
      client.send(msg);
    });
  });

  socket.on("userStartsExercise", function (msg) {
    socket.emit("userStartsExercise", msg, onlyToCorrectPythonClient);
  });
  socket.on("positionUpdate", function (msg) {
    socket.emit("positionUpdate", msg, correctWebClient);
  });
  socket.on("message", function (msg) {});
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
