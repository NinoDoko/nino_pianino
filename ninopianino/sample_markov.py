markov_values = [
    [0.1, 0.05, 0.15, 0.1, 0.15, 0.1, 0.1, 0.05, 0.015, 0.05, 0.015, 0.05, 0.03, 0.02, 0.02],
    [0.1, 0.05, 0.05, 0.1, 0.2, 0.15, 0.05, 0.05, 0.02, 0.05, 0.02, 0.03, 0.04, 0.04, 0.05],
    [0.1, 0.05, 0.05, 0.1, 0.15, 0.1, 0.1, 0.1, 0.015, 0.05, 0.025, 0.04, 0.04, 0.04, 0.04],
    [0.1, 0.15, 0.05, 0.05, 0.1, 0.15, 0.05, 0.15, 0.1, 0.02, 0.025, 0.015, 0.01, 0.01, 0.02],
    [0.05, 0.05, 0.15, 0.015, 0.015, 0.03, 0.1, 0.1, 0.085, 0.15, 0.1, 0.01, 0.025, 0.01, 0.11],
    [0.05, 0.05, 0.05, 0.03, 0.025, 0.05, 0.1, 0.1, 0.15, 0.15, 0.05, 0.075, 0.025, 0.05, 0.045], 
    [0.025, 0.05, 0.1, 0.05, 0.065, 0.1, 0.05, 0.075, 0.2, 0.12, 0.05, 0.075, 0.01, 0.02, 0.01],
    [0.1, 0.05, 0.075, 0.05, 0.075, 0.025, 0.025, 0.1, 0.015, 0.1, 0.1, 0.125, 0.1, 0.05, 0.01],
    [0.01, 0.02, 0.015, 0.1, 0.1, 0.1, 0.075, 0.025, 0.01, 0.025, 0.125, 0.125, 0.15, 0.1, 0.02],
    [0.02, 0.01, 0.01, 0.02, 0.15, 0.125, 0.115, 0.1, 0.015, 0.02, 0.1, 0.1, 0.15, 0.1, 0.01],
    [0.01, 0.01, 0.02, 0.01, 0.15, 0.15, 0.08, 0.08, 0.025, 0.02, 0.05, 0.12, 0.1, 0.1, 0.075],
    [0.01, 0.02, 0.01, 0.02, 0.02, 0.175, 0.025, 0.11, 0.115, 0.25, 0.045, 0.025, 0.05, 0.025, 0.1],
    [0.02, 0.03, 0.03, 0.02, 0.03, 0.025, 0.125, 0.1, 0.12, 0.15, 0.025, 0.025, 0.05, 0.15, 0.1],
    [0.03, 0.03, 0.03, 0.03, 0.01, 0.02, 0.03, 0.075, 0.15, 0.17, 0.15, 0.075, 0.025, 0.075, 0.1],
    [0.01, 0.02, 0.02, 0.01, 0.015, 0.01, 0.075, 0.16, 0.17, 0.085, 0.15, 0.075, 0.05, 0.05, 0.1],
    [0.01, 0.01, 0.01, 0.02, 0.075, 0.075, 0.05, 0.1, 0.1, 0.13, 0.13, 0.13, 0.075, 0.075, 0.01],
]
 
import json
with open('/home/ninodoko/musicgenerator/ninopianino/results.json') as f: 
    new_results = json.loads(f.read())


#markov_values = new_results
