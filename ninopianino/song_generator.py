import uuid
import subprocess
import random
import template_utils   
import generator
import haikunator
import sys
import copy
from sample_markov import markov_values

def get_bounds(val, par_a, par_b, par_c, val_mul_a, val_mul_b):
    lower_bound = int(par_a * par_b/ (par_b - val*val_mul_a))
    higher_bound = int(par_c * par_b / val * val_mul_b)
    return (lower_bound, higher_bound)
    

def organize_blocks(blocks):
    for i in range(len(blocks)):
        if i: 
            blocks[i]['play_at'] = [blocks[i-1]['play_at'][-1] + blocks[i-1]['number_of_bars'] * blocks[i-1]['number_of_beats_per_bar']]
    return blocks

def shuffle_segments(segments, segment_number_range = range(1, 3)):
    shuffled_segments = []
    for segment in segments: 
        for i in segment_number_range: 
            shuffled_segments.append(copy.deepcopy(segment))
    random.shuffle(shuffled_segments)
    organized = organize_blocks(shuffled_segments)
    return organized


def shuffle_play_at(segments, segment_number_range = range(1, 3)):
    segments_with_repeats = [[segment, random.choice(segment_number_range)] for segment in segments]
    current_play_at = 0
    while segments_with_repeats:
        segment = random.choice(segments_with_repeats)

        i = segments_with_repeats.index(segment)
        segments_with_repeats[i][1] -= 1
        if segments_with_repeats[i][1] == 0: del segments_with_repeats[i]
        segment = segment[0]

        i = segments.index(segment)
        segments[i]['play_at'].append(current_play_at)
        current_play_at = current_play_at + segment['number_of_bars'] * segment['number_of_beats_per_bar']
    return segments
    

def create_segment_percussion(segment, kwargs):
    percussion = template_utils.create_percussion(segment, no_hits = random.randint(1, 3), no_cymbals = random.randint(1, 3))
    percussion['blocks'][0]['pattern'] = [1] * (segment['number_of_beats_per_bar']%2) + [4]*int(segment['number_of_beats_per_bar']/4)
    percussion['blocks'][0]['default_accent'] = 100
    percussion['markov_values'] = False

    for block in percussion['blocks'][1:]: 
        pattern = template_utils.generate_pattern(segment, 1, kwargs.get('pattern_note_len_range', 4))
        block['pattern'] = pattern
        block['bias_same_note'] = random.choice(kwargs.get('percussion_bias_same_note', range(30, 90, 5)))
        block['default_accent'] = segment['default_accent'] + random.randint(-5, 5)
    return percussion


