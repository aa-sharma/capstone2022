import { SERVER_BASE_URL } from "../modules/constants.js";
import API from "../modules/api.js";
import Render from "../modules/render/render.js";
import Toast from "../modules/toast.js";

const token = localStorage["token"];
const exerciseId = localStorage["exerciseId"];
let timer = null;
const startLevelButton = document.getElementById("start-level");
const stopLevelButton = document.getElementById("stop-level");
const expectedPositionHeader = document.getElementById(
  "expectedPositionHeader"
);
const toast = new Toast();

// initilize socketio
const socket = io(SERVER_BASE_URL, {
  auth: { "x-auth-token": token },
  transports: ["websocket"],
});

// fetch expected exercise from database
const api = new API({ url: `/api/exercise/${exerciseId}`, token });
const { json: expectedExercise } = await api.call();

// populate dom with the exercise
const populateLevel = document.getElementById("level");
populateLevel.innerHTML = `
  <header>
    <h1 class="display-4">LEVEL ${expectedExercise.level}</h1>
    <p class="fw-bold mb-0">Exercise ${expectedExercise.exerciseNumber}</p>
    <p class="fw-light mb-0">${expectedExercise.description}</p>
  </header>
`;

// THREEJS initilize rendering
let startingPosition = [];
let finalPosition = [];
setTimeout(() => {
  console.log(startingPosition);
  if (startingPosition.length == 0) {
    toast.display({
      level: "error",
      title: "Error Connecting Hardware",
      msg: "There was an error connecting your hardware. Check to make sure product key is set, and hardware is turned on!",
    });
  }
}, 2000);
const expectedPosition = document.getElementById("expectedPosition");
const actualPosition = document.getElementById("actualPosition");

const actualRender = new Render({ element: actualPosition });
const expectedRender = new Render({
  element: expectedPosition,
  pointColor: 0x45ba6d,
});
actualRender.animate();
expectedRender.animate();

// declare socketio events and emitions
socket.emit("fetch_expected_position", expectedExercise);

startLevelButton.addEventListener("click", (ev) => {
  socket.emit("fetch_expected_position", expectedExercise);
  toast.display({
    level: "success",
    title: "Initial Position",
    msg: "Please position your hand in the initial position",
  });
  expectedPositionHeader.innerText = "Initial Position";
  socket.emit("user_start_exercise", expectedExercise);
  clearInterval(timer);
});

stopLevelButton.addEventListener("click", (ev) => {
  toast.display({
    level: "error",
    title: "Stopped Exercise",
    msg: "User requested to halt the exercise",
  });
  socket.emit("user_stop_exercise");
  clearInterval(timer);
});

socket.on("data_processor_start_exercise", () => {
  toast.display({
    level: "success",
    title: "Starting Exercise",
    msg: "Starting exercise in 3 seconds!",
  });

  expectedPositionHeader.innerText = "Final Position";

  for (const key in finalPosition) {
    expectedRender.move(key, finalPosition[key]);
  }
  expectedRender.render();

  const minutesLabel = document.getElementById("minutes");
  const secondsLabel = document.getElementById("seconds");
  const milasecondsLabel = document.getElementById("milaseconds");
  // start timer after 3 seconds
  setTimeout(() => {
    let totalMilaseconds = 0;
    timer = setInterval(() => {
      totalMilaseconds += 100;
      milasecondsLabel.innerText = pad(totalMilaseconds % 1000, 3);
      secondsLabel.innerText = pad(parseInt(totalMilaseconds / 1000) % 60, 2);
      minutesLabel.innerText = pad(parseInt(totalMilaseconds / 60000), 2);
    }, 100);
  }, 3000);
});

function pad(val, length) {
  let valString = String(val);
  for (let i = 0; i < length; i++) {
    console.log(valString.length);
    if (valString.length < length) {
      valString = "0" + valString;
    } else {
      return valString;
    }
  }
  return valString;
}

socket.on("exercise_completed", (message) => {
  if (message.error) {
    toast.display({
      level: "error",
      title: "Error Creating User Progress Rport",
      msg: message.error,
    });
  } else {
    toast.display({
      level: "success",
      title: "Completed Exercise",
      msg: `Successfully Completed Exercise!\nAgility Score: ${message.agilityScore}\nDexterity Score: ${message.dexterityScore}\nOverall Score: ${message.overallScore}`,
    });
  }
  clearInterval(timer);
});

socket.on("python_client_connected", () => {
  socket.emit("fetch_expected_position", expectedExercise);
  expectedPositionHeader.innerText = "Initial Position";
});

socket.on("receive_actual_position", (xyzDict) => {
  for (const key in xyzDict) {
    const { x, y, z } = xyzDict[key];
    actualRender.move(key, { x, y, z });
  }
  actualRender.render();
});

socket.on("receive_expected_position", (startingAndFinalPosition) => {
  startingPosition = startingAndFinalPosition[0];
  finalPosition = startingAndFinalPosition[1];

  for (const key in startingPosition) {
    expectedRender.move(key, startingPosition[key]);
  }
  expectedRender.render();
});

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
