# ✈️ Aircraft Design Evaluation System

A simple, interactive web application built with **Flask** to evaluate aircraft designs based on aerodynamic and geometric parameters. Users can enter aircraft design values like wingspan, tip chord, root chord, chassis width, and sweep angle to get performance evaluations using Python-based calculations (converted from MATLAB).

## 🚀 Features

- Input aircraft geometry parameters directly through the web interface
- Calculate performance indicators such as aspect ratio, taper ratio, and wing area
- Visualize design metrics using dynamic plots
- Converted from a legacy MATLAB system to a modern Python + Flask app
- Lightweight and easy to use for academic or prototyping purposes

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Matplotlib
- **Libraries:** NumPy, Pandas

## 🧠 Core Functionalities

- **Parameter Input:** 
  - Wingspan  
  - Tip Chord  
  - Root Chord  
  - Chassis Width  
  - Sweep Angle  

- **Output Calculations:**
  - Wing Area  
  - Aspect Ratio  
  - Taper Ratio  
  - Additional aerodynamic factors

- **Graphical Output:** Generate and display relevant graphs based on inputs

## 🔧 Installation

```bash
git clone https://github.com/Dars-git/Aircraft-Design-Evaluation-System.git
cd Aircraft-Design-Evaluation-System
pip install -r requirements.txt
python app.py
