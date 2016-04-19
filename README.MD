<h1>
    JSON Template Music Generator
</h1>

<h2>
    Synopsys
</h2>

This is a program designed to create music based on previously defined JSON templates. These templates allow you to define blocks of music, and then combine said blocks to create a song. Defining a block of music requires details about the piece of music it should generate (such as number of notes, the key(s) used in the block, time signature and so on), but a lot of these options have defaults, so, in theory, you should be able to just leave a blank block and it should generate some sort of music. 
This is <b>not</b> a software that will write music on its own. I have given many a thought about how to write a semi-intelligent program that can write music, but I always ended up putting in a lot of unwritten rules which end up being personal preferences, so I would try to think of a way to allow the user to configure the program to create music to his/her own liking, and always ended with ideas similar to this one. 
Extensive music knowledge is not required to use this program. I will provide a few test templates which you can use to generate your music, and if this gets popular enough, maybe I will make a platform for sharing said templates. 
Programming knowledge also should not be a problem; even if you don't know what JSON means. I will try to explain how the template structure works as exhaustivelly as I can, but you should still read up on how JSOn works. 

<h2>
    Templates
</h2>
    TODO
    
<h2>
    Usage
</h2>
    TODO
    
<h2>
    Music generator
</h2>

This is a section to describe the workings of the program. It does not describe how to actually use it, so it may not be of your interest to read it. 

The main bit of the program is contained in the models being used. The music generator itself uses all of these methods to piece together music based on templates. If you wish to use these models and write your own generator, feel free to do so. 

<h4>
Note
</h4>

The Note model is just a wrapper around the midiutil package and serves as a convenience class to pass around values which are then sent for output. Mind you, while the midiutil package's addNote method requires a pitch value, the note class takes in a note value and then converts it to pitch in the __init__ method. 
The format of notes that can be passed to this class is <notevalue>[#]<octave>. For instance, G#6 means the G# note on the 6th octave on a keyboard. For convenience's sake, I do not use flat notes because, well, this is not a music theory textbook, and I would not appreciate having almost 80% more notes in certain arrays. I do understand why flat notes exist, but i prefer simplicity over correctness when writing code like this. 

<h4>
Key
</h4>

The Key is there to help out generating random notes with some patterns. When creating a Key instance, you give it the root note and the type of scale, and it will generate a list of notes belonging to this scale. You can then call the generate_note method to, well, generate a note. 
<quote>
    #This function generates a note regarding the note_pivot it is given. 
    #A pivot is required so the notes chosen aren't just completely arbitrary, and so with a given pivot and radius, the generator will pick notes relatively close to each other. 
    #The bias_same_note is an int argument <100 that is a probability for the generator to choose the same note as the pivot. If using the note_timing module, notes with the same value are squished together, which is basically how you get notes of varying length. 
</quote>

To sum it up - you pass it a pivot note and a radius, and the method will generate a note within the specified radius of the pivot note that belongs to the key. For instance, if working in the Am key, passing it pivot_note = E3, note_radius = 3, it will return a random note from [B(E-3), C, D, E, F, G, B(E+3)].

<h4>
Bar
</h4>

The Bar class helps out with timing notes. When given a list of notes, this list is separated into bars where all notes have a combined length as specified by the time signature. The bar can then accent these notes to add to the effect of playing in said signature. 
