<h1>
    JSON Template Music Generator
</h1>

<h2>
    Synopsys
</h2>

This is a program designed to create music based on previously defined JSON templates. These templates allow you to define blocks of music, and then combine said blocks to create a song. Defining a block of music requires details about the piece of music it should generate (such as number of notes, the key(s) used in the block, time signature and so on), but a lot of these options have defaults, so, in theory, you should be able to just leave a blank block and it should generate some sort of music. 

<h2>
    Templates
</h2>
Example templates will be provided with the repo. 

#TODO: Add templates and list what they do. 

The way templates work is by defining a JSON file which contains a single list of blocks. Each block is a dictionary which looks like this : 

<h3>Blocks</h3>
```
{
	"name": "intro_block1",
	"track": 0,
	"play_at": [0, 44, 88, 588, 824],
	"bpm": 200,
	"number_of_bars": 4,
	"number_of_notes_in_bar": 11,
	"bias_same_note": 55,
	"bias_separate_notes": 5,
	"pattern": [1, 2, 1, 2, 1, 3, 1],
	"root_note": "C#",
	"scale": "minor",
	"low_end": "C#3",
	"high_end": "C#5",
	"default_accent": 100,
	"accents": {
		"0": 100, 
		"3": 80,
		"6": 80
	}
}
```
<ul>
    <li>
    name: This is the name of the block. It simply states the name of the track. (note: in the current version, this doesn't work. midiutil doesn't want to properly convert the text to ascii, and I need to figure this out). Default : ''.
    </li>
    <li>
    track: The number of the track this block goes to. Default : 0.
    </li>
    <li>
    play_at: A list of integers where each number is the beat when the block is played. The above block will be played at the 0th beat, 44th beat, 88th beat and so on. This is the only way to synchronize blocks to play at certain times. <b>Required</b
    </li>
    <li>
    bpm: The tempo at which the block is played. Take care when adding tempos to tracks: it you put two blocks on the same track and add different tempos for them, it might not sound as intended. Default: 120.
    </li>
    <li>
    number_of_bars: The number of bars per block. Default: 1
    </li>
    <li>
    number_of_beats_per_bar: The number of beats per bar. This, alongside number_of_bars determines how many notes there are in a block. In the above block, with 4 bars of 11 beats, the block will last for 44 beats, so setting the play_at value at [0, 44, 88] will mean the block will play continualy for 132 beats. Default : 4
    </li>
    <li>
    bias_same_note: This is a value which is used to determine whether two consecutive notes will be the same. The generator will merge two consecutive notes into one note with combined length (unless bias_separate_notes is used). Basically, this is the probability that after generating a note, the next one will be the same. Default: 0.
    </li>
    <li>
    bias_separate_notes: This is a value which dictates whether two same consecutive notes are merged together or not. You can use this to create longer notes for faster tempos. Default: 0.
    </li>
    <li>
    pattern: A list of how notes should be arranged. The number of values is the number of notes in the bar, and the value is how many beats it lasts. In the above example, each bar will have 7 notes and the notes will have length of 1, 2, 1, 2, 1, 3, 1 respectively. Adding up the lengths correctly brings up to 11 beats per bar. Incorrect patterns are not documented. Default: [].
    </li>
    <li>
    root_note: The root note that, along with the scale value, will determine the notes generated for the block. Default: A
    </li>
    <li>
    scale: Combined with the root note, this represents a list of notes that the generator will choose from. There's a lot of different types of scales that you can look up online. The ones implemented are :
    #TODO spoiler quote with all scales
    Defaul: minor
    </li>
    <li>
    base_notes: If there is not a scale that you want to use, you can use a list of base notes. For instance, if you want to use a gypsy scale minus the last two notes, you can write a base_notes value like so: [0, 2, 3, 6, 7]. Default: []
    </li>
    <li>
    low_end: The lowest note that can be generated for the block. Default: A0
    </li>
    <li>
    high_end: The highest note that can be generated for the block. Use it with low_end to define a range from which notes can be chosen. The block above will choose values between C#3 and C#5. Default G#8.
    </li>
    <li>
    default_accent: Accents are basically the volume levels for notes. Non-accented notes will use the default accent. Default: 50.
    </li>
    <li>
    accents: A dictionary where the keys are the number of the note to be accented and the values are the volumes of these notes. Default: {}.
    </li>
</ul>

<h3>Complex blocks</h3>

Sometimes, you may want to have certain blocks played together all the time, for instance a chorus segment. This segment may have a block for the main line, that plays higher notes, and a couple of blocks that play lower notes. You may also maybe like to make a polyrythm, for instance 3 bars of 7 beats each and a pause of 1 beat at the end played over a background block of 2 blocks of 11 beats each. You can do this with ordinary blocks, but writing the play_at list will be a pain in the A minor. So you can just use complex blocks instead. 

(this is blocks/complextest.json)

