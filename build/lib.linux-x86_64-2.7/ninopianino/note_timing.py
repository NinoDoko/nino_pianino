import music_models, random



#Time_signature should be a string formatted as x/y, for instance 3/8. 
#The function makes a list of bars (where a bar is a list of notes) and in those bars are tuples of notes + length of note in beats. 
def group_notes_for_time_signature(notes, no_beats, bias_separate_notes = 0, accents = {}, start_at = 0, pattern = [], time_signature = '', default_accent = 50):
    notes = [notes[i:i+no_beats] for i in range(0, len(notes), no_beats)]
    
    result = [[]]
    t = start_at
    for bar in notes:
        new_bar = []
        i = 0
        if pattern: 
            for i in range(len(bar)-1): 
                try:
                    bar[i].duration = pattern[i]
                    bar[i].time = t
                    t += pattern[i]
                    new_bar.append(bar[i])
                except Exception: 
                    continue
        else: 
            while i < no_beats :
                if len(bar) < no_beats : break
                length = 0.0
                j = i
                while bar[i].pitch == bar[j].pitch :
                    length += 1
                    j += 1
                    if random.randint(0, 100) < bias_separate_notes or j == no_beats : 
                        break
                bar[i].duration = length
                if length > 20:
                    print 'Length exceeded!'
                    print length
                    exit()
                bar[i].time = t
                t += length
                new_bar.append(bar[i])
                i = j
        result.append(music_models.Bar(new_bar, accents, default_accent))
    return [x for x in result if x]
