const canvas = document.getElementById("canvas1");
import * as THREE from './three.js-master/build/three.module.js';
import { OrbitControls } from './three.js-master/examples/jsm/controls/OrbitControls.js'

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 500 );
const orbit = new OrbitControls(camera, renderer.domElement);

camera.position.set( 0, 15, 40 );
camera.lookAt( 0, 0, 0 );
orbit.update();

const axesHelper = new THREE.AxesHelper(100);
scene.add(axesHelper);

const hemiLight = new THREE.HemisphereLight (0xffffff, 0x444444)
hemiLight.position.set(0, 20, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xfffffff);
dirLight.position.set (0, 2, 1);
dirLight.castShadow = true;
dirLight.shadow.camera.top = 18;
dirLight.shadow.camera.bottom = -10;
dirLight.shadow.camera.left = -12;
dirLight.shadow.camera.right = 12;
scene.add(dirLight)

//scene.add(new THREE.CameraHelper(dirLight.shadow.camera));

renderer.setClearColor(0xfffffffff);

//ground
const planeGeometry = new THREE.PlaneGeometry (80, 50);
const planeMaterial = new THREE.MeshPhongMaterial({
    color: 0x999999,
    depthWrite: false
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial)
plane.rotation.x = - Math.PI / 2;
plane.receiveShadow = true;
scene.add(plane);

const grid = new THREE.GridHelper(80, 50, 0x0fd000, 0x000000);
grid.material.opacity = 0.1;
grid.material.transparent = true;
scene.add(grid);


const material = new THREE.LineBasicMaterial( { color: 0x6AA1CB, linewidth: 10 } );

//wrist skeleton
const wrist_points = [];
wrist_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB
wrist_points.push( new THREE.Vector3( 0, 0, 0 ) );        //wristA
wrist_points.push( new THREE.Vector3( -4, 0, 0 ) );       //wristC
wrist_points.push( new THREE.Vector3( -4, -8, 0 ) );      //wristE
wrist_points.push( new THREE.Vector3( 4, -8, 0 ) );       //wristD
wrist_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB

const wrist_geometry = new THREE.BufferGeometry().setFromPoints( wrist_points );
const wrist_line = new THREE.Line( wrist_geometry, material );
scene.add( wrist_line );

//thumb skeleton
const thumb_points = [];
thumb_points.push( new THREE.Vector3( -4, 1, 0 ) );        //wristB
thumb_points.push( new THREE.Vector3( -6, 3.5, 0 ) );        //wristA
thumb_points.push( new THREE.Vector3( -7, 6, 0 ) );       //wristC

const thumb_geometry = new THREE.BufferGeometry().setFromPoints( thumb_points );
const thumb_line = new THREE.Line( thumb_geometry, material );
scene.add( thumb_line );

//index finger skeleton
const index_points = [];
index_points.push( new THREE.Vector3( -3, 7, 0 ) );        //wristB
index_points.push( new THREE.Vector3( -4, 10, 0 ) );        //wristA
index_points.push( new THREE.Vector3( -5, 13, 0 ) );       //wristC

const index_geometry = new THREE.BufferGeometry().setFromPoints( index_points );
const index_line = new THREE.Line( index_geometry, material );
scene.add( index_line );

//middle finger skeleton
const middle_points = [];
middle_points.push( new THREE.Vector3( 0, 8, 0 ) );        //wristB
middle_points.push( new THREE.Vector3( 0, 12, 0 ) );        //wristA
middle_points.push( new THREE.Vector3( 0, 16, 0 ) );       //wristC

const middle_geometry = new THREE.BufferGeometry().setFromPoints( middle_points );
const middle_line = new THREE.Line( middle_geometry, material );
scene.add( middle_line );

//ring finger skeleton
const ring_points = [];
ring_points.push( new THREE.Vector3( 2.5, 7.5, 0 ) );        //wristB
ring_points.push( new THREE.Vector3( 3, 10, 0 ) );        //wristA
ring_points.push( new THREE.Vector3( 3.5, 14, 0 ) );       //wristC

const ring_geometry = new THREE.BufferGeometry().setFromPoints( ring_points );
const ring_line = new THREE.Line( ring_geometry, material );
scene.add( ring_line );

//pinky finger skeleton
const pinky_points = [];
pinky_points.push( new THREE.Vector3( 4, 5, 0 ) );        //wristB
pinky_points.push( new THREE.Vector3( 4.9, 8, 0 ) );        //wristA
pinky_points.push( new THREE.Vector3( 5.5, 11, 0 ) );       //wristC

const pinky_geometry = new THREE.BufferGeometry().setFromPoints( pinky_points );
const pinky_line = new THREE.Line( pinky_geometry, material );
scene.add( pinky_line );

//palm skeleton
const palm_points = [];
palm_points.push( new THREE.Vector3( -4, 0, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( -4, 1, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( -3, 7, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( 0, 8, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( 2.5, 7.5, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( 4, 5, 0 ) );        //wristB
palm_points.push( new THREE.Vector3( 4, 0, 0 ) );        //wristB

const palm_geometry = new THREE.BufferGeometry().setFromPoints( palm_points );
const palm_line = new THREE.Line( palm_geometry, material );
scene.add( palm_line );


// function animate() {
//     requestAnimationFrame( animate );
//     //line.rotation.x += 0.01; 
//     thumb_line.rotation.y += 0.1;
//     renderer.render( scene, camera );
//     orbit.update();
// }
// animate();

var targetPositionX = 6;

function animate(){
    // render the scene
    renderer.render(scene, camera);
    // Check the object's X position
    if (thumb_line.position.x <= targetPositionX) {
        thumb_line.position.x += 0.1; // You decide on the increment, higher value will mean the objects moves faster
    }
    // call the loop function again
    requestAnimationFrame(animate);
}
animate();

// automatic resize
window.addEventListener('resize', function() {
    camera.aspect = this.window.innerWidth / this.window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
})

