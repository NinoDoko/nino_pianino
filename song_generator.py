import uuid
import subprocess
import random
import template_utils   
import generator
import haikunator
import sys

def accent_bound(prev):
    #arbitrary functions that generate bounds
    #lower bpms generate higher values for higher_bpm_bound and lower values for lower_bpm_bound, meaning there's a higher chance to increase bpm
    #the reverse goes for high bpms. 
    lower_bpm_bound = int(-5 * 540 / (540 - prev*0.99))
    higher_bpm_bound = int(50 * 540 / prev*0.7)
    return (lower_bpm_bound, higher_bpm_bound)
    
    
def generate_song(**kwargs):
    song_root_note = random.choice(template_utils.base_notes)
    number_of_segments = kwargs.get('number_of_segments', random.randint(1, 5))
    
    segments = [generate_segment(x) for x in range(number_of_segments)]
    
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
            
            lower_bpm_bound, higher_bpm_bound = kwargs.get('bound_function', accent_bound)(prev['bpm'])
            
            print 'Bounds are : ', lower_bpm_bound, higher_bpm_bound, prev['bpm']
            segment['bpm'] = prev['bpm'] + random.randint(lower_bpm_bound, higher_bpm_bound)
            
        else: 
            segment['default_accent'] = random.choice(kwargs.get('default_accent_range', range(45, 55)))

        number_segment_instruments_range = kwargs.get('no_segment_instruments', range(0, 2))
        number_segment_instruments = random.choice(number_segment_instruments_range)
        
        segment_instrument_range = kwargs.get('segment_instrument_range', range(0, 90))
        segment_instruments = song_instruments + [random.choice(segment_instrument_range) for i in range(number_segment_instruments)]
        
        chords = template_utils.generate_chord_progression(song_root_note)
        print 'These are chords : ', chords
        print 'Adding bars. '
        segment['number_of_bars'] = len(chords) * random.choice(kwargs.get('number_segment_bars_range', range(4, 8)))
        print segment['number_of_bars']
        
        for instrument in range(len(segment_instruments)):
            #TODO args for low_end and high_end
            low_end = random.randint(1, 3)
            high_end = low_end + random.randint(1, low_end if low_end<3 else 2)
            
            segment_channel = instrument + segment['track']*len(segment_instruments) + 1 
            if segment_channel == 10: segment_channel = instrument + len(segments)*len(segment_instruments) + 1 
            
            segment['blocks'] += template_utils.create_chord_progression(segment, chords = chords, extra_kwargs = {'low_end' : song_root_note + str(low_end), 'high_end' : song_root_note + str(high_end), 'channel' : segment_channel , 'program_number' : segment_instruments[instrument], 'default_accent' : segment['default_accent'] + random.choice(kwargs.get('block_default_accent_range', range(-5, 5))), 'bias_notes' : {'0' : 3, '4' : 3, '7' : 3}, 'bias_same_note' : random.choice(kwargs.get('block_same_note_range', range(10, 80, 15)))})
            
        percussion = template_utils.create_percussion(segment, no_hits = random.randint(2, 3), no_cymbals = random.randint(1, 3))
        percussion['blocks'][0]['pattern'] = [1] * (segment['number_of_bars']%2) + [2]*int(segment['number_of_bars']/2)
        percussion['blocks'][0]['default_accent'] = 20
                
#        return
        for block in percussion['blocks'][1:]: 
            block['bias_same_note'] = random.choice(kwargs.get('percussion_bias_same_note', range(30, 80, 10)))
            block['default_accent'] = segment['default_accent'] + random.randint(-5, 5)
            
        segment['blocks'].append(percussion)
        
        print percussion['play_at'], percussion['number_of_bars'], percussion['number_of_beats_per_bar']
        print segment['play_at'], segment['number_of_bars'], segment['number_of_beats_per_bar']
    
    
    base_block = template_utils.create_base_block()
    base_block['blocks'] = segments
    
    mid = generator.generate(base_block)
    song_name = kwargs.get('generate_dir', 'generated/') + haikunator.Haikunator.haikunate()
    song_path = generator.write_mid(mid, song_name, use_soundfont = kwargs.get('soundfont', 'soundfonts/FluidR3_GM.sf2'))
#    song_path = generator.write_mid(mid, song_name, use_soundfont = 'soundfonts/ProTrax_Classical_Guitar.sf2')
    success = subprocess.check_output(['lame', song_path + '.wav'])
    return song_path + '.mp3'

def generate_segment(track_no):
    segment =  {
        'track' : track_no,
        'play_at' : [0], 
        'number_of_beats_per_bar' : random.randint(3, 15), 
        'bpm' : random.randrange(150, 540, 15),
        'block_type' : 'complex', 
        'blocks' : []
    }
    return segment

if __name__ == '__main__' :
    if len(sys.argv) == 2: 
        soundfont = sys.argv[1]
    else: 
        soundfont = 'soundfonts/FluidR3_GM.sf2'
    generate_song(song_instruments = range(7) + range(25, 28) + range(57, 72), soundfont = soundfont, generate_dir = 'http_generated/')

