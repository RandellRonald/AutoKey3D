import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Configuration
const API_URL = 'http://localhost:8000'; // Adjust if needed

// State
let currentKeyId = null;
let scene, camera, renderer, controls;
let keyMesh = null;

// DOM Elements
const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const statusDiv = document.getElementById('status');
const canvasContainer = document.getElementById('canvas-container');

// Initialize 3D Scene
function initScene() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x333333); // Neutral dark gray

    // Camera
    const aspect = canvasContainer.clientWidth / canvasContainer.clientHeight;
    camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 100);
    camera.position.set(0, 0, 50); // Zoom out to see the key (22mm length)

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight);
    canvasContainer.appendChild(renderer.domElement);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
    backLight.position.set(-10, -5, -10);
    scene.add(backLight);

    // Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    // Handle Window Resize
    window.addEventListener('resize', () => {
        const newAspect = canvasContainer.clientWidth / canvasContainer.clientHeight;
        camera.aspect = newAspect;
        camera.updateProjectionMatrix();
        renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight);
    });
}

function loadSTL(url) {
    const loader = new STLLoader();

    // Remove old mesh
    if (keyMesh) {
        scene.remove(keyMesh);
        if (keyMesh.geometry) keyMesh.geometry.dispose();
        if (keyMesh.material) keyMesh.material.dispose();
        keyMesh = null;
    }

    loader.load(
        url,
        function (geometry) {
            // Center geometry
            geometry.center();

            // Material - Gold for visibility
            const material = new THREE.MeshStandardMaterial({
                color: 0xD4AF37,
                metalness: 0.8,
                roughness: 0.3
            });

            keyMesh = new THREE.Mesh(geometry, material);

            // Adjust rotation to face camera nicely
            keyMesh.rotation.x = -Math.PI / 2;
            keyMesh.rotation.z = Math.PI / 2; // Flat and horizontal

            scene.add(keyMesh);

            // Fit camera to object (Optional, but good UX)
            // const box = new THREE.Box3().setFromObject(keyMesh);
            // ... logic to fit ...
        },
        (xhr) => {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        (error) => {
            console.error('An error happened', error);
            statusDiv.textContent = "Error loading 3D model.";
        }
    );
}

// Check API availability
async function checkApi() {
    try {
        // Just checking if we can fetch something, e.g. /docs or just implicit
        statusDiv.textContent = "System Ready";
    } catch {
        statusDiv.textContent = "API Offline";
    }
}

// Event Listeners
generateBtn.addEventListener('click', async () => {
    generateBtn.disabled = true;
    downloadBtn.disabled = true;
    statusDiv.innerHTML = '<span class="spinner"></span> Generating...';

    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Success
        currentKeyId = data.key_id;
        const stlUrl = `${API_URL}/${data.stl_url}`;

        statusDiv.textContent = `Generated Key ID: ${currentKeyId}`;

        // Load 3D
        loadSTL(stlUrl);

        // Enable Download
        downloadBtn.disabled = false;

    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Generation Failed";
    } finally {
        generateBtn.disabled = false;
    }
});

downloadBtn.addEventListener('click', () => {
    if (currentKeyId) {
        window.location.href = `${API_URL}/download/${currentKeyId}`;
    }
});

// Init
initScene();
statusDiv.textContent = "System Ready";