def generate_song(**kwargs):
    song_root_note = random.choice(template_utils.base_notes)
    song_chord = random.choice(kwargs.get('song_scale', ['major', 'minor']))
    number_of_segments = random.choice(kwargs.get('number_of_segments_range', random.randint(3, 7)))

    bpm_range = kwargs.get('bpm_range', range(150, 540, 15))
    
    segments = [generate_segment(x, kwargs.get('beats_per_bar_range', range(3, 15)), bpm_range) for x in range(number_of_segments)]

    number_of_instruments = random.choice(kwargs.get('number_of_song_instruments_range', range(1, random.randint(1, 3))))
    song_instruments = [random.choice(kwargs.get('instruments_range', range(0, 90))) for i in range(1, number_of_instruments)]
        
    for i in range(len(segments)):
        song_root_note = random.choice(template_utils.base_notes)

        segment = segments[i]
        prev = {}
        if i: 
            prev = segments[i-1]
            segment['default_accent'] = prev['default_accent'] + random.choice(kwargs.get('accent_offset', range(-5, 5)))
            
            lower_bpm_bound, higher_bpm_bound = kwargs.get('bpm_bounds', get_bounds(prev['bpm'], -5, 540, 25, 0.99, 0.7))
            
            segment['bpm'] = prev['bpm'] + random.randint(lower_bpm_bound, higher_bpm_bound)
            lower_accent_bound, higher_accent_bound = kwargs.get('default_accent_bounds', get_bounds(prev['default_accent'], -3, 100, 4, 0.9, 0.9))
            
            segment['default_accent'] = prev['default_accent'] + random.randint(lower_accent_bound, higher_accent_bound)
        else: 
            segment['default_accent'] = random.choice(kwargs.get('default_accent_range', range(65, 85)))

        number_segment_instruments_range = kwargs.get('no_segment_instruments_range', range(1, 5 - len(song_instruments)))
        number_segment_instruments = random.choice(number_segment_instruments_range)
        
        segment_instruments_range = kwargs.get('segment_instruments_range', range(0, 90))
        segment_instruments = song_instruments + [random.choice(segment_instruments_range) for i in range(number_segment_instruments)]
        
        chords = template_utils.generate_random_chord_progression(song_root_note, song_chord,  random.choice(kwargs.get('chords_per_segment_range', range(3, 8))), scale_choices = ['major', 'minor', 'blues'], markov_values = markov_values, exp_var = kwargs.get('chord_exp_var', 5))
        segment['number_of_bars'] = len(chords) * random.choice(kwargs.get('number_segment_bars_range', range(1, 3)))
        
        for instrument in range(len(segment_instruments)):
            #TODO args for low_end and high_end
            low_end = random.randint(1, 3)
            high_end = low_end + random.randint(1, low_end if low_end<3 else 2)
            
            segment_channel = instrument + 1 #+ segment['track']*len(segment_instruments) + 1 
            if segment_channel == 10: segment_channel = instrument + len(segments)*len(segment_instruments) + 1 
                            
            segment['blocks'] += template_utils.create_chord_progression(segment, chords = chords, extra_kwargs = {'low_end' : song_root_note + str(low_end), 'high_end' : song_root_note + str(high_end), 'channel' : segment_channel , 'program_number' : segment_instruments[instrument], 'default_accent' : segment['default_accent'] + random.choice(kwargs.get('block_default_accent_range', range(-5, 5))), 'bias_same_note' : random.choice(kwargs.get('block_same_note_range', range(10, 100, 15)))})

            for block in segment['blocks']:
                pattern = template_utils.generate_pattern(segment, kwargs.get('segment_instrument_pattern_chance', 0.5), kwargs.get('pattern_note_len_range', 4))
                block['pattern'] = pattern

        do_percussion = random.random()
        if not (do_percussion >= kwargs.get('segment_percussion_chance', 0.85) and len(segment['blocks'])/len(segment_instruments) < kwargs.get('skip_percussion_treshold', 3)): 
            percussion = create_segment_percussion(segment, kwargs)           
            segment['blocks'].append(percussion)
 
    segments = shuffle_play_at(segments, kwargs.get('segment_shuffle_range', range(1, 3)))   
    print 'Generated segments are : '
    for segment in segments: 
        print 'Segment ', segment['track'], ' has ', segment['play_at'], ' has  ', segment['number_of_beats_per_bar'], ' beats per bar and ', segment['number_of_bars'], ' bars and lasts ', segment['number_of_beats_per_bar'] * segment['number_of_bars']

#    segments = shuffle_segments(segments, kwargs.get('segment_shuffle_range', range(1, 3)))
    base_block = template_utils.create_base_block()

    base_block['blocks'] = segments
    new_values = [[random.random() + prob for prob in note_probs] for note_probs in markov_values]
    new_values = [[i / sum(x) for i in x] for x in markov_values]
    base_block['markov_values'] = markov_values
    
    mid = generator.generate(base_block)
    song_name = kwargs.get('generate_dir', 'generated/') + haikunator.Haikunator.haikunate()


    soundfont = kwargs.get('soundfont', 'soundfonts/FluidR3_GM.sf2')
    print 'Using soundfont : ', soundfont
    song_path = generator.write_mid(mid, song_name, use_soundfont = soundfont )
    if kwargs.get('get_mid'): 
        return song_path + '.mid'
    success = subprocess.check_output(['lame', song_path + '.wav'])
    return song_path + '.mp3'

def generate_segment(track_no, beats_per_bar_range, bpm_range):
    segment =  {
        'name' : 'generated_track_no_' + str(track_no),
        'track' : track_no,
        'play_at' : [], 
        'number_of_beats_per_bar' : random.choice(beats_per_bar_range), 
        'bpm' : random.choice(bpm_range),
        'block_type' : 'complex', 
        'blocks' : []
    }
    return segment

def main(argv):
    if len(argv) > 2: 
        soundfont = argv[1]
        if len(argv) == 3: 
            generate_dir = argv[2]
    else: 
        soundfont = '../soundfonts/FluidR3_GM.sf2'
        generate_dir = '../http_generated/'
    generate_song(instruments_range = [1, 2, 4, 20, 21, 23, 24, 27, 34, 37, 39, 45, 47, 56, 68], segment_instruments_range = [1, 5, 8, 10, 11, 17, 24, 26, 28, 32, 33, 35, 36, 38, 39, 41, 45, 46, 52, 53, 54, 58, 68, 70, 72, 75, 76, 77, 78, 85], soundfont = soundfont, generate_dir = generate_dir)
#    generate_song(soundfont = soundfont, generate_dir = '../http_generated/')

#    generate_song(soundfont = soundfont, generate_dir = 'http_generated/')


if __name__ == '__main__' :
    main(sys.argv)
