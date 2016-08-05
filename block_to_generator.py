import json

class Block:
    def __init__(self, name = 'unnamed',
                 track = 1, 
                 channel = 1, 
                 program_number = 1, 
                 play_at = [0], 
                 bpm = 60, 
                 number_of_bars = 1, 
                 number_of_beats_per_bar = 4, 
                 bias_same_note = 0, 
                 bias_separate_notes = 0, 
                 pattern = [], 
                 repeat = 1, 
                 root_note = 'C', 
                 scale = 'major', 
                 base_notes = [], 
                 low_end = 'C1', 
                 high_end = 'C6', 
                 default_accent = 50, 
                 accents = {}, 
                 notes_bias = {}, 
                 block_type = None, 
                 blocks = []):
        
        self.name, self.track, self.channel, self.program_number, self.play_at, self.bpm, self.number_of_bars, self.number_of_beats_per_bar, self.bias_same_note, self.bias_separate_notes, self.pattern, self.repeat, self.root_note, self.scale, self.base_notes, self.low_end, self.high_end, self.default_accent, self.accents, self.notes_bias, self.block_type, self.blocks = (
            name, track, channel, program_number, play_at, bpm, number_of_bars, number_of_beats_per_bar, bias_same_note, bias_separate_notes, pattern, repeat, root_note, scale, base_notes, low_end, high_end, default_accent, accents, notes_bias, block_type, blocks
        )
        
        
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
            

