from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json, subprocess

def gen_notes_for_key(track, number_notes, key, scale, duration = 1, bias_same_note = 0, low_end = 'A0', high_end = 'G#8'):
    k = music_models.Key(key, scale)
    prev_note = random.choice(k.notes)
    notes = []
    while number_notes>0:
        notes.append(music_models.Note(track = track, note = prev_note, duration = duration, volume = 100)) 
        while True:
            prev_note = k.generate_note(prev_note, 7, bias_same_note)
            if music_models.get_pitch(prev_note) < music_models.get_pitch(high_end) and music_models.get_pitch(prev_note) > music_models.get_pitch(low_end): break
        number_notes -= 1 
    return notes

def calculate_number_of_notes(block):
    if block.get('number_of_notes'): return block['number_of_notes']
    elif block.get('number_of_bars'): return block['number_of_bars'] * block['number_of_notes_in_bar']
    elif block.get('note_length'): return block['bpm']/60 * block['note_length']
    elif block.get('block_length'): return block['block_length'] / (1.0 / (block['bpm']/60))
    else: raise Exception('There was an error calculating the number of notes in block ', block.get('name'))


def generate_generic_notes(b):
    number_of_notes = calculate_number_of_notes(b)
    gen_notes_kwargs = {'track' : b['track'], 'number_notes' : number_of_notes, 'key' : b.get('key', 'A'), 'scale' : b.get('scale', 'minor'), 'bias_same_note' : b.get('bias_same_note'), 'high_end' : b.get('high_end'), 'low_end' : b.get('low_end')}
    generic_notes = gen_notes_for_key(**gen_notes_kwargs)
    return generic_notes


def group_generic_notes(b, generic_notes, starting_point):
    ungrouped_notes = copy.deepcopy(generic_notes)
    if b.get('accents') : 
        accents = {int(x):b['accents'][x] for x in b['accents']}
    else : accents = {}
    grouped_notes_kwargs = {'notes' : ungrouped_notes, 'no_beats' : b.get('number_of_notes_in_bar'), 'time_signature' : b.get('time_signature'), 'bias_separate_notes' : b.get('bias_separate_notes'), 'accents' : accents, 'start_at' : starting_point, 'pattern' : b.get('pattern', [])}
    grouped_notes = note_timing.group_notes_for_time_signature(**grouped_notes_kwargs)
    return grouped_notes    


def handle_block(b):
#        mid.addTrackName(b['track'], b['play_at'][0], b['name'])
    entire_track = []
    generic_notes = generate_generic_notes(b)
    for starting_point in b['play_at']: 
        grouped_notes = group_generic_notes(b, generic_notes, starting_point)
        entire_track += grouped_notes
    return entire_track

def main():

    parser = argparse.ArgumentParser(description="Basic arguments")
    parser.add_argument('--use_soundfont', help = 'Soundfont to use for creating a wav file. If not specified, will just create a mid file', default = '')
    parser.add_argument('--output', help = 'Path for output midi file. ', default = 'output')
    parser.add_argument('--input', help = 'Path for input JSON file. ', default = 'input.JSON')

    args = parser.parse_args()
    output = args.output
    blocks = json.loads(open(args.input, 'r').read())
    
    no_tracks = max([b['track'] for b in blocks]) + 1
    print 'Generating : ', no_tracks
    mid = MIDIFile(no_tracks)
    
    for b in blocks:
        if b.get('block_type') == 'complex' : 
            complex_track = []
            for block in b['blocks']: 
                mid.addTempo(block['track'], block['play_at'][0], block['bpm'])
                complex_track += handle_block(block)
            entire_track = []
            for starting_point in b['play_at']: 
                temp_track = copy.deepcopy(complex_track)
                for bar in temp_track: 
                    for note in bar.notes:
                        note.time += starting_point
                entire_track += temp_track
        else:   
            mid.addTempo(b['track'], b['play_at'][0], b['bpm'])
            entire_track = handle_block(b)
        for bar in entire_track: 
            for note in bar.notes:
                print (note.pitch, note.length, note.volume, note.time, note.track)
                mid.addNote(*note.get_values())

    binfile = open(output + '.mid', 'wb')
    mid.writeFile(binfile)
    binfile.close()
    if args.use_soundfont: 
        command = ['fluidsynth', '-F', output + '.wav', args.use_soundfont, output + '.mid']
        subprocess.call(command)

main()
