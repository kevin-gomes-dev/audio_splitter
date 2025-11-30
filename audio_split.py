# Handles splitting an audio file by the silences. Accepts splitting once with params or searching for a split count given some max and min values of params
from pydub import AudioSegment,silence
import os
import time
def split_audio(audio,silence_len,thresh,seek_step,keep_silence = 100):
    # min_len = 0
    # max_len = 50000
    # silences = silence.detect_silence(audio,silence_len,thresh,seek_step)
    # print(f'Silences: {len(silences)}')
    audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,thresh,seek_step=seek_step,keep_silence=keep_silence)
    # last_silence = 0
    # audio_silent_list = []
    # for range in silences:
    #     print(range)
    #     if  range[1] - last_silence > min_len and range[1] - last_silence < max_len:        
    #         audio_silent_list.append(audio[last_silence:range[1]])
    #         last_silence = range[1]
    print('Segment count:',len(audio_silent_list))
    return audio_silent_list

# Returns list of aug segs where len = expected count, or empty list if cannot be found
# Increments keep_silence, seek_step,silence_len by 100 each iteration, and thresh by 1.
# Does this by first changing individual values, then if nothing found, will do an entire combination search
# Tests all possible combinations until either we find a split or time is up, defaults to 1 min (60000ms)
# If count = 0, will ask each iteration if you wish to export what it found.
def find_split_count(audio,expected_count = 0,silence_len = 5000,max_silence_len = 5000,thresh = -40,max_thresh = -40,seek_step = 100,max_seek_step = 100,keep_silence = 100, max_keep_silence = 100,inc = 100, stop_time = 60000):
    if stop_time == 0 or not stop_time:
        print("WARNING: Will go until reaching all max values as no end timer was given.")
        timer = lambda x,y: False
    return_segs = []
    nano_to_ms = 1000000.0
    start_time = time.time_ns() / nano_to_ms
    actual_start_time = start_time
    print(f'Start time: {start_time}\n')
    
    # Check each combination with loops
    print('Checking incrementing silence len...')
    temp_silence_len = silence_len
    while temp_silence_len <= max_silence_len:
        print(f'Current silence len: {temp_silence_len}')
        audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,temp_silence_len,thresh,seek_step=seek_step,keep_silence=keep_silence)
        # test = silence.detect_silence(audio,temp_silence_len,thresh,seek_step)
        if len(audio_silent_list) == expected_count:
            print('Expected count reached! Returning list of audio segs.')
            print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
            return audio_silent_list
        elif expected_count == 0:
            export_now = input(f'Audio files to export: {len(audio_silent_list)}, proceed? ')
            if export_now == 'y':
                return audio_silent_list
        temp_silence_len += inc
        if timer(start_time,stop_time):
            print('Timer reached.')
            break
        
    start_time = time.time_ns() / nano_to_ms
    # Check incrementing thresh
    print('Checking incrementing thresh...')
    temp_thresh = thresh
    while temp_thresh <= max_thresh:
        print(f'Current thresh: {temp_thresh}')
        audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,temp_thresh,seek_step=seek_step,keep_silence=keep_silence)
        if len(audio_silent_list) == expected_count:
            print('Expected count reached! Returning list of audio segs.')
            print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
            return audio_silent_list
        elif expected_count == 0:
            export_now = input(f'Audio files to export: {len(audio_silent_list)}, proceed? ')
            if export_now == 'y':
                return audio_silent_list
        temp_thresh += 1
        if timer(start_time,stop_time):
            print('Timer reached.')
            break
    
    start_time = time.time_ns() / nano_to_ms
    # Check incrementing seek step
    print('Checking incrementing seek step...')
    temp_seek_step = seek_step
    while temp_seek_step <= max_seek_step:
        print(f'Current seek step: {temp_seek_step}')
        audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,thresh,seek_step=temp_seek_step,keep_silence=keep_silence)
        if len(audio_silent_list) == expected_count:
            print('Expected count reached! Returning list of audio segs.')
            print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
            return audio_silent_list
        elif expected_count == 0:
            export_now = input(f'Audio files to export: {len(audio_silent_list)}, proceed? ')
            if export_now == 'y':
                return audio_silent_list
        temp_seek_step += inc
        if timer(start_time,stop_time):
            print('Timer reached.')
            break
    
    start_time = time.time_ns() / nano_to_ms
    # Check incrementing keep silence
    print('Checking incrementing keep silence...')
    temp_keep_silence = keep_silence
    while temp_keep_silence <= max_keep_silence:
        print(f'Current keep silence: {temp_keep_silence}')
        audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,thresh,seek_step=seek_step,keep_silence=temp_keep_silence)
        if len(audio_silent_list) == expected_count:
            print('Expected count reached! Returning list of audio segs.')
            print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
            return audio_silent_list
        elif expected_count == 0:
            export_now = input(f'Audio files to export: {len(audio_silent_list)}, proceed? ')
            if export_now == 'y':
                return audio_silent_list
        temp_keep_silence += inc
        if timer(start_time,stop_time):
            print('Timer reached.')
            break
    
    print('\nNo list found. Running exhaustive loops.\n')
    
    # Run all loops nested such that every combination is found.
    temp_keep_silence = keep_silence
    temp_seek_step = seek_step
    temp_silence_len = silence_len
    temp_thresh = thresh
    i = 0
    while temp_silence_len <= max_silence_len:
        while temp_keep_silence <= max_keep_silence:
            while temp_seek_step <= max_seek_step:
                while temp_thresh <= max_thresh:
                    print(f'Iteration {i}: silence_len: {temp_silence_len}, keep_silence: {temp_keep_silence}, seek_step: {temp_seek_step}, thresh: {temp_thresh}')
                    audio_silent_list: list[AudioSegment] = silence.split_on_silence(audio,silence_len,thresh,seek_step=seek_step,keep_silence=temp_keep_silence)
                    if len(audio_silent_list) == expected_count:
                        print('Expected count reached! Returning list of audio segs.')
                        print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
                        return audio_silent_list
                    elif expected_count == 0:
                        export_now = input(f'Audio files to export: {len(audio_silent_list)}, proceed? ')
                        if export_now == 'y':
                            return audio_silent_list
                    temp_thresh += 1
                    i += 1
                    if timer(start_time,stop_time):
                        print('Timer reached.')
                        return []
                temp_thresh = thresh
                temp_seek_step += inc
            
            temp_seek_step = seek_step
            temp_keep_silence += inc
        
        temp_keep_silence = keep_silence
        temp_silence_len += inc
    print('No list found. Returning empty list.')
    print(f'Total time taken, in minutes: {(time.time_ns() / nano_to_ms - actual_start_time)/1000/60}')
    return []
    

