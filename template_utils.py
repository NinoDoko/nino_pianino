def create_base_block(bpm = 120, play_at = [0], name = 'base', track = 1, ):
    return {'bpm' : bpm, 'play_at' : play_at, 'name' : name, 'block_type' : 'complex', 'track' : track, 'blocks' : []}


def create_percussion(block, no_hits = 1, no_cymbals = 1):
    percussion_base = {"block_type":"complex", "name":"percussions",  "track":10, "channel":10, "default_accent":80, "play_at":[0], "number_of_beats_per_bar" : block["number_of_beats_per_bar"], "number_of_bars" : block["number_of_bars"], "blocks": []} 
    for i in range(no_hits):
        percussion_base['blocks'].append({
            "name": "percussions_" + str(i),
            "play_at": [0],
            "root_note": "C",
            "scale": "major",
            "low_end": "B0",
            "high_end": "G1",
        })
        no_hits -= 1
    for i in range(no_cymbals):
        percussion_base['blocks'].append({
            "name": "percussions_cymbals_" + str(i),
            "play_at": [0],
            "base_notes" : ['F#', 'G#', 'A#', 'C#', 'D#'],
            "low_end": "F#1",
            "high_end": "D#2",
        })
        no_hits -= 1
    return percussion_base


#chords is a list of (root_note, scale) pairs. For instance : [('A', 'minor'), ('C', 'major'), ('E', 'minor')]
def create_chord_progression(block, chords = [], extra_kwargs = {}):
    no_beats = block['number_of_beats_per_bar']
    no_bars = block['number_of_bars'] / len(chords)
    blocks = []
    for i in range(len(chords)): 
        new_block = {
            'name' : 'gen_chord_' + chords[i][0], 
            'play_at' : [i * no_beats * no_bars],
            'root_note' : chords[i][0], 
            'scale' : chords[i][1], 
            'number_of_bars' : no_bars,
            'number_of_beats_per_bar' : block['number_of_beats_per_bar']
        }
        for kwarg in extra_kwargs: 
            new_block[kwarg] = extra_kwargs[kwarg]
        blocks.append(new_block)
    return blocks

def repeat_block(block, number_repeats, number_of_bars):
    play_at = block['play_at']
    result = []
    for entry in play_at:
        result += [entry] + [entry + i * block.get('number_of_beats_per_bar', 1) * number_of_bars for i in range(1, number_repeats)]
    return result
