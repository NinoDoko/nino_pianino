import itertools, random

base_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
notes_list = [x + y for y in  [str(i) for i in range(0, 9)] for x in base_notes]
pitch_offset = 24

keys_diffs = {
    'major' : [0, 2, 4, 5, 7, 9, 11],
    'minor' : [0, 2, 3, 5, 7, 8, 10],
    'acoustic' : [0, 2, 4, 6, 7, 9, 10],
    'algerian' : [0, 2, 3, 6, 7, 8, 11, 12, 14, 15, 17],
    'altered' : [0, 1, 3, 4, 6, 8, 10], 
    'augmented' : [0, 3, 4, 7, 8, 11],
    'bebop' : [0, 2, 4, 5, 7, 9, 10, 11],
    'blues' : [0, 3, 5, 6, 7, 10],
    'chromatic' : [0, 1, 2, 3, 4, 5,6, 7, 8, 9, 10, 11],
    'double_harmonic' : [0, 1, 4, 5, 7, 8, 11],
    'enigmatic' : [0, 1, 5, 6, 8, 9, 11],
    'flamenco' : [0, 1, 4, 5, 7, 8, 11], 
    'gypsy' : [0, 2, 3, 6, 7, 8, 10], 
    'half_iminished' : [0, 2, 3, 5, 6, 8, 10],
    'harmonic_major' : [0, 2, 4, 5, 7, 8, 11],
    'harmonic_minor' : [0, 2, 3, 5, 7, 8, 11],
    'hijaroshi' : [0, 4, 6, 7, 11],
    'hungarian_minor' : [0, 2, 3, 6, 7, 8, 11],
    'insen' : [0, 1, 5, 7, 10],
    'iwato' : [0, 1, 5, 6, 10], 
    'locrian' : [0, 1, 3, 5, 6, 8, 10],
}

def get_pitch(note):
    return notes_list.index(note) + pitch_offset

#Note class; mostly used to add data to a midi file. 
class Note:
    def __init__(self, track = 0, channel = 0, note = 'A0', time = 0, duration = 0, volume = 0):
        self.track = track
        self.note = note
        self.channel = channel - 1 #in code, channels are numbered 0-15, while in files they're 1-16. This matters when using percussion (channel 9 in code, 10 in files). 
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
    
    def __init__(self, root_note = 'A', scale = 'minor', b_notes = [], notes_bias = {}, low_end = 'A2', high_end = 'G#6', markov_values = None):
        self.scale = scale
        self.keys_diffs = keys_diffs
        self.root_note = root_note
        root_note_index = base_notes.index(root_note)
        self.diffs = [(x + root_note_index)%len(base_notes) for x in self.keys_diffs[scale]]
        notes_bias = {str((int(x) + root_note_index)%len(base_notes)) : notes_bias[x] for x in notes_bias}
        
        for note_diff in notes_bias:  
            if int(note_diff) in self.diffs:
                self.diffs += [int(note_diff) for i in range(notes_bias[note_diff])]

        if not b_notes : 
            self.base_notes = [base_notes[x] for x in self.diffs]
        else : 
            self.base_notes = b_notes
      
        self.notes = [[x] * self.base_notes.count(x[:-1]) for x in notes_list if x[:-1] in self.base_notes and notes_list.index(low_end) <= notes_list.index(x) <= notes_list.index(high_end)]
        self.notes = [item for sublist in self.notes for item in sublist]

        #Markov values are used for generating notes using Markov chains.  
        #It's explained a bit better below, at the function. 
        self.markov_values = markov_values
        if markov_values: 
            depth = lambda L: isinstance(L, list) and max(map(depth, L)) +1 
            markov_depth = depth(markov_values)
            self.markov_prev_notes = [self.notes.index(self.generate_note(None, 3)) for i in range(markov_depth-1)]



    #This function generates a note regarding the note_pivot it is given. 
    #A pivot is required so the notes chosen aren't just completely arbitrary, and so with a given pivot and radius, the generator will pick notes relatively close to each other. 
    #The bias_same_note is an int argument <100 that is a probability for the generator to choose the same note as the pivot. If using the note_timing module, notes with the same value are squished together, which is basically how you get notes of varying length. 
    def generate_note(self, note_pivot = None, note_radius = 3, bias_same_note = 0, dir_write_note = ''):
        if random.randint(0, 100) < bias_same_note and note_pivot: 
            return note_pivot
            
        if not note_pivot: 
            return random.choice(self.notes)
        else:
            if self.markov_values:
                note = self.generate_note_markov(note_pivot)
                note_index = None
            else: 
                pivot_index = self.notes.index(note_pivot)
                note_index = random.randint(max(0, pivot_index - note_radius), min(pivot_index + note_radius, len(self.notes)-1))
                note = self.notes[note_index]
           
        if dir_write_note: 
            with open(dir_write_note, 'a+') as f: 
                if not note_index: 
                    note_index = self.notes.index(note)
                f.write(', ' + str(note_index % 16))
        return note


    #This function generates a note but by using markov chain principles instead. Basically, there is (or should be) a file containing values that help choose the note based on the previous one. The values are contained in a list like so : 
    #markov_values = [[0.2, 0.1, 0.2, 0.05, ...], [0.1, 0.2, ...]] 
    #Here, each list represents the values for a note (for instance, the 0th list represents the values for the 0th note in the scale), and each value in that list is the probability that that is the chosen note from the chain. More on this in the readme. 
    #As of a recent update, you can have multiple layers in the chains. 

    def generate_note_markov(self, prev_note):
        if not self.markov_values: 
            print 'No markov values found, but tried to generate using Markov chains. '
            print 'Ensure you are not using the Markov attribute, or include a markov_file and initialize the Key object with it. '
            exit()
        prev_notes = self.markov_prev_notes[1:] + [self.notes.index(prev_note)]
        note_index = self.base_notes.index(prev_note[:-1])
        note_table = self.markov_values

        for note in prev_notes: 
            note_table = note_table[note]

        note_table = [x/sum(note_table) for x in note_table]
        r, s = random.random(), 0
        for i in range(len(note_table)):
            note = note_table[i]
            s+= note
            if s >= r: 
                note_index = i % len(self.notes)
                return self.notes[note_index]
        #If we get here, something wrong happened because at some point, s has to be greater than r. 
        print 'Something went wrong at generating markov note, random int was ', r, ' and sum was ', s
        exit()

#A bar is a class containing several notes. The class is mainly used to accent notes. 
#The accent_notes function receives a dictionary as an argument, but the user can manually set the accents property. 
#The accents is a dictionary that looks like {1 : 100, 3 : 80}, where the key is the note that is accented, and the value is the volume. This accenting dictionary will make the first note with the highest volume, and the 3rd with 80% of the highest volume. 
#All other notes use the default value used in the constructor. 
class Bar:
    def __init__(self, notes, accents = {}, default_accent = 50):
        self.notes = notes
        for note in self.notes : note.volume = default_accent
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
