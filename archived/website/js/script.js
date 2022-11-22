const canvas = document.getElementById("canvas1");
import * as THREE from "./three.js-master/build/three.module.js";

//GLOBAL VARS
var line, pointsPinky;
var lineGeom;

let target = {
  1: { x: 0, y: 0, z: 0 },
  2: { x: 0, y: 0, z: 0 },
  3: { x: 0, y: 0, z: 0 },
  4: { x: 0, y: 0, z: 0 },
};
console.log(target);

// ======================================== WEBSOCKETS ===========================================
const serverAddress = "ws://127.0.0.1:5002";
const serverConnection = new WebSocket(serverAddress);

serverConnection.onopen = function () {
  console.log(
    new Date() + "[Client]: JS client connected to server " + serverAddress
  );
  serverConnection.send(
    "This is JS (hand-model) client. Connected to server " + serverAddress
  );
};
serverConnection.onclose = function () {
  console.log(
    new Date() +
      "[Client]: JS client (hand-model) disconnecting from server " +
      serverAddress
  );
  serverConnection.send(
    "This is JS (hand-model) client. Disconnecting from server " + serverAddress
  );
};

serverConnection.onmessage = function (event) {
  if (event.data instanceof Blob) {
    var reader = new FileReader();

    reader.onload = () => {
      console.log(
        "[Client]: Received message from server (parsed): " + reader.result
      );
      let obj = JSON.parse(reader.result);
      target = obj;
      console.log(target);
    };
    reader.readAsText(event.data);
  } else {
    console.log(
      "[Client]: Received message from server (not-parsed): " + event.data
    );
    console.log(event.data);
  }
};

// ======================================== SETUP SCENE ===========================================

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
renderer.setPixelRatio(window.devicePixelRatio);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  30,
  window.innerWidth / window.innerHeight,
  1,
  500
);

camera.position.set(1, 35, 75);
camera.lookAt(0, 0, 0);

document.addEventListener("mousewheel", (event) => {
  camera.position.z += event.deltaY / 200;
});

const axesHelper = new THREE.AxesHelper(100);
scene.add(axesHelper);

const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
hemiLight.position.set(0, 20, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xfffffff);
dirLight.position.set(0, 2, 1);
dirLight.castShadow = true;
dirLight.shadow.camera.top = 18;
dirLight.shadow.camera.bottom = -10;
dirLight.shadow.camera.left = -12;
dirLight.shadow.camera.right = 12;
scene.add(dirLight);

//scene.add(new THREE.CameraHelper(dirLight.shadow.camera));

renderer.setClearColor(0xfffffffff);

