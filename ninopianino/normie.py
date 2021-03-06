import random, json, os


nino_dir = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])

def main():
    kwargs = {
        #What the general scale for the shond should be - chosen randomly from this list. 
        'song_scale' : ['major', 'minor'],

        #How many segments the song has. 
        'number_of_segments_range' : range(2, 5),
    
        #The range of BPMs for each segment. Chooses randomly for each segment. 
        'bpm_range': range(160, 450, 15), 

        #A range for beats per bar for each segment. Will choose randomly. 
        'beats_per_bar_range' : [3, 9],

        #A range for how many chords each segment should have. Chooses randomly from this list. 
        'chords_per_segment_range': range(1, 4), 

        #A list containing the program numbers of instruments that should be used. The program will choose randomly from these. 
#        'instruments_range' : range(1, 20),
         'instruments_range' : [1, 4, 24, 26, 33, 36, 37, 45, 46], 
#        'instruments_range' : [1, 2, 4, 7, 26, 32, 33, 45, 46, 82],
#        'instruments_range' : [1, 2, 6, 7, 15, 16, 19, 20, 21, 22, 23, 24, 27, 29, 37, 38, 39, 40, 41, 42, 52, 57, 60, 67, 80, 81, 87], #for merlin; 19 is organ, 80 + 81 are techno

        'segment_instruments_range' : [4, 10, 11, 12, 24, 28, 32, 33, 34, 35, 39, 45, 46,  ], # for merlin

#        'segment_instruments_range' : [8, 9, 10, 13, 16, 17, 18, 22, 24, 25, 26, 28, 33, 34, 35, 36, 39, 41,43, 45, 46, 49, 53, 54, 56, 58, 60, 62, 63, 64, 65, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79, 82, 83, 85, ], # for merlin

        #The number of instruments that will be active throughout the song. 
        'number_of_song_instruments_range' : range(3, 6),

        #Number of main instruments per segment
        'number_main_instruments' : 1,

        #The bias_same_note chances for the main instruments. It's a list that is randomly chosen from. 
        'main_instrument_bias_same_note' : [0],

        #How much louder the main instrument should be.
        'main_default_accent_offset' : 20,

        #The maximum pattern note length for the main instrument
        'main_pattern_len_range' : 2, 

        #Each segment will have a different accent from the previous, determined by a random value from this list. 
        'accent_offset' : range(-5, 5),

        #A list from accents from which segments will receive their base accent. 
        'default_accent_range' : range(70, 85),

        #Volume to be added to percussions. 
        'percussion_accent_offset' : 0,

        #Number of extra instruments per segment. 
        'no_segment_instruments_range' : range(1, 4),

        #Instruments range for the segment specific instruments.
#        'segment_instruments_range' : range(1, 20),
#        'segment_instruments_range' : [1, 4, 10, 12, 24, 26, 32, 33, 34, 35, 41, 42, 45, 46, 58, 74, 75, 76, 78],

        #Range for the number of bars per segment. Will choose randomly from this list. 
        'number_segment_bars_range' : range(5, 9),

        #Accent range offset for instrument specific blocks. 
        'block_default_accent_range' :  range(-5, 5),

        #A list of values for bias_same_note for specific instruments. 
        'block_same_note_range' :  range(10, 40, 5),

        #Chance for each instrument to follow a pattern for the duration of the segment. 
        'segment_instrument_pattern_chance' : 0.9,

        #Upper range for how long a pattern note can last. Should not be longer than the maximum amount of beats per bar for the instrument. 
        'pattern_note_len_range' :  2,
        
        #And the lower range for how long the note can last. Should not be less than 1. 
        'pattern_note_min_len_range' : 1,

        #List for possible values for the bias_same_note for percussions per segment. 
        'percussion_bias_same_note' : range(30, 90, 5),

        #The same min and max values, but only for percussions. 
        'pattern_percussion_min_len_range': 2,
        'pattern_percussion_max_len_range': 4,

        #The dir where the songs are saved. 
        'generate_dir' :  nino_dir + '/nino_gen_14/',

        #The file from which we get markov values. 
        'markov_values' : nino_dir + '/trainer/results.json', 

        #The directory for the soundfont. This is an example, and should be supplied for specific use cases. 
        'soundfont' :  nino_dir + '/soundfonts/OmegaGMGS2.sf2',

#'/soundfonts/orchestra_sf/techno combo2.sf2',
# '/soundfonts/orchestra_sf/SGM-V2.01.sf2',
#'/soundfonts/orchestra_sf/merlin_gmv22.sf2',
#'/soundfonts/FluidR3_GM.sf2',

        #The song generator will randomly repeat segments and then shuffle them. This is a range of the numbers of repeats for each segment. 
        'segment_shuffle_range' : range(2, 6),

        #The script uses a specific function to generate a base default accent, but we may want to place an upper limit. 
        'max_base_default_accent' : 80,

        #This variable basically specifies how often the randomly generated chords will contain a chord vastly different from the generic chord. For instance, how commonly a chord progression for a song in C major to contain a chord in F minor. Higher values mean more generic chords. 
        'chord_exp_var': 7,

        #We may want to have segments with few instruments and no drums. This is the percentage that there are drums if the number of instruments is below the defined treshold. 
        'segment_percussion_chance': 0.85,

        #If there's less than this many instruments in a segment, there's a chance (defined above) that there will be no percussion for that segment. 
        'skip_percussion_treshold' : 3,

    }

    kwargs = json.dumps(kwargs)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/sample_config.json', 'w') as f: 
        f.write(kwargs)

main()
