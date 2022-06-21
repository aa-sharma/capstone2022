const canvas = document.getElementById("canvas1");
import * as THREE from 'three';
import { OrbitControls } from 'OrbitControls';

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 500 );
camera.position.set( 3, 2, 30 );
camera.lookAt( 0, 0, 0 );

const axesHelper = new THREE.AxesHelper(10);
scene.add(axesHelper)


//create a blue LineBasicMaterial
const material = new THREE.LineBasicMaterial( { color: 0x6AA1CB, linewidth: 10 } );
const points = [];
points.push( new THREE.Vector3( - 10, 0, 0 ) );
points.push( new THREE.Vector3( 0, 10, 0 ) );
points.push( new THREE.Vector3( 10, 0, 0 ) );

const geometry = new THREE.BufferGeometry().setFromPoints( points );
const line = new THREE.Line( geometry, material );
scene.add( line );


function animate() {
    requestAnimationFrame( animate );
    line.rotation.x += 0.01; 
    line.rotation.y += 0.01;
    renderer.render( scene, camera );  
}


animate()
