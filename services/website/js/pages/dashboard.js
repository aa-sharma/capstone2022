import API from "../modules/api.js";

const token = localStorage["token"];

const graphUserLevelProgress = new API({
  url: "/api/user-level-progress?pageSize=1000",
  token,
});
const { json: graphUserLevelProgressJson } =
  await graphUserLevelProgress.call();

const tableUserLevelProgress = new API({
  url: "/api/user-level-progress?pageSize=6",
  token,
});
const { json: tableUserLevelProgressJson } =
  await tableUserLevelProgress.call();

const populateTable = (items) => {
  const table = document.getElementById("table");
  for (const item of items) {
    const tableElement = document.createElement("tr");
    const date = new Date(item.date);
    tableElement.innerHTML = `
      <th scope="row">${date.toString().split(" GMT")[0]}</th>
      <td>Level ${item.exercise.level} Exercise ${
      item.exercise.exerciseNumber
    }</td>
      <td>${item.agilityScore}</td>
      <td>${item.dexterityScore}</td>
      <td>${item.overallScore}</td>
    `;
    table.appendChild(tableElement);
  }
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
    yaxis: { title: "Score", linewidth: 2 },
    title: "Dexterity Score",
  };

  const agilityScoreLayout = {
    xaxis: { title: "Date", linewidth: 2 },
    yaxis: { title: "Score", linewidth: 2 },
    title: "Agility Score",
  };

  const overallScoreLayout = {
    xaxis: { title: "Date", linewidth: 2 },
    yaxis: { title: "Score", linewidth: 2 },
    title: "Overall Score",
  };

  Plotly.newPlot("dexterityScore", [dexterityScoreGraph], dexterityScoreLayout);
  Plotly.newPlot("agilityScore", [agilityScoreGraph], agilityScoreLayout);
  Plotly.newPlot("overallScore", [overallScoreGraph], overallScoreLayout);
};

populateTable(tableUserLevelProgressJson.items);
populateGraph(graphUserLevelProgressJson.items);
