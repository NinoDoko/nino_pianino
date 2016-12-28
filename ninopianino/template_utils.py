import random
from music_models import base_notes, keys_diffs, Key
from generator import gen_notes_for_key

chord_progressions = [
    [(0, 'major'), (5, 'major'), (7, 'major')], # I-IV-V (C-F-G)
    [(0, 'major'), (5, 'major'), (2, 'major')], # I-V-II (C-G-D)
    [(0, 'major'), (9, 'minor'), (7, 'major'), (2, 'minor'), (2, 'major')], #I-vi-VII-ii-II (C-Am-G-Dm-D)
    [(0, 'major'), (9, 'minor'), (2, 'minor'), (7, 'major')], #I-vi-ii-V (C-Am-Dm-G)
    [(0, 'major'), (7, 'major'), (2, 'minor'), (9, 'minor'), (5, 'major'), (5, 'minor')], #I-V-ii-vi-IV-iv (C-G-Dm-Am-F-Fm)
]

def generate_pattern(block, min_note_len = 1, max_note_len = 4):
    pattern_sum = block['number_of_beats_per_bar']
    pattern = []
    while sum(pattern) < pattern_sum:
        pattern.append(min(random.randint(min_note_len, max_note_len), pattern_sum - sum(pattern)))
    return pattern

def index_progression_to_notes(root_note, progression):
    return [(base_notes[(root_note + chord[0])%len(base_notes)], chord[1]) for chord in progression]
    

#You can pass root_note as either the index or the value of the note. 
def generate_chord_progression(root_note):
    progression = random.choice(chord_progressions)
    if root_note in base_notes: 
        root_note = base_notes.index(root_note)
    #Here we assume root_note is the index of the root note. 
#    progression = [(base_notes[(root_note + chord[0])%len(base_notes)], chord[1]) for chord in progression]
    progression = index_progression_to_notes(root_note, progression)
    return progression



def generate_random_chord_progression(root_note, scale, number_of_chords, scale_choices = ['major', 'minor'], markov_values = None, exp_var = 4.0):
    root_key = Key(root_note = root_note, scale = scale)
    root_key_base = root_key.base_notes

    chord_notes = [x.note[:-1] for x in gen_notes_for_key(1, number_of_chords, root_note, scale, 1, markov_values)]
    progression = []

    all_keys = [Key(note, scale) for note in root_key.base_notes for scale in scale_choices]

    keys_candidates_ctrs = [(key, 0.0 + len([x for x in key.base_notes if x in root_key.base_notes]) ** exp_var) for key in all_keys]

    key_candidates_probabilities = [(x[0], x[1]/sum([x[1] for x in keys_candidates_ctrs])) for x in keys_candidates_ctrs]
    if sum(x[1] for x in key_candidates_probabilities) > 1 :
        print 'The sum is : ', sum(x[1] for x in key_candidates_probabilities)

    while len(progression) < number_of_chords: 
        r, s = random.random(), 0
        for key_prob in key_candidates_probabilities:
            s += key_prob[1]
            if s >= r: 
                progression.append((key_prob[0].root_note, key_prob[0].scale))
                break
    return progression
           
        
           

def create_base_block(bpm = 120, play_at = [0], name = 'base', track = 1):
    return {'bpm' : bpm, 'play_at' : play_at, 'name' : name, 'block_type' : 'complex', 'track' : track, 'blocks' : []}


def create_percussion(block, no_hits = 1, no_cymbals = 1):
    percussion_base = {"block_type":"complex", "name":"percussions",  "track":10, "channel":10, "play_at":[0], "number_of_beats_per_bar" : block["number_of_beats_per_bar"], "number_of_bars" : block["number_of_bars"], "blocks": []} 
    for i in range(no_hits):
        percussion_base['blocks'].append({
            "name": "percussions_" + str(i),
            "play_at": [0],
            "root_note": "C",
            "scale": "major",
            "low_end": "B0",
            "high_end": "G1",
            "default_accent": 80, 
        })
        no_hits -= 1

    for i in range(no_cymbals):
        percussion_base['blocks'].append({
            "name": "percussions_cymbals_" + str(i),
            "play_at": [0],
            "base_notes" : ['F#', 'F#', 'F#', 'F#', 'F#', 'G#', 'G#', 'G#', 'G#', 'A#', 'A#', 'C#', 'D#'],
            "low_end": "F#1",
            "high_end": "D#2",
            "defualt_accent": 60, 
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

#from sample_markov import markov_values
#generate_random_chord_progression('C', 'major', 5, markov_values = markov_values)

