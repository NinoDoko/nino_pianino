<h1>General template markdown specification </h1>
<h3>Introduction</h4>
So the idea is that you are able to describe a song by defining blocks of music. Each block is consisted of several attributes, such as key, type and so on. This idea will be expanded on as the project matures. 
Once all blocks have been defined, the melody is composed by joining the blocks together. Idealy, you can have multiple tracks allowing multiple types of instruments. The initial version will likely use one track for just a piano or something. 

<h3>Usage</h3>
I didn't know where to go with it first, but I really enjoy making JSON files seeing as they're fairly easy to use. I feel like making a JSON template for a song is a good idea. 
I had other ideas such as using arguments to give the number of notes and so on, but it might just be easier to define them in JSON. Or maybe have arguments which work globally, f.e., total number of notes in the song, or time signature (boo to songs that only use one time signature >:c ) or something. 

Ideally, the script should be used in the following way : 

  python generator.py --json_file song_stuff.json

... with some options which I can't think of right now. 


<h3>Blocks</h4>
The entire data structure is going to be in the JSON format, seeing as the project is written in python, and manipulating JSON data is pretty damn easy. 

The JSON file should contain a blocks list, where each block is a dictionary. The structure should look like this. 

{
	"blocks": {
		"boring_progression": {
			"keys": ["Am", "C", "G", "F"],
			"signature": "11/8",
			"bpm": 111,
			"number_notes": 15
		},
		"nancarrow_style": {
			"keys": ["D", "A", "C", "G"],
			"signature": "1/42",
			"bpm": 50,
			"number_notes": 115
		}
	},
	"arrangement": ["boring_progression", "nancarrow_style", "nancarrow_style"]
}

These will, of course, include much more information, but this is just to have some idea of how a song template will look. 

<h3>Execution</h3>
The generator script will read the file, go block by block and fill a sample midi file. The note generation is the major problem here. Currently, the idea is that the generator takes in consideration only the differences between the current note and the generated one. 

If we're using keys to generate melodies, maybe a more proper way to work is to take the array of all possible notes, and create another list which starts at the bottom note fitting the key and append all notes based on music theory (take notes that differ by 1-1-1/2-1-1-1/2-1 and so on) and take notes from that list in a certain range. 

I'll examine other ways to generate notes, but this seems like a simple enough way. It kinda even accounts for weird time signatures (if we're able to properly deal with them) and chords (all we're doing for a chord like, Cm7, is adding additional notes to Cm). 

<h4>Other stuff</h4>
Um, dunno really. Just talking out of my ass here, maybe I'll get it working one day. 
