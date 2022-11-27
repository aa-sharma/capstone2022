import { sockets } from "../../../server/src/websockets/ws-server.js";
import Render from "./render/render.js";

// const serverAddress = "ws://127.0.0.1:5002";
// const serverConnection = new WebSocket(serverAddress);

// serverConnection.onopen = function () {
//   console.log(
//     new Date() + "[Client]: JS client connected to server " + serverAddress
//   );
//   serverConnection.send(
//     "This is JS (hand-model) client. Connected to server " + serverAddress
//   );
// };
// serverConnection.onclose = function () {
//   console.log(
//     new Date() +
//       "[Client]: JS client (hand-model) disconnecting from server " +
//       serverAddress
//   );
//   serverConnection.send(
//     "This is JS (hand-model) client. Disconnecting from server " + serverAddress
//   );
// };

// serverConnection.onmessage = function (event) {
//   if (event.data instanceof Blob) {
//     var reader = new FileReader();

//     reader.onload = () => {
//       console.log(
//         "[Client]: Received message from server (parsed): " + reader.result
//       );
//       let obj = JSON.parse(reader.result);
//       target = obj;
//       console.log(target);
//     };
//     reader.readAsText(event.data);
//   } else {
//     console.log(
//       "[Client]: Received message from server (not-parsed): " + event.data
//     );
//     console.log(event.data);
//   }
// };
const render = new Render();
render.animate();

sockets.on("python_client_data", (xyzDict) => {
  for (key in xyzDict) {
    render.move(key, xyzDict[key]);
  }
});

// render.move("thumbPointA", { x: 1, y: 9, z: 2 });
// render.move("thumbPointB", { x: 1, y: 7, z: 1 });
// render.move("thumbPointC", { x: 2, y: 5, z: 0 });
// render.move("indexPointD", { x: 3, y: 7, z: 0 });
// render.move("indexPointC", { x: 3, y: 10, z: 2 });
// render.move("indexPointB", { x: 3, y: 12, z: 4 });
// render.move("indexPointA", { x: 3, y: 13, z: 6.5 });
// render.move("middlePointD", { x: 5, y: 7, z: 0 });
// render.move("middlePointC", { x: 5, y: 10, z: 2 });
// render.move("middlePointB", { x: 5, y: 12.5, z: 4 });
// render.move("middlePointA", { x: 5, y: 14, z: 6.5 });
// render.move("ringPointD", { x: 7, y: 7, z: 0 });
// render.move("ringPointC", { x: 7, y: 10, z: 2 });
// render.move("ringPointB", { x: 7, y: 12, z: 4 });
// render.move("ringPointA", { x: 7, y: 13, z: 6.5 });
// render.move("pinkyPointD", { x: 9, y: 6, z: 0 });
// render.move("pinkyPointC", { x: 9, y: 7.5, z: 1.5 });
// render.move("pinkyPointB", { x: 9, y: 9, z: 3 });
// render.move("pinkyPointA", { x: 9, y: 10, z: 5 });
// render.move("palmA", { x: 3, y: 1, z: 0 });
// render.move("thumbD", { x: 8, y: 1, z: 0 });
