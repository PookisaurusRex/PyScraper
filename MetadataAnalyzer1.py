import json  
import matplotlib.pyplot as plt  
  
def SpeciesPopulationVisualizer(file_path):  
   with open(file_path, 'r') as f:  
      data = json.load(f)  
  
   # Extract data from JSON  
   timestamps = [entry['timestamp'] for entry in data]  
   species_data = [entry['species'] for entry in data]  
  
   # Create a figure and axis  
   fig, ax = plt.subplots(figsize=(10, 6))  
  
   # Add per-species details  
   species_ids = set()  
   for i, species in enumerate(species_data):  
      for specie in species:  
        species_ids.add(specie['id'])  
  
   for species_id in species_ids:  
      species_sizes = []  
      species_timestamps = []  
  
      for i, species in enumerate(species_data):  
        for specie in species:  
           if specie['id'] == species_id:  
              species_sizes.append(specie['size'])  
              species_timestamps.append(timestamps[i])  
  
      ax.plot(species_timestamps, species_sizes, label=f'Species {species_id}')  
  
   ax.set_title('Species Populations over Time')  
   ax.set_xlabel('Timestamp')  
   ax.set_ylabel('Population')  
   ax.legend()  
  
   # Show the plot  
   plt.tight_layout()  
   plt.show()  
  
# Example usage  
file_path = 'population_info_20241028_183538.json'  
SpeciesPopulationVisualizer(file_path)