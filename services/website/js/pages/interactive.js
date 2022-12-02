import { SERVER_BASE_URL } from "../modules/constants.js";
import API from "../modules/api.js";
import Render from "../modules/render/render.js";

const token = localStorage["token"];
const exerciseId = localStorage["exerciseId"];

const socket = io(SERVER_BASE_URL, {
  auth: { "x-auth-token": token },
  transports: ["websocket"],
});

const api = new API({ url: `/api/exercise/${exerciseId}`, token });
const { json } = await api.call();

const populateLevel = document.getElementById("level");
populateLevel.innerHTML = `
  <header>
    <h1 class="display-4">LEVEL ${json.level}</h1>
    <p class="fw-bold mb-0">Exercise ${json.exerciseNumber}</p>
    <p class="fw-light mb-0">${json.description}</p>
  </header>
`;

// THREEJS Rendering
const expectedPosition = document.getElementById("expectedPosition");
const actualPosition = document.getElementById("actualPosition");

const actualRender = new Render({ element: actualPosition });
const expectedRender = new Render({ element: expectedPosition });
actualRender.animate();
expectedRender.animate();

const startLevelButton = document.getElementById("start-level");
const stopLevelButton = document.getElementById("stop-level");

// WEBSOCKETS
socket.on("connect", () => {
  console.log(`Successfully connected websocket server: ${SERVER_BASE_URL}`);
});

socket.on("connect_error", (data) => {
  console.error(
    `Websocket connection to ${SERVER_BASE_URL} failed, with reason: ${data}`
  );
});

socket.on("disconnect", () => {
  console.log(`Disconnected from websocket server: ${SERVER_BASE_URL}`);
});

socket.on("python_client_connected", (data) => {
  console.log(data);
});

socket.on("python_client_data", (xyzDict) => {
  for (const key in xyzDict) {
    actualRender.move(key, xyzDict[key]);
  }
  actualRender.render();
});

startLevelButton.addEventListener("click", (ev) => {
  console.log("start level");
  socket.emit("user_start_exercise", { exercise: json });
});

stopLevelButton.addEventListener("click", (ev) => {
  console.log("stop level");
  socket.emit("user_stop_exercise");
});
