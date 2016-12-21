import random
import song_generator


#attributes_table is a table with keys that look like this: 
#   'key': 
#   {
#       'related_key' : 
#       [
#           {
#                'func' : get_key_values, 
#                'args' : ['some', 'args']
#                'prob' : 0.5,
#                'value' : 50,
#           },{
#                'prob' : 0.5,
#                'func' : get_key_values, 
#                'args' : ['some', 'args']
#                'value' : [
#                   {
#                       'prob' : 0.5, 
#                       'value' : 25
#                   }, {
#                       'prob' : 0.5, 
#                       'value' : 15
#                   }
#                ]
#           }
#       ]
#   }, {
#       'related_key_2':
#        ...
#
#How it then works is, we have the key that we want to make a decision for (called as decision key from now on). Then, we go key-by-key, find the decision key, randomly choose a value using the probability value ('prob') and then return the value for that key. 
#Values can be just a straight up value, but they can also be a list of dictionaries, each with their own probabilities and values, which can be further nested. 
#Alternatively, you may pass a function to the 'func' key, and args to the 'args' key. This function will then be called with the arguments to programatically generate the values. 


class DecisionMaker():
    def __init__(self, attributes, attributes_table):
        self.attributes_table = attributes_table
        for attribute in attributes: 
            setattr(self, attribute, attributes[attribute])

    def make_decision(self, attribute, related_keys = None): 
        attribute_table = [self.attributes_table[key] for key in self.attributes_table if key == attribute][0]
        attribute_value = self.get_table_result(attribute_table)
        

    def get_table_result(self, attribute_table):
        r, s = random.random(), 0
        for d in table:
            if type(d['value']) == list:
                d_value = self.get_table_result(d)
            else: 
                d_value = d['value']
            s += d['prob']
            if s >= r: 
                return d_value
