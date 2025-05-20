from pydub import AudioSegment,silence
import os

def main():
    while True:
        print('Enter file, db threshold, length of silence to split on and amount to step over per iteration (both in ms) in form: fn,,thresh,,silence_len,,seek_step')
        print('If not entered, default values are -40 for threshold, 5000 for silence length, and 100 for step size. Adjust step size if not getting segments you expect but note lower = longer process time.')
        values = input('Enter q to quit. Enter <cwd> in file name to quickly join the cwd and your file name (<cwd> can be anywhere): ').split(',,')
        if len(values) < 4:
            if values[0] == 'q' or values[0] == 'Q':
                print('Ending.')
                break
            else:
                print(f"Couldn't properly parse. Param len: {len(values)}, input: {values}. Ensure you used ,, as the separator.\n")
                continue
        print()
        fn = values[0]
        if '<cwd>' in values[0]:
            fn = os.path.join(os.getcwd(),fn.replace('<cwd>',''))
        print('File to use:',fn)
        
        thresh = int(values[1]) or -40
        silence_len = int(values[2]) or 5000
        # If you don't get expected segments, change this to change how many ms to go per iteration. Using 1, while getting everything, would take forever.
        # 100 is a good point for most cases, taking about 5 seconds for a 6min audio file
        seek_step = int(values[3]) or 100
        
        audio = AudioSegment.from_wav(fn)
        audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,thresh,seek_step=seek_step)
        print('Segments:',audio_silent_list)
        for i,a in enumerate(audio_silent_list):
            opt_name: str = fn.replace('.wav', '_' + str(i).zfill(4) + '.wav')
            print(f'Iteration {i}, exporting {opt_name}...')
            a.export(opt_name,'wav')
        print('Done!\n')
        
    
if __name__ == '__main__':
    main()