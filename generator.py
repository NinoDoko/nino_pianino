from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing, copy, json

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

def main():

    parser = argparse.ArgumentParser(description="Basic arguments")
    parser.add_argument('--some_argument', help = 'Stub argument', default = '')
    parser.add_argument('--number_notes', help = 'Number of notes to play ', default = 50, type = int)
    parser.add_argument('--notes_duration_range_min', help = 'Top range for variation of note duration. ', type = int, default = 0.5)
    parser.add_argument('--notes_duration_range_max', help = 'Lower range for variation of note duration. ', type = int, default = 2)
    parser.add_argument('--output', help = 'Path for output midi file. ', default = 'output.mid')
    parser.add_argument('--input', help = 'Path for input JSON file. ', default = 'input.JSON')

    args = parser.parse_args()
    print args.input
    n_notes = args.number_notes
    duration_max = args.notes_duration_range_max
    duration_min = args.notes_duration_range_min
    output = args.output
    mid = MIDIFile(1)
    blocks = json.loads(open(args.input, 'r').read())
    
    for b in blocks:
        mid.addTrackName(b['track'], b['play_at'][0], 'track_name')
        number_of_notes = b['number_of_bars'] * int(b['time_signature'].split('/')[0])
        generic_notes = gen_notes_for_key(b['track'], number_of_notes, key = b['key'], scale = b['scale'], bias_same_note = b['bias_same_note'], high_end = b['high_end'], low_end = b['low_end'])
        entire_track = []
        for starting_point in b['play_at']: 
            ungrouped_notes = copy.deepcopy(generic_notes)
            accents = {int(x):b['accents'][x] for x in b['accents']}
            print accents
            grouped_notes = note_timing.group_notes_for_time_signature(ungrouped_notes, b['time_signature'], b['bpm'], b['bias_separate_notes'], accents, start_at = starting_point)
            entire_track += grouped_notes
#        print [[(note.pitch, note.length, note.volume, note.time) for note in bar.notes] for bar in entire_track] ,'\n\n\n'
        
        for bar in entire_track: 
            for note in bar.notes:
                print (note.pitch, note.length, note.volume, note.time)
                mid.addNote(*note.get_values())

    binfile = open(output, 'wb')
    mid.writeFile(binfile)
    binfile.close()

main()
