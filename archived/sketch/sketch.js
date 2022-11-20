//Global params
const EASE_CTRL = 0.1;

//Current point position
let pos = {
  x:0,
  y:0,
};

//Target point position
let target = {
  x:0,
  y:0,
};


function setup() {
  createCanvas(400, 400);
  
  background(0);
  noStroke();
}

function draw() {
  //trail
  fill(0, 15);
  rect(0, 0, width, height);
  
  //point
  fill(255);
  circle(pos.x, pos.y, 20);
  
  //Ease position into target
  pos.x += EASE_CTRL * (target.x - pos.x);
  pos.y += EASE_CTRL * (target.y - pos.y);

}

function mouseClicked() {
  setTarget(mouseX, mouseY);
  sendTargetToServer();
  
  console.log("New target:");
  console.log(target);
}

function setTarget(tx, ty) {
  target = {
    x: tx,
    y: ty
  };
}

function sendTargetToServer() {
    let norm = {
      x: target.x / width,
      y: target.y / height
    }
    //necessary to stringify non-string data to be able to transfer properly over socket (JSON format)
    let str = JSON.stringify(target);
    serverConnection.send(str);
}

//WEBSOCKETS (p5.js specific)
const serverAddress = "ws://127.0.0.1:5000";

const serverConnection = new WebSocket(serverAddress);

serverConnection.onopen = function() {
    console.log( (new Date()) + "[Client]: JS client connected to server " + serverAddress);
    serverConnection.send( "This is JS client. Connected to server " + serverAddress);
}

//NON-BLOB:
// serverConnection.onmessage = function(event) {
//   console.log("Received: " + event.data);
//   let obj = JSON.parse(event.data);
//   obj.x *= width;
//   obj.y *= height;
//   target = obj;
// }


serverConnection.onmessage = function(event) {
  if (event.data instanceof Blob) {
      reader = new FileReader();

      reader.onload = () => {
          //console.log("Result: " + reader.result);
          console.log( "[Client]: Received message from server (parsed): " + reader.result);
          let obj = JSON.parse(reader.result)
          console.log(obj)
          target = obj
      };

      reader.readAsText(event.data);
  } else {
      console.log("[Client]: Received message from server (not-parsed): " + event.data);
      console.log(event.data)
      target = event.data
  }
};