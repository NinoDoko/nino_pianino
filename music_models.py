import itertools

notes_list = [x + y for y in  [str(i) for i in range(8)] for x in ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']]

class Note:
  def __init__(self, track = 0, channel = 0, note = 'A0', time = 0, duration = 0, volume = 0):
    self.track = track
    self.channel = channel
    self.pitch = notes_list.index(note) + 21
    self.time = time
    self.duration = duration
    self.volume = volume

  def get_values(self):
    return self.track, self.channel, self.pitch, self.time, self.duration, self.volume

