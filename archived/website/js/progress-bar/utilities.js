//==================Gauge==================
function createCircleChart(percent, color, size, stroke) {
  let svg = `<svg class="mkc_circle-chart" viewbox="0 0 36 36" width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
        <path class="mkc_circle-bg" stroke="#eeeeee" stroke-width="${
          stroke * 0.5
        }" fill="none" d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"/>
        <path class="mkc_circle" stroke="${color}" stroke-width="${stroke}" stroke-dasharray="${percent},100" stroke-linecap="round" fill="none"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831" />
        <text class="mkc_info" x="50%" y="50%" alignment-baseline="central" text-anchor="middle" font-size="8">${percent}%</text>
    </svg>`;
  return svg;
}

let charts = document.getElementsByClassName("mkCharts");

for (let i = 0; i < charts.length; i++) {
  let chart = charts[i];
  let percent = chart.dataset.percent;
  let color = "color" in chart.dataset ? chart.dataset.color : "#2F4F4F";
  let size = "size" in chart.dataset ? chart.dataset.size : "100";
  let stroke = "stroke" in chart.dataset ? chart.dataset.stroke : "1";
  charts[i].innerHTML = createCircleChart(percent, color, size, stroke);
}

//==================Timer==================
var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var totalSeconds = 0;
setInterval(setTime, 1000);

function setTime() {
  ++totalSeconds;
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
}

function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}

// //==================Battery (Progress Bar)==================
// import ProgressBar from "progressbar.js";

// var bar = new ProgressBar.Line(batteryContainer, {
//   strokeWidth: 4,
//   easing: "easeInOut",
//   duration: 1400,
//   color: "#FFEA82",
//   trailColor: "#eee",
//   trailWidth: 1,
//   svgStyle: { width: "100%", height: "100%" },
//   from: { color: "#FFEA82" },
//   to: { color: "#ED6A5A" },
//   step: (state, bar) => {
//     bar.path.setAttribute("stroke", state.color);
//   },
// });

// bar.animate(1.0); // Number from 0.0 to 1.0
