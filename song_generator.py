import uuid
import subprocess
import random
import template_utils   
import generator

def generate_song():
    song_root_note = random.choice(template_utils.base_notes)
    number_of_segments = random.randint(1, 5)
    
    segments = [generate_segment(x) for x in range(number_of_segments)]
    
    song_instruments = [random.randint(0, 90) for i in range(random.randint(1, 3))]
        
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
            segment['default_accent'] = prev['default_accent'] + random.randint(-10, 10)
            
        else: 
            segment['default_accent'] = random.randint(40, 60)
            
        segment_instruments = song_instruments + [random.randint(0, 90) for i in range(random.randint(0, 2))]
        
        chords = template_utils.generate_chord_progression(song_root_note)
        print 'These are chords : ', chords
        print 'Adding bars. '
        segment['number_of_bars'] = len(chords) * random.randint(4, 8)
        print segment['number_of_bars']
        
        for instrument in range(len(segment_instruments)):
            low_end = random.randint(1, 3)
            high_end = low_end + random.randint(1, low_end if low_end<3 else 2)
            
            segment_channel = instrument + segment['track']*len(segment_instruments) + 1 
            if segment_channel == 10: segment_channel = instrument + len(segments)*len(segment_instruments) + 1 
            
            segment['blocks'] += template_utils.create_chord_progression(segment, chords = chords, extra_kwargs = {'low_end' : song_root_note + str(low_end), 'high_end' : song_root_note + str(high_end), 'channel' : segment_channel , 'program_number' : segment_instruments[instrument], 'default_accent' : segment['default_accent'] + random.randint(-5, 5), 'bias_notes' : {'0' : 3, '4' : 3, '7' : 3}, 'bias_same_note' : random.randrange(10, 60, 5)})
            
        percussion = template_utils.create_percussion(segment, no_hits = random.randint(2, 3), no_cymbals = random.randint(1, 3))
        percussion['blocks'][0]['pattern'] = [1] * (segment['number_of_bars']%2) + [2]*int(segment['number_of_bars']/2)
        percussion['blocks'][0]['default_accent'] = 20
                
#        return
        for block in percussion['blocks'][1:]: 
            block['bias_same_note'] = random.randrange(30, 80, 10)
            block['default_accent'] = segment['default_accent'] + random.randint(-5, 5)
            
        segment['blocks'].append(percussion)
        
        print percussion['play_at'], percussion['number_of_bars'], percussion['number_of_beats_per_bar']
        print segment['play_at'], segment['number_of_bars'], segment['number_of_beats_per_bar']
    
    
    base_block = template_utils.create_base_block()
    base_block['blocks'] = segments
    
    mid = generator.generate(base_block)
    song_id = str(uuid.uuid4())
    song_name = '/tmp/' + 'generated_song_' + song_id
    song_path = generator.write_mid(mid, song_name, use_soundfont = 'soundfonts/FluidR3_GM.sf2')
    success = subprocess.check_output(['lame', song_path + '.wav'])
    return song_path + '.mp3'

def generate_segment(track_no):
    segment =  {
        'track' : track_no,
        'play_at' : [0], 
        'number_of_beats_per_bar' : random.randint(3, 15), 
        'bpm' : random.randrange(150, 270, 15),
        'block_type' : 'complex', 
        'blocks' : []
    }
    return segment

if __name__ == '__main__' :     
    generate_song()

