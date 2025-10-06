import argparse
import yaml
from pathlib import Path

from experiments import EXPERIMENT_REGISTRY

# Project root (three levels up from src/galton/main.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Paths
CONFIG_PATH = PROJECT_ROOT / "config" / "config_galton.yaml"
RESULTS_DIR = PROJECT_ROOT / "results" / "galton"


def parse_args_and_config():
    """
    Parses CLI arguments, loads YAML config, and merges parameter overrides.
    Returns a dict: {exp_name: params} of experiments to run.
    """
    parser = argparse.ArgumentParser(description="Run experiments")
    parser.add_argument("--experiment", "-e", type=str, help="Name of experiment to run (overrides YAML)")
    parser.add_argument("--config", "-c", type=str, default=CONFIG_PATH, help="YAML config path")
    parser.add_argument("--param", "-p", action='append', help="Override a parameter (format: key=value)")
    args = parser.parse_args()

    # Load YAML config
    with open(args.config) as f:
        configs = yaml.safe_load(f)

    # Parse CLI parameter overrides
    cli_params = {}
    if args.param:
        for p in args.param:
            if '=' not in p:
                raise ValueError(f"Invalid parameter override: {p}")
            key, value = p.split('=', 1)
            # Convert to int or float if possible
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # keep as string
            cli_params[key] = value

    # Decide which experiments to run
    experiments_to_run = {}
    if args.experiment:
        if args.experiment not in configs:
            raise ValueError(f"Experiment '{args.experiment}' not found in YAML")
        # Merge YAML and CLI params
        params = {**configs[args.experiment], **cli_params}
        experiments_to_run[args.experiment] = params
    else:
        # Run all experiments, apply CLI overrides if relevant
        for exp_name, yaml_params in configs.items():
            params = {**yaml_params, **cli_params}
            experiments_to_run[exp_name] = params

    return experiments_to_run

def run_experiment(exp_name, params):
    exp_class = EXPERIMENT_REGISTRY[exp_name]
    exp = exp_class(**params)
    exp.run()
    exp.plot(RESULTS_DIR)

def main():
    experiments = parse_args_and_config()
    for exp_name, params in experiments.items():
        print(f"\n--- Running experiment: {exp_name} ---")
        run_experiment(exp_name, params)

if __name__ == "__main__":
    main()
