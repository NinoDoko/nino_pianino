import json

class Block:
    defaults = {
        'name' : 'unnamed',
        'track' : 1, 
        'channel' : 1, 
        'program_number' : 1, 
        'play_at' : [0], 
        'bpm' : 60, 
        'number_of_bars' : 1, 
        'number_of_beats_per_bar' : 4, 
        'bias_same_note' : 0, 
        'bias_separate_notes' : 0, 
        'pattern' : [], 
        'repeat' : 1, 
        'root_note' : 'C', 
        'scale' : 'major', 
        'base_notes' : [], 
        'low_end' : 'C1', 
        'high_end' : 'C6', 
        'default_accent' : 50, 
        'accents' : {}, 
        'notes_bias' : {}, 
        'block_type' : None, 
        'blocks' : []
    }
    
    
    hard_defaults = {
        'play_at' : [0], 
        'block_type' : None, 
    }
    def __init__(self, **kwargs):
        
        if kwargs.get('use_defaults', True): 
            for default in self.defaults: 
                if default not in kwargs: 
                    kwargs[default] = self.defaults[default]
                    
        for key in self.hard_defaults: 
            if key not in kwargs: 
                kwargs[key] = self.hard_defaults[key]
            
        for key in kwargs: 
            setattr(self, key, kwargs[key])

        print dir(self)

    def generate_dict_tree(self):
        if self.block_type: 
            temp_block = self
            blocks_temp = []
            for block in self.blocks:
                blocks_temp.append(block.generate_dict_tree())
            temp_block.blocks = blocks_temp
            return temp_block.__dict__
        else:
            d = self.__dict__
            return {x: d[x] for x in self.__dict__ if d[x]}


    def generate_json(self):
        dict_tree = self.generate_dict_tree()
        return json.dumps(dict_tree)
            
    def dump_json_to_file(self, file_path):
        with open(file_path, 'w') as f:
            t = self.generate_json()
            f.write(t)
            

def generate_percussion(block, hit_patterns = [], cymbal_patterns = []):
    percussions = Block(name = 'percussions', channel = 10, block_type = 'complex', number_of_bars = block.number_of_bars, number_of_beats_per_bar = block.number_of_beats_per_bar)
    
    for i in range(len(hit_patterns)):
        percussion_hits = Block(name = 'percussion_hits_' + str(i), pattern = hit_patterns[i], low_end = 'B0', high_end = 'G1', use_defaults = False)
        percussions.blocks = percussions.blocks + [percussion_hits]
        
    for i in range(len(cymbal_patterns)): 
        cymbal_hits = Block(name = 'cymbal_hits_' + str(i), pattern = cymbal_patterns[i], low_end = 'B0', high_end = 'G1', use_defaults = False)
        percussions.blocks= percussions.blocks + [cymbal_hits]
    return percussions
