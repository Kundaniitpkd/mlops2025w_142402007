import toml
import torch

def load_training_config(config_path="./config/training_config.toml"):
    return toml.load(config_path)

def get_optimizer(optimizer_name, model_params, learning_rate, momentum=None):
    if optimizer_name.lower() == "adam":
        return torch.optim.Adam(model_params, lr=learning_rate)
    elif optimizer_name.lower() == "sgd":
        return torch.optim.SGD(model_params, lr=learning_rate, momentum=momentum)

def save_model_results(model_results, file_path="model_best_parameters.txt"):
    with open(file_path, "w") as f:
        f.write("MODEL-WISE BEST HYPERPARAMETERS\n")
        f.write("=" * 50 + "\n\n")
        
        for model_name, best_params in model_results.items():
            f.write(f"MODEL: {model_name.upper()}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Best Accuracy: {best_params['accuracy']:.2f}%\n")
            f.write(f"Learning Rate: {best_params['learning_rate']}\n")
            f.write(f"Optimizer: {best_params['optimizer']}\n")
            f.write(f"Momentum: {best_params['momentum']}\n")
            f.write("\n")
        
        f.write("=" * 50 + "\n")

def save_overall_best(best_params, file_path="overall_best.txt"):
    with open(file_path, "w") as f:
        f.write("OVERALL BEST HYPERPARAMETERS\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Best Model: {best_params['model']}\n")
        f.write(f"Best Accuracy: {best_params['accuracy']:.2f}%\n")
        f.write(f"Learning Rate: {best_params['learning_rate']}\n")
        f.write(f"Optimizer: {best_params['optimizer']}\n")
        f.write(f"Momentum: {best_params['momentum']}\n")
        f.write("\n" + "=" * 40 + "\n")