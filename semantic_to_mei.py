#convert a semantic file to an mei file, following to 5.0 version standard
from enum import Enum
from music21 import *
from semantic_obj import *
import argparse as ap

SEMANTIC_DELIMITER = "\t"

semantic_keywords_arr = ["barline", "clef", "gracenote", "keySignature", "multirest", "note", "rest", "tie", "timeSignature"]
supported_formats = ["mei", "xml"]

def semantic_duration_to_music21_duration(semantic_duration):
    for duration in LENGTHS:
        if duration in semantic_duration:
            if duration == "hundred_twenty_eighth":
                return "128th"
            elif duration == "sixty_fourth":
                return "64th"
            elif duration == "thirty_second":
                return "32nd"
            elif duration == "sixteenth":
                return "16th"
            elif duration == "double_whole":
                return "breve"
            elif duration == "quadruple_whole":
                return "longa"
            else:
                return duration
    raise Exception("Invalid duration: " + semantic_duration)

def semantic_to_music21_stream(semantic_score):
    #create a music21 stream
    s = stream.Stream()
    current_measure = stream.Measure(number=1)
    tie_next = False
    
    #iterate through the semantic score, and build the music21 stream
    for word in semantic_score:
        for keyword in semantic_keywords_arr:
            if keyword in word:     
                if keyword=="clef":
                    c = semantic_clef(word)
                    #set the clef line
                    if "C" in c.clef:
                        s.append(clef.CClef())
                    elif "G" in c.clef:
                        s.append(clef.GClef())
                    elif "F" in c.clef:
                        s.append(clef.FClef())
                    else:
                        raise Exception("Invalid clef: " + c.clef)
                    s[-1].line = c.clef[-1]
                elif keyword=="barline":
                    s.append(current_measure)
                    current_measure = stream.Measure(number=current_measure.number + 1)
                    current_measure.clear()
                    
                elif keyword =="keySignature":
                    ks = semantic_key_signature(word)
                    current_measure.append(key.KeySignature(ks.value))
                    
                elif keyword =="note" or keyword=="gracenote":
                    n = semantic_note(word)
                    m21_note = note.Note()
                    m21_note.pitch = pitch.Pitch(n.pitch.replace("b", "-"))
                    m21_note.duration.type = semantic_duration_to_music21_duration(n.length)
                    
                    if(n.dot == "single"):
                        m21_note.duration.dots = 1
                    elif(n.dot == "double"):
                        m21_note.duration.dots = 2
                    elif(n.dot == "none"):
                        m21_note.duration.dots = 0
                        
                    # if(n.grace):
                    #     m21_note.duration.grace = True
                        
                    if(n.fermata):
                        m21_note.expressions.append(expressions.Fermata())
                        
                    if(tie_next):
                        m21_note.tie = tie.Tie("stop")
                        tie_next = False
                    
                    #turn off padding
                    m21_note.paddingLeft = 0
                    m21_note.paddingRight = 0
                    current_measure.append(m21_note)
                elif keyword =="rest":
                    r = semantic_rest(word)
                    m21_rest = note.Rest()
                    m21_rest.duration.type = semantic_duration_to_music21_duration(r.length)
                    current_measure.append(m21_rest)
                    
                elif keyword =="multirest":
                    mr = semantic_multirest(word)
                    for i in range(int(mr.length) - 1):
                        #get the duration of the current measure from the time signature
                        r = note.Rest("quarter", fullMeasure=True)
                        current_measure.append(r)
                        s.append(current_measure)
                        current_measure = stream.Measure(number=current_measure.number + 1)
                    r = note.Rest("quarter", fullMeasure=True)
                    current_measure.append(r)
                       
                    
                elif keyword =="tie":
                    current_measure[-1].tie = tie.Tie("start")
                    tie_next = True
                 
                    
                elif keyword =="timeSignature":
                    ts = semantic_time_signature(word)
                    current_measure.append(meter.TimeSignature(ts.time_signature))
                
                else:
                    raise Exception("Unimplemented keyword: " + keyword)
                
                break
    if(len(current_measure) > 0):
        s.append(current_measure)

    return s

def main(semantic_file, output_type, output, title, artist):
    if output_type not in supported_formats:
        raise Exception("Unsupported output format: " + output_type)
    
    #read the semantic file
    semantic_file = open(semantic_file, "r")
    semantic_contents = semantic_file.read().split(SEMANTIC_DELIMITER)
    semantic_file.close()
    print(semantic_contents)
    s = semantic_to_music21_stream(semantic_contents)
    
    #name the output file
    s.metadata = metadata.Metadata()
    s.metadata.title = title
    s.metadata.composer = artist

    s.write("musicxml", fp=output+"." +output_type)
    
        
    #show the output file
    if args.show:
        s.show("text")
        
    
if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Convert a semantic file to an MEI file")
    parser.add_argument("semantic_file", help="The semantic file to convert")
    parser.add_argument("-type", "--output_type", help="The type of file to output to. Defaults to MEI.\nFormats: " + str(supported_formats), default="musicxml")
    parser.add_argument("-o", "--output", help="The file to output to. Defaults to output", default="output")
    parser.add_argument("--show", help="Show the output file in a music21 window", action="store_true")
    parser.add_argument("--title", help="The title of the score", default="Untitled")
    parser.add_argument("--artist", help="The artist of the score", default="Unknown")
    args = parser.parse_args()
    main(args.semantic_file, args.output_type, args.output, args.title, args.artist)
    
    