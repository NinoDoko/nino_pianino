from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json, subprocess

#If this value is supplied, the Key class will write down all notes it generates in the file specified. 
dir_write_note = ''

def set_dir_write_note(new_dir):
    global dir_write_note
    dir_write_note = new_dir

def gen_notes_for_key(track, number_notes, root_note, scale, channel, duration = 1, bias_same_note = 0, low_end = 'A0', high_end = 'G#8', base_notes = [], notes_bias = {}, markov_values = None):
    k = music_models.Key(root_note, scale, base_notes, notes_bias, low_end, high_end, markov_values)
    notes = []
    prev_note = k.generate_note(None, 3)
    while number_notes>0:
        prev_note = k.generate_note(prev_note, 7, bias_same_note, dir_write_note = dir_write_note)
        notes.append(music_models.Note(channel = channel, track = track, note = prev_note, duration = duration, volume = 100)) 
        number_notes -= 1 
    return notes

def calculate_number_of_notes(block):
    if block.get('number_of_notes'): return block['number_of_notes']
    elif block.get('number_of_bars'): return block['number_of_bars'] * block['number_of_beats_per_bar']
    else: raise Exception('There was an error calculating the number of notes in block ', block.get('name'))


def generate_generic_notes(b):
    number_of_notes = calculate_number_of_notes(b)
    gen_notes_kwargs = {'track' : b['track'], 'channel' : b.get('channel', 1), 'number_notes' : number_of_notes, 'root_note' : b.get('root_note', 'A'), 'scale' : b.get('scale', 'minor'), 'bias_same_note' : b.get('bias_same_note'), 'high_end' : b.get('high_end', 'G#7'), 'low_end' : b.get('low_end', 'C1'), 'base_notes': b.get('base_notes'), 'notes_bias': b.get('notes_bias', {}), 'markov_values' : b.get('markov_values')}
    generic_notes = gen_notes_for_key(**gen_notes_kwargs)
    return generic_notes


def group_generic_notes(b, generic_notes, starting_point):
    ungrouped_notes = copy.deepcopy(generic_notes)
    if b.get('accents') : 
        accents = {int(x):b['accents'][x] for x in b['accents']}
    else : accents = {}
    grouped_notes_kwargs = {'notes' : ungrouped_notes, 'no_beats' : b.get('number_of_beats_per_bar'), 'time_signature' : b.get('time_signature'), 'bias_separate_notes' : b.get('bias_separate_notes'), 'accents' : accents, 'start_at' : starting_point, 'pattern' : b.get('pattern', []), 'default_accent':b.get('default_accent', 50)}
    grouped_notes = note_timing.group_notes_for_time_signature(**grouped_notes_kwargs)
    return grouped_notes    


def handle_block(b, mid):
    if b.get('repeat', 1) > 1:
        b['play_at'] += [i * b.get('number_of_beats_per_bar', 1) * b.get('number_of_bars') for i in range(1, b['repeat']+1)]
    if b.get('block_type') == 'complex' :
        mid.addTempo(b['track'], b['play_at'][0], b['bpm']) 
        complex_track = []
        for block in b['blocks']: 
            if not block: continue 
            for key in b:
                if key not in block.keys() + ['blocks', 'block_type', 'play_at', 'repeat', 'number_of_blocks']:
                    block[key] = b[key]
            complex_track += handle_block(block, mid)

        entire_track = []
        
        for starting_point in b['play_at']:
            temp_track = copy.deepcopy(complex_track)
            for bar in temp_track: 
                for note in bar.notes:
                    note.time += starting_point
            entire_track += temp_track
    else:
        entire_track = []
        generic_notes = generate_generic_notes(b)       
            
        for starting_point in b['play_at']:
                mid.addProgramChange(b['track'], b.get('channel', 2) - 1, starting_point, b.get('program_number', 0)) 
                grouped_notes = group_generic_notes(b, generic_notes, starting_point)
                entire_track += grouped_notes
#        print 'notes for ', b['name'], ':', [[t.time for t in x.notes] for x in entire_track], '\n\n'
    return entire_track





def main():

    parser = argparse.ArgumentParser(description="Basic arguments")
    parser.add_argument('--use_soundfont', help = 'Soundfont to use for creating a wav file. If not specified, will just create a mid file', default = '')
    parser.add_argument('--output', help = 'Path for output midi file. ', default = 'output')
    parser.add_argument('--input', help = 'Path for input JSON file. ', default = 'input.JSON')
    parser.add_argument('--no_tracks', help = 'Number of tracks. Default is 100. ', default = 100)

    args = parser.parse_args()
    output = args.output
    blocks = json.loads(open(args.input, 'r').read())
    
    no_tracks = args.no_tracks
    
    mid = generate(blocks, no_tracks)
    write_mid(mid, args.output, args.use_soundfont)
    
    
def generate(blocks, no_tracks = 100):
    mid = MIDIFile(no_tracks)

    entire_track = handle_block(blocks, mid)
    print ('Entire track is : ', entire_track)
    return generate_from_track(mid, entire_track, no_tracks)    

def generate_from_track(mid, entire_track, no_tracks = 100):
    for bar in entire_track: 
        for note in bar.notes:
            mid.addNote(*note.get_values())                

    return mid
   
def write_mid(mid, output):
    binfile = open(output + '.mid', 'w+b')
    
    mid.writeFile(binfile)
    binfile.close()
    return output

def to_wav(song_path, soundfont):
    command = ['fluidsynth', '-F', song_path + '.wav', soundfont, song_path + '.mid']
    subprocess.call(command)


if __name__ == '__main__' : 
    main()
