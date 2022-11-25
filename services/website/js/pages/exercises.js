import { SERVER_BASE_URL } from "../modules/constants.js";
import API from "../modules/api.js";

const token = localStorage["token"];

const socket = io(SERVER_BASE_URL, {
  auth: { "x-auth-token": token },
  transports: ["websocket"],
});

const api = new API({ url: "/api/exercise", token });
const { json } = await api.call();

const startLevelButton = document.getElementById("start-level");
const stopLevelButton = document.getElementById("stop-level");

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

startLevelButton.addEventListener("click", (ev) => {
  console.log("start level");
  socket.emit("user_start_exercise", { exercise: json.items[0] });
});

stopLevelButton.addEventListener("click", (ev) => {
  console.log("stop level");
  socket.emit("user_stop_exercise");
});
