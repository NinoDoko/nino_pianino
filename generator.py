from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json, subprocess

def gen_notes_for_key(track, number_notes, root_note, scale, channel, duration = 1, bias_same_note = 0, low_end = 'A0', high_end = 'G#8', base_notes = [], notes_bias = {}):
    k = music_models.Key(root_note, scale, base_notes, notes_bias, low_end, high_end)
    notes = []
    prev_note = k.generate_note(None, 3)
    while number_notes>0:
        prev_note = k.generate_note(prev_note, 3, bias_same_note)
        notes.append(music_models.Note(channel = channel, track = track, note = prev_note, duration = duration, volume = 100)) 
        number_notes -= 1 
    return notes

def calculate_number_of_notes(block):
    if block.get('number_of_notes'): return block['number_of_notes']
    elif block.get('number_of_bars'): return block['number_of_bars'] * block['number_of_beats_per_bar']
    else: raise Exception('There was an error calculating the number of notes in block ', block.get('name'))


def generate_generic_notes(b):
    number_of_notes = calculate_number_of_notes(b)
    gen_notes_kwargs = {'track' : b['track'], 'channel' : b.get('channel', 1), 'number_notes' : number_of_notes, 'root_note' : b.get('root_note', 'A'), 'scale' : b.get('scale', 'minor'), 'bias_same_note' : b.get('bias_same_note'), 'high_end' : b.get('high_end'), 'low_end' : b.get('low_end'), 'base_notes': b.get('base_notes'), 'notes_bias': b.get('notes_bias', {})}
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
#        mid.addTrackName(b['track'], b['play_at'][0], b['name'])
    if b.get('repeat', 1) > 1:
        b['play_at'] += [i * b.get('number_of_beats_per_bar', 1) * b.get('number_of_bars') for i in range(1, b['repeat']+1)]
    if b.get('block_type') == 'complex' :
        mid.addTempo(b['track'], b['play_at'][0], b['bpm']) 
        complex_track = []
        
        for block in b['blocks']: 
            for key in b:
                if type(block) != dict: 
                    print block, type(block)
                    print b['blocks']
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
        print b.get('name')
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

    args = parser.parse_args()
    output = args.output
    blocks = json.loads(open(args.input, 'r').read())
    
    no_tracks = 100
    mid = MIDIFile(no_tracks)

    
#    for b in blocks:
#        print 'Added program change : ', b['track'], b['channel'], b['play_at'][0], b.get('program_number', 0)
    entire_track = handle_block(blocks, mid)
#        mid.addProgramChange(b['track'], b['channel'] - 1, 0, b.get('program_number', 0))
    #channel-1 because channels are numbered 0-15 in code, 1-16 in files. 
    for bar in entire_track: 
        for note in bar.notes:
#            print note.get_values(), note.note
            mid.addNote(*note.get_values())                

    binfile = open(output + '.mid', 'wb')
    mid.writeFile(binfile)
    binfile.close()
    if args.use_soundfont: 
        command = ['fluidsynth', '-F', output + '.wav', args.use_soundfont, output + '.mid']
        subprocess.call(command)

main()
