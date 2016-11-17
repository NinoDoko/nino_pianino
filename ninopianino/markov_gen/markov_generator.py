import sys, json


def rec_markov(base_markov, values):
    if len(values) > 1: 
        return rec_markov(base_markov[values[0]], values[1:])
    else: 
        base_markov[values[0]] += 1.0


def markov_from_values(base_markov, values, markov_layers):
    for i in range(markov_layers, len(values)):
        prev_notes = values[i-markov_layers:i]
        rec_markov(base_markov, prev_notes)
    return base_markov

def main():
    try: 
        base_markov = sys.argv[1]
        with open(base_markov, 'r') as f: 
            base_markov = json.loads(f.read())

        markov_json = sys.argv[2]
        markov_vals = []
        with open(markov_json, 'r') as f: 
            markov_vals = json.loads(f.read())

        markov_result = sys.argv[3]
        markov_layers = int(sys.argv[4])
        markov_vals = markov_from_values(base_markov, markov_vals, markov_layers)

        with open(markov_result, 'w') as f: 
            f.write(json.dumps(markov_vals))
    except: 
        print 'Something went wrong; probably did not supply a proper argument. Arguments were ', sys.argv, ' expecting 3 arguments - base_markov markov_values markov_result'
        import traceback
        traceback.print_exc()

main()
