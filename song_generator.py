import uuid
import subprocess
import random
import template_utils   
import generator
import haikunator
import sys

def get_bounds(val, par_a, par_b, par_c, val_mul_a, val_mul_b):
    lower_bound = int(par_a * par_b/ (par_b - val*val_mul_a))
    higher_bound = int(par_c * par_b / val * val_mul_b)
    print 'Bounds : ', lower_bound, val, higher_bound
    return (lower_bound, higher_bound)
    
def generate_song(**kwargs):
    song_root_note = random.choice(template_utils.base_notes)
    number_of_segments = kwargs.get('number_of_segments', random.randint(3, 7))
    
    segments = [generate_segment(x, range(3, 15), range(150, 540, 15)) for x in range(number_of_segments)]
    
    song_instruments = [random.choice(kwargs.get('instruments_range', range(0, 90))) for i in range(random.randint(1, 3))]
        
    for i in range(len(segments)):
        segment = segments[i]
        prev = {}
        if i: 
            prev = segments[i-1]
            if not prev.get('number_of_bars'): 
                print 'Messup!'
                print prev, ' is prev'
#                print segments
                print len(segments), ' number of segments'
                exit(-1)
            segment['play_at'] = [prev['play_at'][0] + prev['number_of_bars'] * prev['number_of_beats_per_bar']]
            segment['default_accent'] = prev['default_accent'] + random.choice(kwargs.get('accent_offset', range(-5, 5)))
            
            lower_bpm_bound, higher_bpm_bound = kwargs.get('bpm_bounds', get_bounds(prev['bpm'], -5, 540, 25, 0.99, 0.7))
            
            segment['bpm'] = prev['bpm'] + random.randint(lower_bpm_bound, higher_bpm_bound)
            lower_accent_bound, higher_accent_bound = kwargs.get('default_accent_bounds', get_bounds(prev['default_accent'], -3, 100, 4, 0.9, 0.9))
            
            segment['default_accent'] = prev['default_accent'] + random.randint(lower_accent_bound, higher_accent_bound)
        else: 
            segment['default_accent'] = random.choice(kwargs.get('default_accent_range', range(45, 55)))

        number_segment_instruments_range = kwargs.get('no_segment_instruments', range(1, 5 - len(song_instruments)))
        number_segment_instruments = random.choice(number_segment_instruments_range)
        
        segment_instruments_range = kwargs.get('segment_instruments_range', range(0, 90))
        segment_instruments = song_instruments + [random.choice(segment_instruments_range) for i in range(number_segment_instruments)]
        
        chords = template_utils.generate_chord_progression(song_root_note)
        segment['number_of_bars'] = len(chords) * random.choice(kwargs.get('number_segment_bars_range', range(7, 14)))

        
        for instrument in range(len(segment_instruments)):
            #TODO args for low_end and high_end
            low_end = random.randint(1, 3)
            high_end = low_end + random.randint(1, low_end if low_end<3 else 2)
            
            segment_channel = instrument + segment['track']*len(segment_instruments) + 1 
            if segment_channel == 10: segment_channel = instrument + len(segments)*len(segment_instruments) + 1 
            
            segment['blocks'] += template_utils.create_chord_progression(segment, chords = chords, extra_kwargs = {'low_end' : song_root_note + str(low_end), 'high_end' : song_root_note + str(high_end), 'channel' : segment_channel , 'program_number' : segment_instruments[instrument], 'default_accent' : segment['default_accent'] + random.choice(kwargs.get('block_default_accent_range', range(-5, 5))), 'bias_notes' : {'0' : 3, '4' : 3, '7' : 3}, 'bias_same_note' : random.choice(kwargs.get('block_same_note_range', range(10, 80, 15)))})
            
        percussion = template_utils.create_percussion(segment, no_hits = random.randint(2, 3), no_cymbals = random.randint(1, 3))
        percussion['blocks'][0]['pattern'] = [1] * (segment['number_of_beats_per_bar']%2) + [4]*int(segment['number_of_beats_per_bar']/4)
        percussion['blocks'][0]['default_accent'] = 60
        
        print 'Segment ', i, ' from ', segment['play_at'], ' to ', segment['play_at'][0] + segment['number_of_bars'] * segment['number_of_beats_per_bar'], ' has program numbers ', [x.get('program_number') for x in segment['blocks']]
#        return
        for block in percussion['blocks'][1:]: 
            block['bias_same_note'] = random.choice(kwargs.get('percussion_bias_same_note', range(20, 90, 5)))
            block['default_accent'] = segment['default_accent'] + random.randint(-5, 5)
            
        segment['blocks'].append(percussion)
    
    
    base_block = template_utils.create_base_block()
    base_block['blocks'] = segments
    
    mid = generator.generate(base_block)
    song_name = kwargs.get('generate_dir', 'generated/') + haikunator.Haikunator.haikunate()
    song_path = generator.write_mid(mid, song_name, use_soundfont = kwargs.get('soundfont', 'soundfonts/FluidR3_GM.sf2'))
#    song_path = generator.write_mid(mid, song_name, use_soundfont = 'soundfonts/ProTrax_Classical_Guitar.sf2')
    success = subprocess.check_output(['lame', song_path + '.wav'])
    return song_path + '.mp3'

def generate_segment(track_no, beats_per_bar_range, bpm_range):
    segment =  {
        'track' : track_no,
        'play_at' : [0], 
        'number_of_beats_per_bar' : random.choice(beats_per_bar_range), 
        'bpm' : random.choice(bpm_range),
        'block_type' : 'complex', 
        'blocks' : []
    }
    return segment

if __name__ == '__main__' :
    if len(sys.argv) == 2: 
        soundfont = sys.argv[1]
    else: 
        soundfont = 'soundfonts/FluidR3_GM.sf2'
    generate_song(instruments_range = [1, 2, 4, 20, 21, 23, 24, 27, 34, 37, 39, 40, 45, 47, 56, 68], segment_instruments_range = [1, 5, 8, 10, 11, 17, 24, 26, 28, 32, 33, 35, 36, 38, 39, 41, 45, 46, 52, 53, 54, 58, 68, 70, 72, 75, 76, 77, 78, 85], soundfont = soundfont, generate_dir = 'http_generated/')
#    generate_song(soundfont = soundfont, generate_dir = 'http_generated/')