```
[
{
    "block_type":"complex",
    "play_at":[0, 44, 88],
    "bpm": 500,
    "track" : 0,
    "blocks":
    [
    {
	    "name": "main_block1",
	    "play_at": [0, 22],
	    "number_of_bars": 3,
	    "root_note": "B",
	    "scale": "major",
	    "number_of_beats_per_bar": 7,
	    "low_end": "B3",
	    "high_end": "C5",
	    "bias_separate_notes": 100,
	    "default_accent": 40,
	    "accents": {
		    "0": 70,
		    "3": 70, 
		    "5": 50
	    }
    },{
	    "name": "main_block2",
	    "play_at": [0, 22],
	    "number_of_bars": 2,
	    "root_note": "B",
	    "scale": "major",
	    "number_of_beats_per_bar": 11,
	    "low_end": "B1",
	    "high_end": "C3",
	    "pattern":[3, 2, 2, 1, 2, 2],
	    "accents": {
		    "0": 100,
		    "3": 100, 
		    "6": 80, 
		    "8": 80, 
		    "13": 100
	    }
    }
]
}
]
```

The complex block must have a block_type value set to 'complex'. This block also must have a play_at value which works as an ordinary block - this one is played on the 0th, 44th and 88th beats. It also has a bpm and track values which act as in a normal block. 

Then, it must have a blocks value, which is a list of other blocks. These blocks may leave out the bpm and track values, which will make it so they use the parent block's bpm and track. The idea here is that the children blocks have their play_at values act differently - they describe when the block is played <b>inside</b> the complex block. In the above example, if you consider the block as a separate block of music, they will play on the 0th and 22th beat in that block. Than, the complex block makes that block repeat on the 0th, 44th and 88th beat. 

Furthermore, you can have complex blocks containing other complex blocks. Check out nestedcomplextest.json in the blocks/ directory. 

<h2>
    Usage
</h2>
You call the generator.py script with certain arguments to get your music, and that script, in turn, calls the other modules which contain the actual meat. If you cloned/downloaded the repo, you can do: 
```
    $python generator.py --input blocks/longsongtest.json --output myfirstsong
```

This will use an example template and create a midi file - myfirstsong.mid . Adding synthesizers to convert the midi to a wav/mp3/whatever is up to the user. The easiest way is to get fluidsynth. 
```
    #apt-get install fluidsynth
```

Then, you need a soundfont. <a href = "http://www.synthfont.com/soundfonts.html">This </a>is where I got the ones I use for testing, specifically the FluidR3 GM bank. Mind you, this is an sfArk file, and you need to find a way to decompress it. Alternatively, you can just google around for a standard issue sf2. 

With fluidsynth, you can then go: 

```
    $fluidsynth -F myfirstsong.wav /path/to/file.sf2 myfirstsong.mid
```

Or, to save on a few keystrokes, there is an argument you can use for this: 

```
    $python generator.py --input blocks/longsongtest.json --output myfirstsong --use_soundfont /path/to/file.sf2
```

Alternatively, if you cleanly organized your template into tracks, you can import it into actual music editing software, like rosegarden or lmms. 

List of arguments: 
<ul>
    <li>
    --output: An argument which defines the name under which the .mid (and .wav) file be saved. Default = 'output'
    --input: An argument with the path to the .json file containing the template. Default = 'input.json'
    --use_soundfont: Path to the sf2 file to use for creating a wav. Only works if you have fluidsynth. default = ''
    </li>
</ul>
    
<h2>
    Project overview
</h2>

This is a section to describe the workings of the program. It does not describe how to actually use it, so it may not be of your interest to read it. 

<h3>
    music_models.py
</h3>

This module contains the models for generating a list of notes. 

<h4>
Note
</h4>

The Note model is just a wrapper around the midiutil package and serves as a convenience class to pass around values which are then sent for output. Mind you, while the midiutil package's addNote method requires a pitch value, the note class takes in a note value and then converts it to pitch in the __init__ method. 
The format of notes that can be passed to this class is <notevalue>[#]<octave>. For instance, G#6 means the G# note on the 6th octave on a keyboard. For convenience's sake, I do not use flat notes because, well, this is not a music theory textbook, and it's way more simple this way. 

<h4>
Key
</h4>

The Key is there to help out generating random notes with some patterns. When creating a Key instance, you give it the root note and the type of scale, and it will generate a list of notes belonging to this scale. You can then call the generate_note method to, well, generate a note. 
When initiated, a root note and a scale are required to construct a list of basic notes. For instance, a root note of C and a scale with argument 'major' will generate the basic notes : [C, D, E, F, G, A, B]. With these basic notes, the key can then generate all possible notes for these arguments. 
You can also pass a base_notes argument which will allow you to use a custom scale. 

<h4>
Bar
</h4>

The Bar class helps out with timing notes. It is used in the note_timing.py module, and with the accents and default_accent arguments, it will place the notes' volumes at the specified values. 

<h3>
    notes_timing.py
</h3>

This module contains (for the time being) a single method that organizes notes into bars (using the musuc_models.Bar model). The group_notes_for_time_signature takes a list notes and organizes them using the rest of the arguments. 

The function takes an already generated list of notes and assigns to them the volumes, length and the time at which they appear in the songs. 

<h3>
    generator.py
</h3>

This is what brings it all together. It reads in a JSON file, parses the arguments, passes them to the music models for note generating, receives a fresh batch of notes, then sends them to the note_timing module for the notes to be organized into a list of bars, along with values for when to be played and how long to be played for, and then passes the notes to midiutil and ta-da! 

This module doesn't actually do any of the work - it just takes input, calls other modules, organizes the returned values and handles the output. In other words, you call this script to generate the songs. Usage is described in the Usage section. 
