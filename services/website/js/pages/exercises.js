import API from "../modules/api.js";

const addRedirect = (element, exerciseId) => {
  for (let button of element.children) {
    if (button.tagName.toLowerCase() === "button") {
      button.addEventListener("click", () => {
        localStorage["exerciseId"] = exerciseId;
        window.location.assign("./interactive.html");
      });
    }
  }
};

const token = localStorage["token"];

const api = new API({ url: "/api/exercise?pageSize=20", token });
const { json } = await api.call();

let level = 0;
for (const exercise of json.items) {
  const exercises = document.getElementById("exercises");
  if (exercise.level > level) {
    const populateLevel = document.createElement("div");
    populateLevel.innerHTML = `
    <div class="col-12 mx-auto">
      <div class="mb-4">
        <header class="text-center ms-1">
          <h1 class="display-5">Level ${exercise.level}</h1>
        </header>
      </div>
    </div>
    `;
    exercises.appendChild(populateLevel);
    level = exercise.level;
  }

  const populateExercise = document.createElement("div");
  populateExercise.classList.add(
    "col-lg-3",
    "col-md-6",
    "text-center",
    "mt-2",
    "mb-5"
  );
  populateExercise.innerHTML = `
  <div class="d-inline-block">
    <img
      src="../img/exsc-icon.png"
      class="rounded-circle"
      alt=""
      style="width: 300px; height: 300px"
    />
    <h5 class="text-uppercase">Exercise ${exercise.exerciseNumber}</h5>
    <p class="text-muted font-weight-light">${exercise.description}</p>
    <button type="button" class="btn btn-primary mr-3">
      START
    </button>
  </div> 
  `;
  addRedirect(populateExercise.firstElementChild, exercise._id);

  exercises.appendChild(populateExercise);
}
