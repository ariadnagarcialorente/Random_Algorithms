# 🎲 Galton Board Experiments — Random Algorithms

This project explores the relationship between **Galton board simulations**, **binomial distributions**, and their **normal approximations**.  
It provides a flexible experimental framework where you can configure and run multiple statistical experiments, visualize results, and analyze convergence and error trends.

---

## 🧩 Project Overview

A **Galton board** (or quincunx) demonstrates the binomial distribution by dropping balls through rows of pegs.  
This project simulates that process computationally and compares:
- Empirical Galton results vs theoretical **Binomial distributions**
- Binomial vs **Normal** distribution approximations
- Error convergence as the number of balls (`N`) and height (`n`) grow

---

## 📁 Folder Structure

```text
Random_Algorithms/
├── config/
│   └── config_galton.yaml         # YAML configuration of experiments and parameters
│
├── results/
│   └── galton/                    # Automatically created output folder for plots
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

## 🧪 Configuration: config/config_galton.yaml

This YAML file defines which experiments to run and their parameters to get the results provided.

---

## 🚀 Running Experiments

```bash
# Run all experiments defined in the YAML
python src/galton/main.py
```

This will:
- Load experiments from `config/config_galton.yaml`
- Execute each experiment
- Save plots to the `results/galton/` folder

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

After running experiments, results are automatically saved in:

```text
results/galton/
```