import random, json


number_of_song_instruments = random.randint(1, 3)
nino_dir = '/home/ninodoko/musicgenerator'
def main():
    kwargs = {

        #How many segments the song has. 
        'number_of_segments_range' : range(3, 7),

        #A list containing the program numbers of instruments that should be used. The program will choose randomly from these. 
        'instruments_range' : [1, 2, 4, 20, 21, 23, 24, 27, 34, 37, 39, 45, 47, 56, 68],

        #The number of instruments that will be active throughout the song. 
        'number_of_song_instruments' : number_of_song_instruments,

        #Each segment will have a different accent from the previous, determined by a random value from this list. 
        'accent_offset' : range(-5, 5),

        #A list from accents from which segments will receive their base accent. 
        'default_accent_range' : range(65, 85),

        #Number of extra instruments per segment. 
        'no_segment_instruments_range' : range(1, random.randint(1, 5 - number_of_song_instruments)),

        #Instruments range for the segment specific instruments.
        'segment_instruments_range' : [1, 5, 8, 10, 11, 17, 24, 26, 28, 32, 33, 35, 36, 38, 39, 41, 45, 46, 52, 53, 54, 58, 68, 70, 72, 75, 76, 77, 78, 85],

        #Range for the number of bars per segment. Will choose randomly from this list. 
        'number_segment_bars_range' : [1, 2, 3],

        #Accent range offset for instrument specific blocks. 
        'block_default_accent_range' :  range(-5, 5),

        #A list of values for bias_same_note for specific instruments. 
        'block_same_note_range' :  range(10, 100, 15),

        #Chance for each instrument to follow a pattern for the duration of the segment. 
        'segment_instrument_pattern_chance' : 0.5,

        #Upper range for how long a pattern note can last. Should not be longer than the maximum amount of beats per bar for the instrument. 
        'pattern_note_len_range' :  4,

        #List for possible values for the bias_same_note for percussions per segment. 
        'percussion_bias_same_note' : range(30, 90, 5),

        #The dir where the songs are saved. 
        'generate_dir' :  nino_dir + '/nino_generated/',

        #The directory for the soundfont. This is an example, and should be supplied for specific use cases. 
        'soundfont' :  nino_dir + '/soundfonts/FluidR3_GM.sf2',

    }

    kwargs = json.dumps(kwargs)
    with open('/home/ninodoko/musicgenerator/sample_config.json', 'w') as f: 
        f.write(kwargs)

main()
