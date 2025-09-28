#import torch
import torch.nn as nn
from itertools import product
import json

from src.data_loader import MNISTDataLoader
from src.model_factory import ModelFactory
from src.trainer import Trainer
from src.utils import load_training_config, get_optimizer, save_model_results, save_overall_best

def main():
    # Load configurations
    training_config = load_training_config()
    data_loader = MNISTDataLoader()
    train_loader, test_loader = data_loader.get_dataloaders()
    
    # Load available models from JSON
    with open("./config/data_config.json", "r") as f:
        data_config = json.load(f)
    available_models = data_config["model_architecture"]["available_models"]
    
    # Get hyperparameters from TOML
    learning_rates = training_config["hyperparameters"]["learning_rates"]
    optimizers = training_config["hyperparameters"]["optimizers"]
    momentums = training_config["hyperparameters"]["momentums"]
    
    # Track results
    model_best_results = {}
    overall_best_accuracy = 0
    overall_best_params = {}
    
    total_experiments = len(available_models) * len(learning_rates) * len(optimizers) * len(momentums)
    print(f"Starting ML Pipeline - {total_experiments} experiments")
    print(f"Models: {available_models}")
    
    experiment_count = 0
    
    # Test each model with all hyperparameter combinations
    for model_name in available_models:
        print(f"\nTesting {model_name.upper()}")
        model_best_accuracy = 0
        model_best_params = {}
        
        for lr, opt_name, momentum in product(learning_rates, optimizers, momentums):
            experiment_count += 1
            print(f"  Exp {experiment_count}/{total_experiments}: LR={lr}, Opt={opt_name}, Mom={momentum}", end=" -> ")
            
            # Create and train model
            model_factory = ModelFactory()
            model = model_factory.get_model(model_name, training_config["training"]["num_classes"])
            trainer = Trainer(model, training_config["training"]["device"])
            
            optimizer = get_optimizer(opt_name, model.parameters(), lr, momentum)
            criterion = nn.CrossEntropyLoss()
            
            trainer.train(train_loader, optimizer, criterion, training_config["training"]["epochs"])
            accuracy = trainer.evaluate(test_loader, criterion)
            
            print(f"{accuracy:.2f}%")
            
            # Update best for this model
            if accuracy > model_best_accuracy:
                model_best_accuracy = accuracy
                model_best_params = {
                    "model": model_name,
                    "accuracy": accuracy,
                    "learning_rate": lr,
                    "optimizer": opt_name,
                    "momentum": momentum
                }
            
            # Update overall best
            if accuracy > overall_best_accuracy:
                overall_best_accuracy = accuracy
                overall_best_params = model_best_params.copy()
        
        # Store best result for this model
        model_best_results[model_name] = model_best_params
        print(f"  {model_name} Best: {model_best_accuracy:.2f}%")
    
    # Save results to files
    save_model_results(model_best_results, training_config["grid_search"]["model_results_file"])
    save_overall_best(overall_best_params, training_config["grid_search"]["overall_best_file"])
    
    # Print final summary
    print(f"\n{'='*50}")
    print("FINAL RESULTS:")
    print(f"{'='*50}")
    for model_name, params in model_best_results.items():
        print(f"{model_name}: {params['accuracy']:.2f}% (LR: {params['learning_rate']}, {params['optimizer']})")
    
    print(f"\nOverall Winner: {overall_best_params['model']} - {overall_best_params['accuracy']:.2f}%")
    print("Results saved to:")
    print(f"  - {training_config['grid_search']['model_results_file']}")
    print(f"  - {training_config['grid_search']['overall_best_file']}")

if __name__ == "__main__":
    main()