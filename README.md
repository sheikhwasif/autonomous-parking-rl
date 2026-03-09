# Autonomous Car Parking using Reinforcement Learning

## Overview
This project implements an autonomous car parking system using Reinforcement Learning.  
A custom simulation environment was created where an RL agent learns how to navigate and park a vehicle inside a designated parking space.

The agent was trained for **3,000,000 timesteps** using multiple variants of the **Proximal Policy Optimization (PPO)** algorithm.

The goal is to learn optimal steering and movement strategies while avoiding collisions and minimizing positioning error.

---

## Algorithms Implemented

This project explores different PPO configurations:

- **PPO (Discrete Action Space)**  
  The agent selects from predefined steering and movement actions.

- **PPO Continuous**  
  The agent outputs continuous control values such as steering angle and throttle.

- **PPO MultiDiscrete**  
  A combination of multiple discrete actions representing different vehicle controls.

These approaches allow comparison between **discrete and continuous control strategies for autonomous vehicle parking**.

---

## Environment

A custom **Gymnasium-based parking environment** was developed.

The agent must:

- Navigate a vehicle within a parking lot
- Avoid collisions with boundaries
- Align correctly with the parking slot
- Minimize distance and orientation error

### State Space
The observation space includes:

- Vehicle position
- Vehicle orientation
- Distance to parking slot
- Relative position to boundaries

### Action Space

Depending on the model:

- Steering
- Acceleration
- Braking

---

## Training

The models were trained using **Stable-Baselines3 PPO**.

Training duration:
