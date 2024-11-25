import json
import os


class Config:
    def __init__(self, path):
        with open(path, 'r') as archivo:
            self.data = json.load(archivo)

    def get_datasets(self):
        return self.data['datasets']

    def get_variable_id(self, dataset_name, variable_name):
        dataset = next((d for d in self.data['datasets'] if d['name'] == dataset_name), None)
        if not dataset:
            raise ValueError(f"Dataset '{dataset_name}' no encontrado.")
        
        variable = next((v for v in dataset['variables'] if v['name'] == variable_name), None)
        if not variable:
            raise ValueError(f"Variable '{variable_name}' no encontrada en el dataset '{dataset_name}'.")
        
        return variable['id']
    
    def get_dataset_path(self, dataset_name, experiment_name, variable_name, variant_label=None):
        dataset = next((d for d in self.data['datasets'] if d['name'] == dataset_name), None)
        if not dataset:
            raise ValueError(f"Dataset '{dataset_name}' no encontrado.")

        variable = next((v for v in dataset['variables'] if v['name'] == variable_name), None)
        if not variable:
            raise ValueError(f"Variable '{variable_name}' no encontrada en el dataset '{dataset_name}'.")

        if not variant_label:
            variant_label = variable['variant_labels'][0]

        experiment = next((e for e in dataset['experiments'] if e['name'] == experiment_name), None)
        if not experiment:
            raise ValueError(f"Experimento '{experiment_name}' no encontrado en el dataset '{dataset_name}'.")

        path_template = dataset['path_template']
        path = path_template.format(
            path=dataset['path'],
            experiment=experiment['path'],
            frequency=variable['frequency'],
            variable=variable['id'],
            variant_label=variant_label
        )
        return path

def get_nc_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.nc')]

