from midiutil.MidiFile import MIDIFile
import music_models, argparse, random

def gen_notes_for_key(number_notes, key = 'A', scale = 'minor', time = 0, duration = 1):
    k = music_models.Key(key, scale)
    prev_note = random.choice(k.notes)
    notes = []
    while number_notes>0:
        notes.append(music_models.Note(note = prev_note, time = time, duration = duration, volume = 100)) 
        prev_note = k.generate_note(prev_note, 7)
        number_notes -= 1 
    return notes


def gen_note(prev_note = None, t=0, d=1, diffs = []):
    if prev_note:
        if not diffs : 
            diffs = [i for i in [-12, -11, -9, -7, -5, -4, -2, 0, 2, 4, 5, 7, 9, 11, 12] if prev_note.pitch-21-i > 0 and i+prev_note.pitch-21 <len(music_models.notes_list)-1]
        r_note = music_models.notes_list[prev_note.pitch - 21 + random.choice(diffs)]
    else:
        r_note=random.choice(music_models.notes_list)
    print r_note
    return music_models.Note(note = r_note, time = t, duration = d, volume = 100)

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
#    prev_note = gen_note()
    t = 0
    gen_notes_for_key(50)
#    while n_notes:
#        mid.addNote(*prev_note.get_values())
#        prev_note = gen_note(prev_note=prev_note, t=t, d=1)
#        n_notes -= 1
#        t += 1

    binfile = open(output, 'wb')
    mid.writeFile(binfile)
    binfile.close()

main()
