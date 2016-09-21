import random
import template_utils   
import generator

def generate_song():
    song_root_note = random.choice(template_utils.base_notes)
    number_of_segments = random.randint(1, 5)
    
    segments = [generate_segment(x) for x in range(number_of_segments)]
    
    
    for i in range(len(segments)):
        number_of_instruments = random.randint(1, 4) 
        
        segment = segments[i]
        chords = template_utils.generate_chord_progression(song_root_note)
        segment['number_of_bars'] = len(chords) * random.randint(1, 4)
        
        for instrument in range(number_of_instruments):
            low_end = random.randint(1, 3)
            high_end = low_end + random.randint(1, 3)
            segment['blocks'] += template_utils.create_chord_progression(segment, chords = chords, extra_kwargs = {'low_end' : song_root_note + str(low_end), 'high_end' : song_root_note + str(high_end), 'channel' : instrument + segment['track']*number_of_instruments + 1, 'program_number' : random.randint(1, 50), 'default_accent' : random.randint(35, 65), 'bias_notes' : {'0' : 3, '4' : 3, '7' : 3}})
            
        percussion = template_utils.create_percussion(segment, no_hits = random.randint(2, 3), no_cymbals = random.randint(1, 3))
        percussion['blocks'][0]['pattern'] = [1] * (segment['number_of_bars']%2) + [2]*int(segment['number_of_bars']/2)
        percussion['blocks'][0]['default_accent'] = 20
        for block in percussion['blocks'][1:]: 
            block['bias_same_note'] = 60
            block['default_accent'] = 40
#        percussion['blocks'][-1]['bias_same_note'] = 60
        segment['blocks'].append(percussion)
        
        if i: 
            prev = segments[i-1]
            segment['play_at'] = [prev['play_at'][0] + prev['number_of_bars'] * prev['number_of_beats_per_bar']]
            
    
    base_block = template_utils.create_base_block()
    base_block['blocks'] = segments
    
    mid = generator.generate(base_block)
    generator.write_mid(mid, 'generated_test', use_soundfont = 'soundfonts/FluidR3_GM.sf2')

def generate_segment(track_no):
    segment =  {
        'track' : track_no,
        'play_at' : [0], 
        'number_of_beats_per_bar' : random.randint(3, 15), 
        'bpm' : random.choice([60, 120, 150, 180]),
        'block_type' : 'complex', 
        'blocks' : []
    }
    return segment
    
generate_song()
