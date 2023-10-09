#convert a semantic file to an mei file, following to 5.0 version standard
from enum import Enum
from music21 import *

class note_types(Enum):
    barline = 1
    clef = 2
    gracenote = 3
    multirest = 4
    note = 5
    rest = 6
    tie = 7
    timeSignature = 8
    
def main():
    s = stream.Stream()

    # Clef
    # To add a clef, you can use the following code:
    clefG2 = clef.GClef()
    s.append(clefG2)

    # Gracenote
    # To add a gracenote, you can use the following code:
    grace_note = note.Note("F#4", type='quarter', grace=True)
    s.append(grace_note)

    # Multirest
    # To add a multirest, you can use the following code:
    multirest = layout.MultiRest(4)  # Represents a multirest of 4 measures
    s.append(multirest)

    # Note
    # You've already added notes correctly in your code.
    n = note.Note("C4")
    s.append(n)

    # Rest
    # To add a rest, you can use the following code:
    rest = note.Rest()
    rest.duration.type = 'half'
    s.append(rest)

    # Tie
    # To add a tie, you need to create two notes and tie them together:
    note1 = note.Note("C4")
    note2 = note.Note("D4")
    tie = tie.Tie('start')  # Create a tie object
    note1.tie = tie
    s.append(note1)
    s.append(note2)

    # Time Signature
    # To add a time signature, you can use the following code:
    ts = meter.TimeSignature('4/4')
    s.append(ts)

    # Barline
    # To add a barline, you can use the following code:
    barline = layout.SystemLayout()
    barline.rightBarline = bar.Barline(style='light-light')
    s.append(barline)  
    s.write('musicxml', 'output.xml')
    
if __name__ == "__main__":
    main()