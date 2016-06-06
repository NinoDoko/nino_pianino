from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json, subprocess

def gen_notes_for_key(track, number_notes, root_note, scale, channel, duration = 1, bias_same_note = 0, low_end = 'A0', high_end = 'G#8', base_notes = []):
    print 'Low end is : ', low_end, music_models.get_pitch(low_end), 'High end is : ', high_end, music_models.get_pitch(high_end)
    k = music_models.Key(root_note, scale, base_notes)
    prev_note = random.choice(k.notes)
    notes = []
    while number_notes>0:
        notes.append(music_models.Note(channel = channel, track = track, note = prev_note, duration = duration, volume = 100)) 
        while True:
            prev_note = k.generate_note(prev_note, 7, bias_same_note)
            if music_models.get_pitch(low_end) < music_models.get_pitch(prev_note) < music_models.get_pitch(high_end) : 
                print 'Got note : ', prev_note, 'with pitch: ', music_models.get_pitch(prev_note)
                break
        number_notes -= 1 
    return notes

def calculate_number_of_notes(block):
    if block.get('number_of_notes'): return block['number_of_notes']
    elif block.get('number_of_bars'): return block['number_of_bars'] * block['number_of_beats_per_bar']
    elif block.get('note_length'): return block['bpm']/60 * block['note_length']
    elif block.get('block_length'): return block['block_length'] / (1.0 / (block['bpm']/60))
    else: raise Exception('There was an error calculating the number of notes in block ', block.get('name'))


def generate_generic_notes(b):
    number_of_notes = calculate_number_of_notes(b)
    gen_notes_kwargs = {'track' : b['track'], 'channel' : b['channel'], 'number_notes' : number_of_notes, 'root_note' : b.get('root_note', 'A'), 'scale' : b.get('scale', 'minor'), 'bias_same_note' : b.get('bias_same_note'), 'high_end' : b.get('high_end'), 'low_end' : b.get('low_end'), 'base_notes': b.get('base_notes')}
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
    if b.get('block_type') == 'complex' : 
        complex_track = []
        for block in b['blocks']: 

            block['channel'] = block.get('channel', b['channel'])
            block['track'] = block.get('track', b['track'])
            block['bpm'] = block.get('bpm', b['bpm'])
            block['repeat'] = b.get('repeat', b.get('repeat', 1))
            
            complex_track += handle_block(block, mid)
            
        entire_track = []
        for starting_point in b['play_at']:
            temp_track = copy.deepcopy(complex_track)
            for bar in temp_track: 
                for note in bar.notes:
                    note.time += starting_point
            entire_track += temp_track
    else:
        repeat = b.get('repeat', 1)
        entire_track = []
        generic_notes = []
        while repeat > 0:
            generic_notes += generate_generic_notes(b)
            repeat -= 1
        for starting_point in b['play_at']:
                mid.addProgramChange(b['track'], b['channel'] - 1, starting_point, b.get('program_number', 0)) 
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
    mid = MIDIFile(no_tracks)

    for b in blocks:
        mid.addTempo(b['track'], b['play_at'][0], b['bpm'])
#        print 'Added program change : ', b['track'], b['channel'], b['play_at'][0], b.get('program_number', 0)
        entire_track = handle_block(b, mid)
#        mid.addProgramChange(b['track'], b['channel'] - 1, 0, b.get('program_number', 0))
        #channel-1 because channels are numbered 0-15 in code, 1-16 in files. 
        for bar in entire_track: 
            for note in bar.notes:
#                print (note.pitch, note.length, note.volume, note.time, note.track, note.channel)
                mid.addNote(*note.get_values())

    binfile = open(output + '.mid', 'wb')
    mid.writeFile(binfile)
    binfile.close()
    if args.use_soundfont: 
        command = ['fluidsynth', '-F', output + '.wav', args.use_soundfont, output + '.mid']
        subprocess.call(command)

main()