//ground
const planeGeometry = new THREE.PlaneGeometry(80, 50);
const planeMaterial = new THREE.MeshPhongMaterial({
  color: 0x999999,
  depthWrite: false,
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.receiveShadow = true;
scene.add(plane);

const grid = new THREE.GridHelper(100, 100, 0x0fd000, 0x000000);
grid.material.opacity = 0.1;
grid.material.transparent = true;
scene.add(grid);

renderer.render(scene, camera);

// automatic resize
window.addEventListener("resize", onWindowResize, false);
function onWindowResize() {
  camera.aspect = this.window.innerWidth / this.window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.render(scene, camera);
}

// ======================================== HAND-MODEL ===========================================

var pointGeometry = new THREE.SphereGeometry(0.5, 25, 25);
var pointMaterial = new THREE.MeshPhysicalMaterial({ color: 0xd41c00 });

//meshPinkyPoint.position.x = 0;
// Pinky
var meshPinkyPointA = new THREE.Mesh(pointGeometry, pointMaterial);
meshPinkyPointA.position.set(0, 0, 0);

var meshPinkyPointB = new THREE.Mesh(pointGeometry, pointMaterial);
meshPinkyPointB.position.set(0, 0, 0);

var meshPinkyPointC = new THREE.Mesh(pointGeometry, pointMaterial);
meshPinkyPointC.position.set(0, 0, 0);

var meshPinkyPointD = new THREE.Mesh(pointGeometry, pointMaterial);
meshPinkyPointD.position.set(0, 0, 0);
scene.add(meshPinkyPointA, meshPinkyPointB, meshPinkyPointC, meshPinkyPointD);

// Ring
var meshRingPointA = new THREE.Mesh(pointGeometry, pointMaterial);
meshRingPointA.position.set(0, 0, 0);

var meshRingPointB = new THREE.Mesh(pointGeometry, pointMaterial);
meshRingPointB.position.set(0, 0, 0);

var meshRingPointC = new THREE.Mesh(pointGeometry, pointMaterial);
meshRingPointC.position.set(0, 0, 0);

var meshRingPointD = new THREE.Mesh(pointGeometry, pointMaterial);
meshRingPointD.position.set(0, 0, 0);
scene.add(meshRingPointA, meshRingPointB, meshRingPointC, meshRingPointD);

// Middle
var meshMiddlePointA = new THREE.Mesh(pointGeometry, pointMaterial);
meshMiddlePointA.position.set(0, 0, 0);

var meshMiddlePointB = new THREE.Mesh(pointGeometry, pointMaterial);
meshMiddlePointB.position.set(0, 0, 0);

var meshMiddlePointC = new THREE.Mesh(pointGeometry, pointMaterial);
meshMiddlePointC.position.set(0, 0, 0);

var meshMiddlePointD = new THREE.Mesh(pointGeometry, pointMaterial);
meshMiddlePointD.position.set(0, 0, 0);
scene.add(
  meshMiddlePointA,
  meshMiddlePointB,
  meshMiddlePointC,
  meshMiddlePointD
);

// Index
var meshIndexPointA = new THREE.Mesh(pointGeometry, pointMaterial);
meshIndexPointA.position.set(0, 0, 0);

var meshIndexPointB = new THREE.Mesh(pointGeometry, pointMaterial);
meshIndexPointB.position.set(0, 0, 0);

var meshIndexPointC = new THREE.Mesh(pointGeometry, pointMaterial);
meshIndexPointC.position.set(0, 0, 0);

var meshIndexPointD = new THREE.Mesh(pointGeometry, pointMaterial);
meshIndexPointD.position.set(0, 0, 0);
scene.add(meshIndexPointA, meshIndexPointB, meshIndexPointC, meshIndexPointD);

// Thumb
var meshThumbPointA = new THREE.Mesh(pointGeometry, pointMaterial);
meshThumbPointA.position.set(0, 0, 0);

var meshThumbPointB = new THREE.Mesh(pointGeometry, pointMaterial);
meshThumbPointB.position.set(0, 0, 0);

var meshThumbPointC = new THREE.Mesh(pointGeometry, pointMaterial);
meshThumbPointC.position.set(0, 0, 0);

var meshThumbPointD = new THREE.Mesh(pointGeometry, pointMaterial);
meshThumbPointD.position.set(0, 0, 0);
scene.add(meshThumbPointA, meshThumbPointB, meshThumbPointC, meshThumbPointD);

// Wrist
var meshWristPointO = new THREE.Mesh(pointGeometry, pointMaterial);
meshWristPointO.position.set(0, 0, 0);

var meshWristPointW = new THREE.Mesh(pointGeometry, pointMaterial);
meshWristPointW.position.set(0, 0, 0);
scene.add(meshWristPointO, meshWristPointW);

// console.log(meshPinkyPointA.position);
// console.log(meshPinkyPointB.position);

var pointsPinky = [];
pointsPinky.push(
  meshPinkyPointA.position,
  meshPinkyPointB.position,
  meshPinkyPointC,
  meshPinkyPointD
); //[ (x,y,z), (x,y,z), (x,y,z), (x,y,z) ]

var lineGeom = new THREE.BufferGeometry().setFromPoints(pointsPinky);
var lineMat = new THREE.LineBasicMaterial({
  color: 0x6aa1cb,
  linewidth: 2,
});
var line = new THREE.Line(lineGeom, lineMat);
line.geometry.attributes.position.needsUpdate = true;

scene.add(line);
line.geometry.attributes.position.needsUpdate = true;

var speed = 0.5;

// Utilities
const obj_value = (obj, path) =>
  path
    .replace(/\[|\]\.?/g, ".")
    .split(".")
    .filter((s) => s)
    .reduce((acc, val) => acc && acc[val], obj);

function sleep(delay) {
  var start = new Date().getTime();
  while (new Date().getTime() < start + delay);
}

function animate() {
  // requestAnimationFrame(animate);

  // TODO: Improve this later by using a switch statement for this condition and looping through the points
  if (meshPinkyPointA.position.x < obj_value(target, "1.x")) {
    meshPinkyPointA.position.x += speed;
  } else if (meshPinkyPointA.position.x > obj_value(target, "1.x")) {
    meshPinkyPointA.position.x -= speed;
  }

  if (meshPinkyPointA.position.y < obj_value(target, "1.y")) {
    meshPinkyPointA.position.y += speed;
  } else if (meshPinkyPointA.position.y > obj_value(target, "1.y")) {
    meshPinkyPointA.position.y -= speed;
  }

  if (meshPinkyPointA.position.z < obj_value(target, "1.z")) {
    meshPinkyPointA.position.z += speed;
  } else if (meshPinkyPointA.position.z > obj_value(target, "1.z")) {
    meshPinkyPointA.position.z -= speed;
  }
  //   console.log(meshPinkyPointA.position);

  if (meshPinkyPointB.position.x < obj_value(target, "2.x")) {
    meshPinkyPointB.position.x += speed;
  } else if (meshPinkyPointB.position.x > obj_value(target, "2.x")) {
    meshPinkyPointB.position.x -= speed;
  }

  if (meshPinkyPointB.position.y < obj_value(target, "2.y")) {
    meshPinkyPointB.position.y += speed;
  } else if (meshPinkyPointB.position.y > obj_value(target, "2.y")) {
    meshPinkyPointB.position.y -= speed;
  }

  if (meshPinkyPointB.position.z < obj_value(target, "2.z")) {
    meshPinkyPointB.position.z += speed;
  } else if (meshPinkyPointB.position.z > obj_value(target, "2.z")) {
    meshPinkyPointB.position.z -= speed;
  }
  //   console.log(meshPinkyPointB.position);

  // sleep(100)

  line.geometry.attributes.position.needsUpdate = true;

  //line.geometry.computeBoundingBox();
  //line.geometry.computeBoundingSphere();

  render();
  //console.log(line.geometry.attributes.position)
}

function render() {
  renderer.render(scene, camera);
  line.geometry.attributes.position.needsUpdate = true;
}

render();
animate();

<<<<<<< Updated upstream:archived/website/js/script.js
<<<<<<< Updated upstream:archived/website/js/script.js
//====================== TO BE DELETED ===================================

// var scene, camera, renderer, pointsPinky, line;

// function init() {
//     renderer = new THREE.WebGLRenderer({ antialias: true });
//     renderer.setSize( window.innerWidth, window.innerHeight );
//     document.body.appendChild( renderer.domElement );
//     renderer.setPixelRatio(window.devicePixelRatio)

//     scene = new THREE.Scene();

//     camera = new THREE.PerspectiveCamera(
//         40,
//         window.innerWidth / window.innerHeight,
//         1,
//         500
//     );

//     camera.position.set( 1, 15, 75 );
//     camera.lookAt( 0, 0, 0 );

//     document.addEventListener( 'mousewheel', (event) => {
//         camera.position.z +=event.deltaY/200;
//     });

//     const orbit = new OrbitControls(camera, renderer.domElement);
//     //orbit.update();

//     const axesHelper = new THREE.AxesHelper(100);
//     scene.add(axesHelper);

//     const hemiLight = new THREE.HemisphereLight (0xffffff, 0x444444)
//     hemiLight.position.set(0, 20, 0);
//     scene.add(hemiLight);

//     const dirLight = new THREE.DirectionalLight(0xfffffff);
//     dirLight.position.set (0, 2, 1);
//     dirLight.castShadow = true;
//     dirLight.shadow.camera.top = 18;
//     dirLight.shadow.camera.bottom = -10;
//     dirLight.shadow.camera.left = -12;
//     dirLight.shadow.camera.right = 12;
//     scene.add(dirLight)

//     //scene.add(new THREE.CameraHelper(dirLight.shadow.camera));

//     renderer.setClearColor(0xfffffffff);

//     //ground
//     const planeGeometry = new THREE.PlaneGeometry (80, 50);
//     const planeMaterial = new THREE.MeshPhongMaterial({
//         color: 0x999999,
//         depthWrite: false
//     });
//     const plane = new THREE.Mesh(planeGeometry, planeMaterial)
//     plane.rotation.x = - Math.PI / 2;
//     plane.receiveShadow = true;
//     scene.add(plane);

//     const grid = new THREE.GridHelper(100, 100, 0x0fd000, 0x000000);
//     grid.material.opacity = 0.1;
//     grid.material.transparent = true;
//     scene.add(grid);

//     const material = new THREE.LineBasicMaterial( { color: 0x6AA1CB, linewidth: 2 } );
//     var dotMaterial = new THREE.PointsMaterial({
//         size: 0.5,
//         color: 0x000000
//     });

//     // DATA POINTS - PINKY
//     // Instantiate points (22 of 3 dimensions)
// var pointsPinky = [];
// const pointPinkyA = new THREE.Vector3(4, 5, 5);
// var pointPinkyB = new THREE.Vector3(0, 4, 0);
// var pointPinkyC = new THREE.Vector3(0, 2, 0);
// var pointPinkyD = new THREE.Vector3(0, 0, 0);
// pointsPinky.push(pointPinkyA, pointPinkyB, pointPinkyC, pointPinkyD); //[ (x,y,z), (x,y,z), (x,y,z), (x,y,z) ]
// var lineGeometryPinky = new THREE.BufferGeometry().setFromPoints( pointsPinky );

// //Draw SEGMENT
// var linePinky = new THREE.Line(
//     lineGeometryPinky,
//     material
// );
// scene.add(linePinky)

//     //Draw POINTS
//     var dotGeometryPinkyA = new THREE.BufferGeometry();
//     dotGeometryPinkyA.setAttribute('position',new THREE.Float32BufferAttribute(pointPinkyA, 3));
//     var dotPinkyA = new THREE.Points(dotGeometryPinkyA, dotMaterial);
//     scene.add(dotPinkyA)

//     var dotGeometryPinkyB = new THREE.BufferGeometry();
//     dotGeometryPinkyB.setAttribute('position',new THREE.Float32BufferAttribute(pointPinkyB, 3));
//     var dotPinkyB = new THREE.Points(dotGeometryPinkyB, dotMaterial);
//     scene.add(dotPinkyB)

//     var dotGeometryPinkyC = new THREE.BufferGeometry();
//     dotGeometryPinkyC.setAttribute('position',new THREE.Float32BufferAttribute(pointPinkyC, 3));
//     var dotPinkyC = new THREE.Points(dotGeometryPinkyC, dotMaterial);
//     scene.add(dotPinkyC)

//     var dotGeometryPinkyD = new THREE.BufferGeometry();
//     dotGeometryPinkyD.setAttribute('position',new THREE.Float32BufferAttribute(pointPinkyD, 3));
//     var dotPinkyD = new THREE.Points(dotGeometryPinkyD, dotMaterial);
//     scene.add(dotPinkyD)

//     // DATA POINTS - RING
//     // Instantiate points (22 of 3 dimensions)
//     var pointsRing = [];
//     var pointRingA = new THREE.Vector3(4, 5, 10);
//     var pointRingB = new THREE.Vector3(5, 1, 11);
//     var pointRingC = new THREE.Vector3(6, 2, 0);
//     var pointRingD = new THREE.Vector3(10, 3, 0);
//     pointsRing.push(pointRingA, pointRingB, pointRingC, pointRingD)
//     var lineGeometryRing = new THREE.BufferGeometry().setFromPoints( pointsRing );

//     //Draw SEGMENT
//     var lineRing = new THREE.Line(
//         lineGeometryRing,
//         material
//     );
//     scene.add(lineRing)

//     //Draw POINTS
//     var dotGeometryRing = new THREE.BufferGeometry();
//     dotGeometryRing.setAttribute(
//         'position',
//         new THREE.Float32BufferAttribute(pointRingA, 3)
//     );
//     var dotRing = new THREE.Points(dotGeometryRing, dotMaterial);
//     scene.add(dotRing)

//     //===============================================================================================

//     //wrist skeleton
//     const wrist_points = [];
//     wrist_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB
//     wrist_points.push( new THREE.Vector3( 0, 0, 0 ) );        //wristA
//     wrist_points.push( new THREE.Vector3( -4, 0, 0 ) );       //wristC
//     wrist_points.push( new THREE.Vector3( -4, -8, 0 ) );      //wristE
//     wrist_points.push( new THREE.Vector3( 4, -8, 0 ) );       //wristD
//     wrist_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB

//     const wrist_geometry = new THREE.BufferGeometry().setFromPoints( wrist_points );
//     const wrist_line = new THREE.Line( wrist_geometry, material );
//     //scene.add( wrist_line );

//     //thumb skeleton
//     const thumb_points = [];
//     thumb_points.push( new THREE.Vector3( -4, 1, 0 ) );        //wristB
//     thumb_points.push( new THREE.Vector3( -6, 3.5, 0 ) );        //wristA
//     thumb_points.push( new THREE.Vector3( -7, 6, 0 ) );       //wristC

//     const thumb_geometry = new THREE.BufferGeometry().setFromPoints( thumb_points );
//     const thumb_line = new THREE.Line( thumb_geometry, material );
//     //scene.add( thumb_line );

//     //index finger skeleton
//     const index_points = [];
//     index_points.push( new THREE.Vector3( -3, 7, 0 ) );        //wristB
//     index_points.push( new THREE.Vector3( -4, 10, 0 ) );        //wristA
//     index_points.push( new THREE.Vector3( -5, 13, 0 ) );       //wristC

//     const index_geometry = new THREE.BufferGeometry().setFromPoints( index_points );
//     const index_line = new THREE.Line( index_geometry, material );
//     //scene.add( index_line );

//     //middle finger skeleton
//     const middle_points = [];
//     middle_points.push( new THREE.Vector3( 0, 8, 0 ) );        //wristB
//     middle_points.push( new THREE.Vector3( 0, 12, 0 ) );        //wristA
//     middle_points.push( new THREE.Vector3( 0, 16, 0 ) );       //wristC

//     const middle_geometry = new THREE.BufferGeometry().setFromPoints( middle_points );
//     const middle_line = new THREE.Line( middle_geometry, material );
//     //scene.add( middle_line );

//     //ring finger skeleton
//     const ring_points = [];
//     ring_points.push( new THREE.Vector3( 2.5, 7.5, 0 ) );        //wristB
//     ring_points.push( new THREE.Vector3( 3, 10, 0 ) );        //wristA
//     ring_points.push( new THREE.Vector3( 3.5, 14, 0 ) );       //wristC

//     const ring_geometry = new THREE.BufferGeometry().setFromPoints( ring_points );
//     const ring_line = new THREE.Line( ring_geometry, material );
//     //scene.add( ring_line );

//     //pinky finger skeleton
//     const pinky_points = [];
//     pinky_points.push( new THREE.Vector3( 4, 5, 0 ) );        //wristB
//     pinky_points.push( new THREE.Vector3( 4.9, 8, 0 ) );        //wristA
//     pinky_points.push( new THREE.Vector3( 5.5, 11, 0 ) );       //wristC

//     const pinky_geometry = new THREE.BufferGeometry().setFromPoints( pinky_points );
//     const pinky_line = new THREE.Line( pinky_geometry, material );
//     //scene.add( pinky_line );

//     //palm skeleton
//     const palm_points = [];
//     palm_points.push( new THREE.Vector3( -4, 0, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( -4, 1, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( -3, 7, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( 0, 8, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( 2.5, 7.5, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( 4, 5, 0 ) );        //wristB
//     palm_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB

//     const palm_geometry = new THREE.BufferGeometry().setFromPoints( palm_points );
//     const palm_line = new THREE.Line( palm_geometry, material );
//     //scene.add( palm_line );

//     var targetPositionX = 10;
//     //===============================================================================================
//     console.log(pointsPinky[0])
//     console.log(pointsPinky[0].x)
//     console.log(pointsPinky[0].y)
//     console.log(pointsPinky[0].z)

//     console.log(pointsPinky[1])
//     console.log(pointsPinky[2])
//     console.log(pointsPinky[3])

//     console.log(linePinky.position)
//     console.log(linePinky.position.x)
//     console.log(linePinky.position.z)

//     // automatic resize
//     window.addEventListener('resize', onWindowResize, false)
//     function onWindowResize() {
//         camera.aspect = this.window.innerWidth / this.window.innerHeight;
//         camera.updateProjectionMatrix();
//         renderer.setSize(window.innerWidth, window.innerHeight);
//         renderer.render(scene, camera)
//     }

//     animate();
// }

// function animate() {
//     // render the scene
//     // Check the object's X position
//     console.log(linePinky.position)

//     if (pointsPinky[0].x < targetPositionX) {
//         pointsPinky[0].x += 1; // You decide on the increment, higher value will mean the objects moves faster
//         console.log(pointsPinky[0])
//     }
//     //call the loop function again
//     requestAnimationFrame(animate);
//     renderer.render(scene, camera)
//     orbit.update()
// }

// init();
=======
>>>>>>> Stashed changes:services/website/js/hand-model/script.js
=======
>>>>>>> Stashed changes:services/website/js/hand-model/script.js
