# Rename files based on the first couple of words spoken in them
# Assumes base audio files are in cwd/files, output in cwd/opt, and backs up files in cwd/backup
# If no speech detected, puts "errunknown" in the filename for easy identifying

import speech_recognition as sr
import os
import shutil
r = sr.Recognizer()
        
folder = './files'
backup_folder = os.path.join(folder,'backup')
output_folder = os.path.join(folder,'opt')
# remove files in output folder
for i,j,k in os.walk(output_folder):
    for file in k:
        os.remove(os.path.join(output_folder,file))

for i,folders,files in os.walk(folder):
    files.sort()
    # print(folders)
    # print(files)
    for count,file in enumerate(files):
        full_name = os.path.join(folder,file)
        shutil.copy(full_name,backup_folder + '/')
        shutil.copy(full_name,backup_folder + '/' + 'backup_' + file)
        au = sr.AudioFile(full_name)
        new_name = os.path.splitext(file)[0] + '_'
        with au as f:
            audio = r.record(f)
            print(f'File: {file}, ',end='')
            try:
                s = r.recognize_google(audio)
                print(f'File: {file}, Speech: {s}')
                words: list = s.split(' ')
                for i in range(len(words)):
                    if i < 5:
                        new_name += words[i] + '_'
                new_name = new_name[0:len(new_name) - 1] + '.wav'
                if len(new_name) < 1:
                    print('Error: name was too small')  
            except Exception as e:
                print(f"Exception occured. Most likely couldn't detect any words in file {file}. Exception: {e}")
                new_name += 'errunknown'
        if os.path.exists(os.path.join(output_folder,new_name)):
            i = 0
            while os.path.exists(os.path.join(output_folder,new_name + '_'+str(i).zfill(4))):
                i += 1
            os.rename(full_name,os.path.join(output_folder,new_name + '_'+str(i).zfill(4)))
        else:
            os.rename(full_name,os.path.join(output_folder,new_name))
        os.rename(os.path.join(backup_folder,file),full_name)
    break
# with hellow as source:
#     audio = r.record(source)
# try:
#     s = r.recognize_google(audio)
#     print("Text: "+s)
# except Exception as e:
#     print("Exception: "+str(e))
