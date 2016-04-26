import music_models, random



#Time_signature should be a string formatted as x/y, for instance 3/8. 
#The function makes a list of bars (where a bar is a list of notes) and in those bars are tuples of notes + length of note in beats. 
def group_notes_for_time_signature(notes, time_signature, bpm, bias_separate_notes = 0, accents = {}, start_at = 0):
    no_beats, beat_len = [int(x) for x in time_signature.split('/')]
    notes = [notes[i:i+no_beats] for i in range(0, len(notes), no_beats)]
    
    result = [[]]
    t = start_at
    for bar in notes:
        #This is musically unsound (pun intended). 
        #Basically, if a time signature has more notes than the length of a note (for instance 11/4), it halves the length of the note and halves the bpm, essentially arriving at 11/16 with 1/4 of the original bpm. 
        #If you were to write this down on a piece of paper, it would look ugly, but for listening, it works well enough. 
        while len(bar) < no_beats: 
            no_beats /= 2
            bpm /= 2
        #Note length is 1 / frequency, which is 1 / bpm, which is 1/bps
        note_len = 1.0 / (bpm/60.0)
        new_bar = []
        i = 0
        while i < no_beats :
            if len(bar) < no_beats : break
            length = 0.0
            j = i
            while bar[i].pitch == bar[j].pitch :
                length += 1
                j += 1
                if random.randint(0, 100) < bias_separate_notes or j == no_beats : 
                    break
            bar[i].length = length
            bar[i].time = t
            t += bar[i].length
            new_bar.append(bar[i])
            i = j
        result.append(music_models.Bar(new_bar, accents))
    return [x for x in result if x]
