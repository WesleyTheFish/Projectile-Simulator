# Projectile Simulator

A lightweight projectile/flight simulator with a Pygame-based animator and simple PID-controlled motion models.

This repository contains a 3D projectile simulation core, a Pygame UI to enter flight parameters and animate the simulation, plotting utilities, and a small test suite.

## What this repo contains

- `src/sim.py` — Core simulation code. Defines `Body`, `Controller`, and `Simulator` classes, the physics integration loop, PID corrections, graphing utilities, and a runnable `run_skydiver_simulation()` entrypoint.
- `src/animate.py` — Pygame-based UI/animation. Lets you enter flight parameters, run a simulation, animate the projectile in a window, and view summary graphs.
- `src/assets/` — Fonts and images used by the Pygame UI (icons, backgrounds, fonts).
- `hardware/` — A collection of Adafruit / microcontroller helper libraries (MPY files). These appear to be support files for hardware or microcontroller builds and are kept separate from the desktop simulator.
- `test/test_sim.py` — Basic tests for the `Body` class and a trivial smoke test. Uses pytest-style asserts.
- `requirements.txt` — Python dependencies used for plotting and animation (matplotlib, pygame, numpy, etc.).

## High-level features implemented

- 3D position, velocity, and angular state for a projectile.
- PID controllers for position (x/y) and orientation (angle) with configurable gains.
- Wind models (constant / random) exposed to the simulator and UI.
- Graphing of position/velocity/acceleration and angle vs time (matplotlib).
- Pygame GUI to enter parameters, run the sim, watch an animation, and view summary stats.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment (optional but recommended):

```powershell
# create venv
python -m venv .venv
# activate
.\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the simulator (starts the Pygame UI / animation):

```powershell
python .\src\sim.py
```

Alternatively, to run the animated UI directly (it imports and calls `animate.animate_sim()` when run as main):

```powershell
python .\src\animate.py
```

4. Run tests (if you have pytest installed):

```powershell
pip install pytest
pytest -q
```

## Languages
- Python
- Circuit Python

## required Packages
- Pygame
- Matplotlib


## Notes for developers

- The physics are implemented in `src/sim.py`. `Simulator.run()` steps until the projectile's z (height) <= 0. The `net_accel()` function composes gravitational, drag, wind, and controller-derived forces.
- `animate.py` contains many UI helpers and expects assets (images, fonts) in `src/assets/`.
- The `hardware/` folder contains many `.mpy` Adafruit helper files — these are not required to run the desktop simulator but are likely useful for embedded/board builds.

## Next steps / suggested improvements

- Add more unit tests (integration tests for `Simulator.run()` with deterministic inputs).
- Improve documentation of configurable parameters and expected units (meters, seconds, degrees).
- Update forces to be dependant on projectiles velocity 

## Authors
- Wesley Bass