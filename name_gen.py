import sys, random

def generate_name(word_ctr, word_list, max_word_len):
    random_name = []
    temp_ctr = word_ctr
    while temp_ctr > 0:
        word = random.choice(word_list)
        while len(word) > max_word_len: 
            word = random.choice(word_list)
        random_name += [word]
        temp_ctr -= 1
    return random_name

def main():
    if len(sys.argv) < 2:
        print 'Usage : python rngnamegenerator.py (number_of_names_to_display) (number_of_words) (max_word_len) '
        print 'Example : python rngnamegenerator.py 5 2'
        sys.exit(-1)
    name_ctr = int(sys.argv[1])
    word_ctr = int(sys.argv[2])
    max_word_len = int(sys.argv[3])
    word_list = open('/usr/share/dict/american-english', 'r').read().split('\n')
    while name_ctr > 0:
        random_name = generate_name(word_ctr, word_list, max_word_len)
        print '-'.join(random_name)

        name_ctr -= 1
main()
