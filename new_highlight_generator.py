import cv2
import sys
from pynput.keyboard import HotKey, Key, Listener
from os import listdir
from shutil import copyfile, move
from time import sleep, time

# Get team names, map names, and file locations from user
correct_input = False
while not correct_input:
    teams = []
    teams.append(input('Enter the name of team 1: '))
    teams.append(input('Enter the name of team 2: '))

    num_maps = int(input('Enter number of maps: '))
    maps = []
    for i in range(num_maps):
        maps.append(input('Enter the name of map {}: '.format(i + 1)))
    print('')
    print('=======================')
    print('Teams:')
    print(*teams, sep=', ')
    print('')
    print('Maps:')
    print(*maps, sep=', ')
    print('=======================')
    print('')
    answer = input('Is this information correct? (y/n) ')
    correct_response = False
    while not correct_response:
        if answer == 'y' or answer == 'Y':
            correct_input = True
            break
        elif answer == 'n' or answer == 'N':
            break
        else:
            print('')
            answer = input('Please enter \'y\' for yes or \'n\' for no: ')

print('')
print('Press f5 to add clips to the highlight.  Press f6 to end clip collection for the map.')
print('')
print('=======================')
print('Beginning ' + maps[0] + ' clip collection...')
out = cv2.VideoWriter('current_highlights.mp4',
                      cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                      60, (1920, 1080), 1)
map_number = 0
new_highlight = True
begin_frames = []
previous_frames = []


def refresh():
    global map_number, new_highlight, begin_frames, previous_frames
    clips = [n for n in listdir('clips') if n[:3] == 'rep' and n[-4:] == '.mp4']
    total_clips = len(clips)

    for index, clip in enumerate(clips):
        cap = cv2.VideoCapture('clips/' + clip)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0
        start_time = time()
        print('')
        print('Adding clip {}/{}'.format(index + 1, total_clips))
        end_frames = []

        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                cap.release()
                break
            if frame_count < 60 and new_highlight:
                begin_frames.append(frame)
            elif frame_count < 60:
                new_frame = cv2.addWeighted(previous_frames[frame_count], (60 - frame_count) / 60, frame,
                                            frame_count / 60, 0)
                out.write(new_frame)
            elif total_frames - frame_count <= 61:
                end_frames.append(frame)
            else:
                out.write(frame)

            frame_count += 1
            if frame_count % 10 == 0:
                print('{:2.2f}% done, {:2.2f}s'.format(100 * frame_count / total_frames, time() - start_time), end='\r')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print('End of clip, time elasped: ' + str(time() - start_time))
        previous_frames = end_frames
        new_highlight = False
        move('clips/' + clip, 'clips/old_clips/' + clip)


def stop():
    global map_number, out, new_highlight, begin_frames, previous_frames
    start_time = time()
    if not begin_frames:
        print('')
        print('No clips were added... skipping map')
        print('Ending ' + maps[map_number] + ' clip collection')
        print('=======================')
        out.release()
    else:
        print('')
        print('Adding last frames...')
        for frame_count in range(60):
            new_frame = cv2.addWeighted(previous_frames[frame_count], (60 - frame_count) / 60, begin_frames[frame_count],
                                        frame_count / 60, 0)
            out.write(new_frame)
        new_highlight = True
        begin_frames = []
        previous_frames = []
        print('Ending ' + maps[map_number] + ' clip collection')
        print('=======================')
        out.release()
        copyfile('current_highlights.mp4', 'highlights/{} vs {} {}.mp4'.format(teams[0], teams[1], maps[map_number]))
        copyfile('current_highlights.mp4', 'highlight_reel.mp4')
    map_number += 1
    cv2.destroyAllWindows()
    if map_number >= num_maps:
        input('Goodbye :)')
        sys.exit()
    else:
        out = cv2.VideoWriter('current_highlights.mp4',
                              cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                              60, (1920, 1080), 1)
        print('')
        print('=======================')
        print('Beginning ' + maps[map_number] + ' clip collection')


hotkey1 = HotKey(
    [Key.f5],
    refresh
)
hotkey2 = HotKey(
    [Key.f6],
    stop
)
hotkeys = [hotkey1, hotkey2]


def signal_press_to_hotkeys(key):
    for hotkey in hotkeys:
        hotkey.press(l.canonical(key))
        hotkey.release(l.canonical(key))


with Listener(on_press=signal_press_to_hotkeys) as l:
    l.join()
