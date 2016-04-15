from midiutil.MidiFile import MIDIFile
import music_models, argparse, random, note_timing

def gen_notes_for_key(number_notes, key = 'A', scale = 'minor', time = 0, duration = 1, bias_same_note = 0):
    k = music_models.Key(key, scale)
    prev_note = random.choice(k.notes)
    notes = []
    while number_notes>0:
        notes.append(music_models.Note(note = prev_note, time = time, duration = duration, volume = 100)) 
        prev_note = k.generate_note(prev_note, 7, bias_same_note)
        number_notes -= 1 
    return notes

def main():

    parser = argparse.ArgumentParser(description="Basic arguments")
    parser.add_argument('--some_argument', help = 'Stub argument', default = '')
    parser.add_argument('--number_notes', help = 'Number of notes to play ', default = 50, type = int)
    parser.add_argument('--notes_duration_range_min', help = 'Top range for variation of note duration. ', type = int, default = 0.5)
    parser.add_argument('--notes_duration_range_max', help = 'Lower range for variation of note duration. ', type = int, default = 2)
    parser.add_argument('--output', help = 'Path for output midi file. ', default = 'output.mid')

    args = parser.parse_args()
    n_notes = args.number_notes
    duration_max = args.notes_duration_range_max
    duration_min = args.notes_duration_range_min
    output = args.output

    mid = MIDIFile(1)
    mid.addTrackName(0, 0, 'Sample')
    notes = gen_notes_for_key(50, bias_same_note = 40)
    entire_track = note_timing.group_notes_for_time_signature(notes, '7/8', 120, bias_separate_notes = 50, accents = {0 : 100, 2 : 80})
    print [[(note.pitch, note.length, note.volume, note.time) for note in bar.notes] for bar in entire_track]
    
    for bar in entire_track: 
        for note in bar.notes:
            mid.addNote(*note.get_values())

    binfile = open(output, 'wb')
    mid.writeFile(binfile)
    binfile.close()

main()
