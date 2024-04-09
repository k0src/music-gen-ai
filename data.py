from mido import MidiFile
from music21 import converter, instrument, note, chord, stream
import csv

# Assumation - everything is a chord
# Chord = [note1, note2, note3, note4...]

def write_midi_to_csv(midi_files):
    with open('data.csv', mode='w', newline='') as csv_file:
        header = ['Genre', 'Key', 'Chords']
        writer = csv.DictWriter(csv_file, fieldnames=header)

        writer.writeheader()

        for midi in midi_files:
            prog_info = get_prog_info(midi)
            writer.writerow({'Genre': prog_info[0], 'Key': prog_info[1], 'Chords': ' ,'.join(prog_info[2:])})

def get_prog_info(midi):
    prog_info = []

    midistream = converter.parse(midi[1])

    prog_info.append(midi[0])

    key = midistream.analyze('key')
    prog_info.append(key.tonic.name + ' ' + key.mode)

    chordstream = midistream.chordify()

    for chord in chordstream.recurse().getElementsByClass('Chord'):
        chord_name = chord.commonName
        root_note = chord.root().name
        inversion = chord.inversion()
        prog_info.append((root_note + ' ' + chord_name + ' ' + str(inversion)))
    
    return prog_info

midi_files = [('Jazz', 'files/jazz_cmaj7am7dm7g7.mid'), 
              ('Jungle', 'files/jungle_cmin9gmin9.mid'), 
              ('Pop', 'files/pop_cmajgmajaminfmaj.mid'), 
              ('Rock', 'files/rock_emajc#minamajbmaj.mid'),
              ('Trap', 'files/trap_gmind#majgmingsus4.mid')]
              
write_midi_to_csv(midi_files)