import itertools, random

base_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_list = [x + y for y in  [str(i) for i in range(8)] for x in base_notes]
pitch_offset = 21

def get_pitch(note):
    return notes_list.index(note) + pitch_offset

#Note class; mostly used to add data to a midi file. 
class Note:
    def __init__(self, track = 0, channel = 0, note = 'A0', time = 0, duration = 0, volume = 0):
        self.track = track
        self.channel = channel
        self.pitch = get_pitch(note)
        self.time = time
        self.duration = duration
        self.volume = volume

    def get_values(self):
        return self.track, self.channel, self.pitch, self.time, self.duration, self.volume
        

#The key class offers functionality relating to generating random notes based off of some rules. 
#The key argument is what the root note of the key is, for instance, the note A. This argument can be ommited if using the base_notes argument. 
#The scale is the name of the scale that the other notes will be generated off. For instance, if using a minor scale with the A as the root of the key, if will generate all the notes belonging to the A minor scale. This argument can be ommited if using the base_notes argument. 
#If you wish to define your own notes that define the key (maybe I missed one or you just want to use a group of notes), you can supply a list of base notes that the key will use (example : ['A', 'C', 'D', 'D#', G#']). This list should not contain flat notes (yes, I know there's a reason for flat and sharp notes existing, but for the sake of code simplicity, I just use sharp notes). 

class Key:
    keys_diffs = {
        'major' : [0, 2, 4, 5, 7, 9, 11],
        'minor' : [0, 2, 3, 5, 7, 8, 10],
    }
    
    def __init__(self, key = 'A', scale = 'minor', b_notes = []):
        self.key = key
        self.diffs = [(x + base_notes.index(key))%len(base_notes) for x in self.keys_diffs[scale]]
        if not b_notes : 
            self.base_notes = [base_notes[x] for x in self.diffs]
        else : 
            self.base_notes = base_notes
        self.notes = [x for x in notes_list if x[:-1] in self.base_notes]

    #This function generates a note regarding the note_pivot it is given. 
    #A pivot is required so the notes chosen aren't just completely arbitrary, and so with a given pivot and radius, the generator will pick notes relatively close to each other. 
    #The bias_same_note is an int argument <100 that is a probability for the generator to choose the same note as the pivot. If using the note_timing module, notes with the same value are squished together, which is basically how you get notes of varying length. 
    def generate_note(self, note_pivot, note_radius = 3, bias_same_note = 0):
        if random.randint(0, 100) < bias_same_note : 
            return note_pivot
        pivot_index = self.notes.index(note_pivot)
        note_index = random.randint(max(0, pivot_index - note_radius), min(pivot_index + note_radius, len(self.notes)-1))
        return self.notes[note_index]

#A bar is a class containing several notes. The class is mainly used to accent notes. 
#The accent_notes function receives a dictionary as an argument, but the user can manually set the accents property. 
#The accents is a dictionary that looks like {1 : 100, 3 : 80}, where the key is the note that is accented, and the value is the volume. This accenting dictionary will make the first note with the highest volume, and the 3rd with 80% of the highest volume. 
#All other notes use the default value used in the constructor. 
class Bar:
    def __init__(self, notes, accents = {}, default_volume = 50):
        self.notes = notes
        for note in self.notes : note.volume = default_volume
        self.accents = accents
        if accents : self.accent_notes(accents)
        
    def accent_notes(self, accents = {}):
        if not self.accents : self.accents = accents
        for accent in accents:
            try:
                self.notes[accent].volume = accents[accent]
            except Exception:
                pass
        
def main():
    a = Key('B', 'minor')
    print a.notes
    
if __name__ == '__main__' : main()
