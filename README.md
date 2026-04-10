# Advanced Ren'Py Parallax Engine

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ren'Py](https://img.shields.io/badge/Ren'Py-FF5A00?style=for-the-badge&logo=renpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Interactive, high-performance parallax scrolling effect custom-built for the Ren'Py visual novel engine. 

https://github.com/user-attachments/assets/efecdd88-54ab-4cac-94c9-0d4f6b21b174

## Key Features
* **Sensor-Based Triggers:** Dynamic visual feedback reacting to game scenes and interactive elements.
* **Anti-Flicker Optimization:** Custom rendering logic optimized to ensure smooth transitions without visual artifacts or screen flickering.
* **Complex Transformations:** Full support for coordinate rotation and deep multi-layering.
* **Performance Focused:** Designed to run smoothly alongside heavy UI and story elements.
* **Native Android Sensor Support**: Unlike standard mouse-driven scripts, this engine hooks directly into Android hardware via `jnius`. It reads raw accelerometer data and applies mathematical smoothing, allowing players to physically tilt their devices to explore the scene.

## The Technical Challenge
Creating a layered parallax effect that doesn't drop frames during complex scenes requires precise calculation. I focused on optimizing coordinate math and refining the core rendering queue, which successfully eliminated the flickering issue common in standard Ren'Py implementations.