def timer(start_time,stop_time):
    nano_to_ms = 1000000.0
    if time.time_ns() / nano_to_ms - start_time > stop_time:
        print(f"Allotted time passed. Time passed: {time.time_ns() / nano_to_ms - start_time}.")
        return True
    return False
    
def main():
    # fn, thresh, silence, seek, keep
    first_defaults = ['test.wav',-50,1400,100,800]
    # count, max silence, max thresh, max step, max keep, inc, time ms
    second_defaults = [0,1500,-50,100,800,100,0]
    use_defaults = True
    while True:
        if use_defaults:
            print('Using defaults.')
            fn,thresh,silence_len,seek_step,keep_silence = [i for i in first_defaults]
        else:
            print('Enter file, db threshold, length of silence to split on, amount to step over per iteration and keep_silence (all ms) in form: fn,thresh,silence_len,seek_step,keep_silence')
            print('If not entered, default values are -40 for threshold, 5000 for silence length, and 100 for step size. Adjust step size if not getting segments you expect but note lower = longer process time.')
            values = input('Enter q to quit. Enter <cwd> in file name to quickly join the cwd and your file name (<cwd> can be anywhere): ').split(',')
            if len(values) < 5:
                if values[0] == 'q' or values[0] == 'Q':
                    print('Ending.')
                    break
                elif len(values) == 1 and values[0]:
                    print(f"Assuming input given was file name. Using default params with given file: {values[0]}")
                    for i in range(0,4):
                        values.append(None)
                else:
                    print(f"Couldn't properly parse. Param len: {len(values)}, input: {values}. Ensure you used , as the separator.\n")
                    continue
            print()
            fn = values[0]
            if '<cwd>' in values[0]:
                fn = os.path.join(os.getcwd(),fn.replace('<cwd>',''))
            print('File to use:',fn)
            
            thresh = values[1] or -40
            silence_len = values[2] or 5000
            # If you don't get expected segments, change this to change how many ms to go per iteration. Using 1, while getting everything, would take forever.
            # 100 is a good point for most cases, taking about 5 seconds for a 6min audio file
            seek_step = values[3] or 100
            keep_silence = values[4] or 100
            # Do converts after to avoid crash
            thresh = int(thresh)
            silence_len = int(silence_len)
            seek_step = int(seek_step)
            keep_silence = int(keep_silence)
        audio = AudioSegment.from_wav(fn)
        
        print(f"Thresh - {thresh}, silence_len - {silence_len}, seek_step: {seek_step}, keep_silence: {keep_silence}")
        mode = input('Enter mode. 1 for split using settings, 2 for finding a split given some count: ')
        if mode == '1':
            audio_list = split_audio(audio,silence_len,thresh,seek_step)
        elif mode == '2':
            if use_defaults:
                print('Using second defaults')
                ct,m_s_l,m_t,m_s_s,m_k_s,inc,stop_time = [int(i) for i in second_defaults]
            else:
                find_params = input('Enter , separated count, max silence len, max thresh, max seek step, max keep_silence, increment to use and stop time: ').split(',')
                if len(find_params) < 7:
                    print('Not enough args given, using defaults.')
                    ct = 0
                    m_s_l = 5000
                    m_t = -40
                    m_s_s = 100
                    m_k_s = 100
                    inc = 100
                    stop_time = 10000
                else:
                    ct,m_s_l,m_t,m_s_s,m_k_s,inc,stop_time = [int(i) for i in find_params]
            print(f'Running with count = {ct}, max_silence_len = {m_s_l}, max_thresh = {m_t}, max seek step = {m_s_s}, max keep silence = {m_k_s}, inc = {inc}, stop time = {stop_time}')
            audio_list = find_split_count(audio,ct,silence_len,m_s_l,thresh,m_t,seek_step,m_s_s,keep_silence,m_k_s,inc,stop_time)
        else:
            print('No mode found.')
            continue
        for i,a in enumerate(audio_list):
            opt_name: str = fn.replace('.wav', '_' + str(i).zfill(4) + '.wav')
            print(f'Iteration {i}, exporting {opt_name}...')
            a.export(opt_name,'wav')
        print()
    

    

if __name__ == '__main__':
    main()