import argparse
import yaml
from pathlib import Path

from experiments import EXPERIMENT_REGISTRY


# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config_galton.yaml"
RESULTS_DIR = PROJECT_ROOT / "results" / "galton"


def parse_args():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Run Galton experiments.")
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=str(DEFAULT_CONFIG),
        help="Path to YAML config file."
    )
    parser.add_argument(
        "--experiment", "-e",
        type=str,
        help="Run only this experiment (name must exist in YAML)."
    )
    parser.add_argument(
        "--param", "-p",
        action="append",
        help="Override parameters, e.g. -p height=15 -p balls=500"
    )
    return parser.parse_args()


def load_config(path: str | Path):
    """
    Load YAML configuration file.
    Expected format:
      experiments:
        galton_binomial:
          - height: 10
            balls: 100
          - height: 15
            balls: 200
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if "experiments" not in cfg:
        raise ValueError("YAML must contain a top-level 'experiments' key.")
    return cfg


def parse_param_overrides(param_list):
    """
    Parse CLI parameter overrides into a dict and infer numeric types.
    """
    params = {}
    if not param_list:
        return params

    for p in param_list:
        if "=" not in p:
            raise ValueError(f"Invalid parameter override format: '{p}'. Expected key=value.")
        key, value = p.split("=", 1)
        # Try to cast to int or float
        try:
            value = float(value) if "." in value else int(value)
        except ValueError:
            pass
        params[key] = value

    return params


def merge_overrides(base_params, overrides):
    """
    Merge base parameters with CLI overrides (CLI takes precedence).
    """
    return {**base_params, **overrides}


def run_experiment(exp_name, params, filename):
    """
    Instantiate and execute a single experiment.
    """
    if exp_name not in EXPERIMENT_REGISTRY:
        raise KeyError(f"Experiment '{exp_name}' not found in registry.")
    exp_cls = EXPERIMENT_REGISTRY[exp_name]
    exp = exp_cls(**params)
    exp.run()
    exp.plot(save_folder=RESULTS_DIR, filename=filename)


def main():
    args = parse_args()
    config = load_config(args.config)
    overrides = parse_param_overrides(args.param)

    experiments = config["experiments"]

    if args.experiment:
        if args.experiment not in experiments:
            raise ValueError(f"Experiment '{args.experiment}' not found in YAML.")
        selected = {args.experiment: experiments[args.experiment]}
    else:
        selected = experiments

    for exp_name, runs in selected.items():
        if not isinstance(runs, list):
            runs = [runs]
        for run_idx, params in enumerate(runs, start=1):
            merged = merge_overrides(params, overrides)
            print(f"▶ Running {exp_name} (run {run_idx}) with params: {merged}")
            run_experiment(exp_name, merged, f"{exp_name}_{run_idx}")


if __name__ == "__main__":
    main()
