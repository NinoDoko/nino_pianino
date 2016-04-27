from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json, subprocess

def gen_notes_for_key(track, number_notes, key = 'A', scale = 'minor', duration = 1, bias_same_note = 0, low_end = 'A0', high_end = 'G#8'):
    k = music_models.Key(key, scale)
    prev_note = random.choice(k.notes)
    notes = []
    while number_notes>0:
        notes.append(music_models.Note(note = prev_note, duration = duration, volume = 100)) 
        while True:
            prev_note = k.generate_note(prev_note, 7, bias_same_note)
            if music_models.get_pitch(prev_note) < music_models.get_pitch(high_end) and music_models.get_pitch(prev_note) > music_models.get_pitch(low_end): break
        number_notes -= 1 
    return notes

def calculate_number_of_notes(block):
    if block.get('number_of_notes'): return block['number_of_notes']
    elif block.get('number_of_bars'): return block['number_of_bars'] * int(block['time_signature'].split('/')[0])
    elif block.get('note_length'): return block['bpm']/60 * block['note_length']
    elif block.get('block_length'): return block['block_length'] / (1.0 / (block['bpm']/60))
    else: raise Exception('There was an error calculating the number of notes in block ', block.get('name'))

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
        mid.addTrackName(b['track'], b['play_at'][0], 'track_name')
        mid.addTempo(b['track'], b['play_at'][0], b['bpm'])
        number_of_notes = calculate_number_of_notes(b)
        generic_notes = gen_notes_for_key(b['track'], number_of_notes, key = b['key'], scale = b['scale'], bias_same_note = b['bias_same_note'], high_end = b['high_end'], low_end = b['low_end'])
        entire_track = []
        for starting_point in b['play_at']: 
            ungrouped_notes = copy.deepcopy(generic_notes)
            if b.get('accents') : 
                accents = {int(x):b['accents'][x] for x in b['accents']}
            else : accents = {}
            grouped_notes = note_timing.group_notes_for_time_signature(ungrouped_notes, b['time_signature'], b['bpm'], b['bias_separate_notes'], accents, start_at = starting_point)
            entire_track += grouped_notes
#        print [[(note.pitch, note.length, note.volume, note.time) for note in bar.notes] for bar in entire_track] ,'\n\n\n'
        
        for bar in entire_track: 
            for note in bar.notes:
                print (note.pitch, note.length, note.volume, note.time)
                mid.addNote(*note.get_values())

    binfile = open(output + '.mid', 'wb')
    mid.writeFile(binfile)
    binfile.close()
    if args.use_soundfont: 
        command = ['fluidsynth', '-F', output + '.wav', args.use_soundfont, output + '.mid']
        subprocess.call(command)

main()
