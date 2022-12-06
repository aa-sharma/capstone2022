import API from "../modules/api.js";

const token = localStorage["token"];
let progressPage = 1;

const graphUserLevelProgress = new API({
  url: "/api/user-level-progress?pageSize=100000",
  token,
});
const { json: graphUserLevelProgressJson } =
  await graphUserLevelProgress.call();

const populateTable = (items) => {
  const table = document.getElementById("table");
  const previousTableBody = document.getElementById("table-body");
  if (previousTableBody) {
    table.removeChild(previousTableBody);
  }
  const tableBody = document.createElement("tbody");
  tableBody.id = "table-body";

  for (const item of items) {
    const tableRow = document.createElement("tr");
    const date = new Date(item.date);
    tableRow.innerHTML = `
      <th scope="row">${date.toString().split(" GMT")[0]}</th>
      <td>Level ${item.exercise.level} Exercise ${
      item.exercise.exerciseNumber
    }</td>
      <td>${item.agilityScore}</td>
      <td>${item.dexterityScore}</td>
      <td>${item.overallScore}</td>
    `;
    tableBody.appendChild(tableRow);
  }
  table.appendChild(tableBody);
};

const navigateNextPage = async () => {
  progressPage += 1;
  const nextPage = document.getElementById("next-page");
  const currentPage = document.getElementById("current-page").firstElementChild;
  const previousPage = document.getElementById("previous-page");

  const tableUserLevelProgress = new API({
    url: `/api/user-level-progress?pageSize=6&page=${progressPage}`,
    token,
  });
  const { json } = await tableUserLevelProgress.call();
  console.log(json.items);
  if (json.page == progressPage) {
    currentPage.innerText = progressPage;
    populateTable(json.items);
  } else {
    progressPage -= 1;
    nextPage.classList.add("disabled");
    nextPage.removeEventListener("click", navigateNextPage);
  }

  if (progressPage != 1) {
    previousPage.classList.remove("disabled");
    previousPage.addEventListener("click", navigatePreviousPage);
  }
};

const navigatePreviousPage = async () => {
  progressPage -= 1;
  const nextPage = document.getElementById("next-page");
  const currentPage = document.getElementById("current-page").firstElementChild;
  const previousPage = document.getElementById("previous-page");

  const tableUserLevelProgress = new API({
    url: `/api/user-level-progress?pageSize=6&page=${progressPage}`,
    token,
  });
  const { json } = await tableUserLevelProgress.call();

  currentPage.innerText = progressPage;
  populateTable(json.items);
  nextPage.classList.remove("disabled");
  nextPage.addEventListener("click", navigateNextPage);

  if (progressPage == 1) {
    previousPage.classList.add("disabled");
    previousPage.removeEventListener("click", navigatePreviousPage);
  }
};

const initNavigateTable = async () => {
  const nextPage = document.getElementById("next-page");

  const tableUserLevelProgress = new API({
    url: `/api/user-level-progress?pageSize=6&page=${progressPage}`,
    token,
  });
  const { json } = await tableUserLevelProgress.call();
  populateTable(json.items);

  nextPage.addEventListener("click", navigateNextPage);
};

const populateGraph = (items) => {
  const dexterityScoreGraph = {
    x: [],
    y: [],
    hovertext: [],
    hoverinfo: "text+y",
    type: "scatter",
    line: {
      color: "blue",
    },
  };

  const agilityScoreGraph = {
    x: [],
    y: [],
    hovertext: [],
    hoverinfo: "text+y",
    type: "scatter",
    line: {
      color: "red",
    },
  };

  const overallScoreGraph = {
    x: [],
    y: [],
    hovertext: [],
    hoverinfo: "text+y",
    type: "scatter",
    line: {
      color: "green",
    },
  };
  const itemsByDateAscending = items.reverse();

  for (const idx in itemsByDateAscending) {
    const index = Number(idx) + 1;
    let date = new Date(itemsByDateAscending[idx].date);
    date = date.toString().split(" GMT")[0];
    dexterityScoreGraph.x.push(index);
    dexterityScoreGraph.y.push(itemsByDateAscending[idx].dexterityScore);
    dexterityScoreGraph.hovertext.push(date);
    agilityScoreGraph.x.push(index);
    agilityScoreGraph.y.push(itemsByDateAscending[idx].agilityScore);
    agilityScoreGraph.hovertext.push(date);
    overallScoreGraph.x.push(index);
    overallScoreGraph.y.push(itemsByDateAscending[idx].overallScore);
    overallScoreGraph.hovertext.push(date);
  }

  const dexterityScoreLayout = {
    xaxis: { title: "Date", linewidth: 2 },
    yaxis: { title: "Score", linewidth: 2, range: [-0.5, 10.5] },
    title: "Dexterity Score",
  };

  const agilityScoreLayout = {
    xaxis: { title: "Date", linewidth: 2 },
    yaxis: { title: "Score", linewidth: 2, range: [-0.5, 10.5] },
    title: "Agility Score",
  };

  const overallScoreLayout = {
    xaxis: { title: "Date", linewidth: 2 },
    yaxis: { title: "Score", linewidth: 2, range: [-0.5, 10.5] },
    title: "Overall Score",
  };

  Plotly.newPlot("dexterityScore", [dexterityScoreGraph], dexterityScoreLayout);
  Plotly.newPlot("agilityScore", [agilityScoreGraph], agilityScoreLayout);
  Plotly.newPlot("overallScore", [overallScoreGraph], overallScoreLayout);
};

initNavigateTable();
populateGraph(graphUserLevelProgressJson.items);
