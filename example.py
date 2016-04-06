from midiutil.MidiFile import MIDIFile
import music_models

def main():
  mid = MIDIFile(1)
  mid.addTrackName(0, 0, 'Sample')

  aNote = music_models.Note(0, 0, 'C4', 0, 1, 100)
  mid.addNote(*aNote.get_values())
  

  binfile = open('output.mid', 'wb')
  mid.writeFile(binfile)
  binfile.close()


main()
