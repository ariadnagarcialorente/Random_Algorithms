# 📚 Random Algorithms — Project Index

This repository contains **two independent projects**:

1. **🎲 Galton Board Experiments** — simulations and statistical analysis
2. **⚖️ Balanced Allocations** — experiments on load balancing and the power of choices

Use the quick navigation below to jump directly to each section:

👉 [Galton Board Project](#-galton-board-experiments)

👉 [Balanced Allocations Project](#-balanced-allocations-experiments)

---

## 📁 Folder Structure

```text
Random_Algorithms/
├── config/                        # YAML configurations of experiments and parameters
│   └── config_galton.yaml         
│   └── config_balanced_allocations.yaml  
│
├── results/                        # Automatically created output folder for plots
│   └── galton/                    
│   └── balanced_allocations/                 
│
├── src/
│   └── galton/
│       ├── main.py                # Entry point: runs experiments defined in the YAML or CLI
│       ├── experiments/
│       │   ├── __init__.py        # Registers all available experiments
│       │   ├── base_experiment.py # Common base class for all experiments
│       │   ├── galton_binomial.py # Galton board vs Binomial comparison
│       │   ├── binomial_normal.py # Binomial vs Normal comparison
│       │   └── galton_triangle_matrix.py  # Other Galton-based experiments
│   └── balanced_allocations/
│       ├── main.py   
│       ├── ...
│
└── README.md
```

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/random-algorithms.git
cd random-algorithms

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

# 🎲 Galton Board Experiments

This project explores the relationship between **Galton board simulations**, **binomial distributions**, and their **normal approximations**.
It provides a flexible experimental framework where you can configure and run multiple statistical experiments, visualize results, and analyze convergence and error trends.

---

## 🧩 Project Overview

A **Galton board** (or quincunx) demonstrates the binomial distribution by dropping balls through rows of pegs.
This project simulates that process computationally and compares:

* Empirical Galton results vs theoretical **Binomial distributions**
* Binomial vs **Normal** distribution approximations
* Error convergence as the number of balls (`N`) and height (`n`) grow

---

## 🧪 Configuration: config/config_galton.yaml

This YAML file defines which experiments to run and their parameters.

---

## 🚀 Running Experiments

```bash
# Run all experiments defined in the YAML
python src/galton/main.py
```

This will:

* Load experiments from `config/config_galton.yaml`
* Execute each experiment
* Save plots to the `results/galton/` folder

### Optional run parameters

```bash
# Run only one experiment
python src/galton/main.py -e galton_binomial

# Override a parameter
python src/galton/main.py -e galton_binomial -p balls=5000

# Use a custom YAML config
python src/galton/main.py -c my_custom_config.yaml
```

---

## 📊 Output and Results

Results are saved in:

```text
results/galton/
```

---

---

# ⚖️ Balanced Allocations Experiments

This project analyzes load balancing in the classic **balls-and-bins** model through extensive empirical experimentation. The goal is to study the **gap**

```
Gₙ = maxᵢ Xᵢ(n) − n/m
```

where:

* `n` = number of balls
* `m` = number of bins
* `Xᵢ(n)` = load of bin `i` after placing all balls
* `Gₙ` = maximum deviation from the average load

The project compares several allocation strategies under three different information settings: **absolute**, **batched**, and **partial-information**.


---

## 🧪 Configuration: config/config_balanced_allocations.yaml

This YAML file defines which experiments to run and their parameters. The default experiments and parameters are the ones used at the assignment 2.

---

## 🚀 Running Experiments

```bash
# Run all experiments defined in the YAML
python src/balanced_allocations/main.py
```

This will:

* Load experiments from `config/config_galton.yaml`
* Execute each experiment
* Save plots to the `results/balanced_allocations/` folder

## 📊 Output and Results

Results are saved in:

```text
results/balanced_allocations/
```
