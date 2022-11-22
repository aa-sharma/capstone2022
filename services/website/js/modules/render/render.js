import * as THREE from "./three.module.js";
import { OrbitControls } from "./OrbitControls.js";

class Render {
  constructor() {
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(this.renderer.domElement);
    this.renderer.setPixelRatio(window.devicePixelRatio);

    this.scene = new THREE.Scene();

    this.camera = new THREE.PerspectiveCamera(
      30,
      window.innerWidth / window.innerHeight,
      1,
      500
    );

    this.camera.position.set(-20, 35, 75);
    this.camera.lookAt(0, 0, 0);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.addEventListener("change", this.__render);

    this.__setResizing(this.renderer, this.scene, this.camera);
    this.__setPlane();
    this.__setGrid();
    this.__setLighting();

    this.lines = [];
    const pointGeometry = new THREE.SphereGeometry(0.5, 25, 25);
    const pointMaterial = new THREE.MeshPhysicalMaterial({ color: 0xd41c00 });

    const handPoints = [
      "pinkyPointA",
      "pinkyPointB",
      "pinkyPointC",
      "pinkyPointD",
      "ringPointA",
      "ringPointB",
      "ringPointC",
      "ringPointD",
      "middlePointA",
      "middlePointB",
      "middlePointC",
      "middlePointD",
      "indexPointA",
      "indexPointB",
      "indexPointC",
      "indexPointD",
      "thumbPointA",
      "thumbPointB",
      "thumbPointC",
      "wristPointO",
      "wristPointW",
    ];

    this.handModel = {};
    handPoints.map((e) => {
      this.handModel[e] = new THREE.Mesh(pointGeometry, pointMaterial);
      this.handModel[e].position.set(0, 0, 0);
      this.scene.add(this.handModel[e]);
    });
  }

  move(point, position) {
    this.handModel[point].position.x = position.x;
    this.handModel[point].position.y = position.y;
    this.handModel[point].position.z = position.z;
    this.__render();
  }

  animate() {
    requestAnimationFrame(this.animate.bind(this));
    this.__render();
  }

  __setGrid() {
    const grid = new THREE.GridHelper(100, 100, 0x0fd000, 0x000000);
    grid.material.opacity = 0.1;
    grid.material.transparent = true;
    this.scene.add(grid);
    const axesHelper = new THREE.AxesHelper(100);
    this.scene.add(axesHelper);
  }

  __setPlane() {
    //ground
    const planeGeometry = new THREE.PlaneGeometry(80, 50);
    const planeMaterial = new THREE.MeshPhongMaterial({
      color: 0x999999,
      depthWrite: false,
    });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.rotation.x = -Math.PI / 2;
    plane.receiveShadow = true;
    this.scene.add(plane);
  }

  __setLighting() {
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
    hemiLight.position.set(0, 20, 0);
    this.scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffffff);
    dirLight.position.set(0, 2, 1);
    dirLight.castShadow = true;
    dirLight.shadow.camera.top = 18;
    dirLight.shadow.camera.bottom = -10;
    dirLight.shadow.camera.left = -12;
    dirLight.shadow.camera.right = 12;
    this.scene.add(dirLight);
    this.renderer.setClearColor(0xfffffffff);
  }

  __setResizing(renderer, scene, camera) {
    // automatic resize
    window.addEventListener("resize", onWindowResize, false);
    function onWindowResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.render(scene, camera);
    }
  }

  __setLines() {
    const material = new THREE.LineBasicMaterial({ color: 0x000000 });
    const connections = [
      ["pinkyPointA", "pinkyPointB"],
      ["pinkyPointB", "pinkyPointC"],
      ["pinkyPointC", "pinkyPointD"],
      ["pinkyPointD", "ringPointD"],
      ["ringPointA", "ringPointB"],
      ["ringPointB", "ringPointC"],
      ["ringPointC", "ringPointD"],
      ["ringPointD", "middlePointD"],
      ["middlePointA", "middlePointB"],
      ["middlePointB", "middlePointC"],
      ["middlePointC", "middlePointD"],
      ["middlePointD", "indexPointD"],
      ["indexPointA", "indexPointB"],
      ["indexPointB", "indexPointC"],
      ["indexPointC", "indexPointD"],
      ["indexPointD", "thumbPointC"],
      ["thumbPointA", "thumbPointB"],
      ["thumbPointB", "thumbPointC"],
      ["thumbPointC", "wristPointW"],
      ["pinkyPointD", "wristPointO"],
      ["wristPointO", "wristPointW"],
    ];

    for (let line of this.lines) {
      this.scene.remove(line);
    }

    for (let connection of connections) {
      const points = [];
      for (let point of connection) {
        points.push(this.handModel[point].position);
      }
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const line = new THREE.Line(geometry, material);
      this.lines.push(line);
      this.scene.add(line);
    }
  }

  __render() {
    try {
      this.__setLines();
      this.renderer.render(this.scene, this.camera);
    } catch (e) {}
  }
}

export default Render;
