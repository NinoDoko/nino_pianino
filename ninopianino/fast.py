import random, json


nino_dir = '/home/ninodoko/musicgenerator'
def main():
    kwargs = {
        #What the general scale for the shond should be - chosen randomly from this list. 
        'song_scale' : ['major', 'minor'],

        #How many segments the song has. 
        'number_of_segments_range' : range(10, 20),

        #A range for beats per bar for each segment. Will choose randomly. 
        'beats_per_bar_range' : range(3, 7),

        #A range for how many chords each segment should have. Chooses randomly from this list. 
        'chords_per_segment_range': range(1, 3), 

        #A list containing the program numbers of instruments that should be used. The program will choose randomly from these. 
        'instruments_range' : [1, 2, 4, 7, 26, 32, 33, 38, 45, 46, 82],

        #The number of instruments that will be active throughout the song. 
        'number_of_song_instruments_range' : range(2, 6),

        #Each segment will have a different accent from the previous, determined by a random value from this list. 
        'accent_offset' : range(-5, 5),

        #A list from accents from which segments will receive their base accent. 
        'default_accent_range' : range(75, 95),

        #Number of extra instruments per segment. 
        'no_segment_instruments_range' : range(0, 3),

        #Instruments range for the segment specific instruments.
        'segment_instruments_range' : [1, 4, 10, 12, 24, 26, 32, 33, 34, 35, 37, 39, 41, 42, 45, 46, 58, 66, 74, 75, 76, 78],

        #Range for the number of bars per segment. Will choose randomly from this list. 
        'number_segment_bars_range' : range(1, 6),

        #Accent range offset for instrument specific blocks. 
        'block_default_accent_range' :  range(-5, 5),

        #A list of values for bias_same_note for specific instruments. 
        'block_same_note_range' :  range(10, 40, 5),

        #Chance for each instrument to follow a pattern for the duration of the segment. 
        'segment_instrument_pattern_chance' : 0.7,

        #Upper range for how long a pattern note can last. Should not be longer than the maximum amount of beats per bar for the instrument. 
        'pattern_note_len_range' :  5,
        
        #And the lower range for how long the note can last. Should not be less than 1. 
        'pattern_note_min_len_range' : 1,

        #List for possible values for the bias_same_note for percussions per segment. 
        'percussion_bias_same_note' : range(30, 90, 5),

        #The dir where the songs are saved. 
        'generate_dir' :  nino_dir + '/nino_gen_8/',

        #The directory for the soundfont. This is an example, and should be supplied for specific use cases. 
        'soundfont' :  nino_dir + '/soundfonts/FluidR3_GM.sf2',

        #The song generator will randomly repeat segments and then shuffle them. This is a range of the numbers of repeats for each segment. 
        'segment_shuffle_range' : range(1, 5),

        #The script uses a specific function to generate a base default accent, but we may want to place an upper limit. 
        'max_base_default_accent' : 80,

        #This variable basically specifies how often the randomly generated chords will contain a chord vastly different from the generic chord. For instance, how commonly a chord progression for a song in C major to contain a chord in F minor. Higher values mean more generic chords. 
        'chord_exp_var': 3,

        #We may want to have segments with few instruments and no drums. This is the percentage that there are drums if the number of instruments is below the defined treshold. 
        'segment_percussion_chance': 0.85,

        #If there's less than this many instruments in a segment, there's a chance (defined above) that there will be no percussion for that segment. 
        'skip_percussion_treshold' : 3,

    }

    kwargs = json.dumps(kwargs)
    with open('/home/ninodoko/musicgenerator/sample_config.json', 'w') as f: 
        f.write(kwargs)

main()
