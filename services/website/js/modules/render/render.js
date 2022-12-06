import * as THREE from "./three.module.js";
import { OrbitControls } from "./OrbitControls.js";

class Render {
  constructor({ element, pointColor }) {
    this.__pointColor = pointColor || 0xd41c00;
    this.element = element;
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(this.element.offsetWidth, this.element.offsetHeight);
    this.element.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();

    this.camera = new THREE.PerspectiveCamera(
      5,
      window.innerWidth / window.innerHeight,
      1,
      3000
    );

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.addEventListener("change", this.render);
    this.camera.position.set(-90, 30, 300);

    this.__setResizing(this.renderer, this.scene, this.camera, this.element);
    this.__setGrid();
    this.__setLighting();
    this.lines = [];
    const pointGeometry = new THREE.SphereGeometry(0.2, 25, 25);
    const pointMaterial = new THREE.MeshPhysicalMaterial({
      color: this.__pointColor,
    });

    const handPoints = [
      "pinkyA",
      "pinkyB",
      "pinkyC",
      "pinkyD",
      "ringA",
      "ringB",
      "ringC",
      "ringD",
      "middleA",
      "middleB",
      "middleC",
      "middleD",
      "indexA",
      "indexB",
      "indexC",
      "indexD",
      "thumbA",
      "thumbB",
      "thumbC",
      "thumbD",
      "palmA",
    ];

    this.handModel = {};
    handPoints.map((point) => {
      this.handModel[point] = new THREE.Mesh(pointGeometry, pointMaterial);
      this.handModel[point].position.set(0, 0, 0);
      this.scene.add(this.handModel[point]);
    });
  }

  move(point, position) {
    this.handModel[point].position.x = position.x;
    this.handModel[point].position.y = position.y;
    this.handModel[point].position.z = position.z;
  }

  setPointColor(point, pointColor) {
    const pointMaterial = new THREE.MeshPhysicalMaterial({
      color: pointColor,
    });

    this.handModel[point].material = pointMaterial;
  }

  animate() {
    requestAnimationFrame(this.animate.bind(this));
    this.render();
  }

  __setGrid() {
    const grid = new THREE.GridHelper(100, 100, "black", "black");
    grid.material.opacity = 0.1;
    grid.material.transparent = true;
    this.scene.add(grid);
  }

  __setLighting() {
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
    this.scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffffff);
    this.scene.add(dirLight);
    this.renderer.setClearColor(0xffffff);
    const axesHelper = new THREE.AxesHelper(50);
    this.scene.add(axesHelper);
  }

  __setResizing(renderer, scene, camera, element) {
    // automatic resize
    window.addEventListener("resize", onWindowResize, false);
    function onWindowResize() {
      camera.aspect = element.offsetWidth / element.offsetHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(element.offsetWidth, element.offsetHeight);
      renderer.render(scene, camera);
    }
  }

  __setLines() {
    const material = new THREE.LineBasicMaterial({ color: 0x000000 });
    const connections = [
      ["pinkyA", "pinkyB"],
      ["pinkyB", "pinkyC"],
      ["pinkyC", "pinkyD"],
      ["pinkyA", "ringA"],
      ["ringA", "ringB"],
      ["ringB", "ringC"],
      ["ringC", "ringD"],
      ["ringA", "middleA"],
      ["middleA", "middleB"],
      ["middleB", "middleC"],
      ["middleC", "middleD"],
      ["middleA", "indexA"],
      ["indexA", "indexB"],
      ["indexB", "indexC"],
      ["indexC", "indexD"],
      ["indexA", "thumbB"],
      ["thumbA", "thumbB"],
      ["thumbB", "thumbC"],
      ["thumbC", "thumbD"],
      ["pinkyA", "palmA"],
      ["thumbA", "palmA"],
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

  render() {
    try {
      this.__setLines();
      this.camera.lookAt(6, 6, 0);

      this.renderer.render(this.scene, this.camera);
    } catch (e) {}
  }
}

export default Render;
