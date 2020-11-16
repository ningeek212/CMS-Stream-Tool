import cv2
import sys
from pynput.keyboard import HotKey, Key, Listener
from os import listdir
from os.path import getsize
from shutil import copyfile, move
from time import sleep, time
from threading import Thread

# TODO: Define these constants using a GUI
LATEST_INSTANT_REPLAY_FILENAME = "latest_replay.mp4"
CURRENT_INSTANT_REPLAY_FILENAME = "current_replay.mp4"
LATEST_HIGHLIGHT_REEL_FILENAME = "latest_highlights.mp4"
CURRENT_HIGHLIGHT_REEL_FILENAME = "highlight_reel.mp4"
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 60
teams = ['1', '2']
maps = ['a', 'b', 'c']
num_maps = 3

# # Get team names, map names, and file locations from user
# correct_input = False
# while not correct_input:
#     teams = []
#     teams.append(input('Enter the name of team 1: '))
#     teams.append(input('Enter the name of team 2: '))
#
#     num_maps = int(input('Enter number of maps: '))
#     maps = []
#     for i in range(num_maps):
#         maps.append(input('Enter the name of map {}: '.format(i + 1)))
#     print('')
#     print('=======================')
#     print('Teams:')
#     print(*teams, sep=', ')
#     print('')
#     print('Maps:')
#     print(*maps, sep=', ')
#     print('=======================')
#     print('')
#     answer = input('Is this information correct? (y/n) ')
#     correct_response = False
#     while not correct_response:
#         if answer == 'y' or answer == 'Y':
#             correct_input = True
#             break
#         elif answer == 'n' or answer == 'N':
#             break
#         else:
#             print('')
#             answer = input('Please enter \'y\' for yes or \'n\' for no: ')

print('')
print('Press f5 to save clip for instant replay.  Press f6 to end clip collection for the map.')
print('')
print('=======================')
print('Beginning ' + maps[0] + ' clip collection...')
map_number = 0
new_highlight = True
begin_frames = []
previous_frames = []


class HighlightGenerator:
    def __init__(self):
        self.out = cv2.VideoWriter(LATEST_HIGHLIGHT_REEL_FILENAME,
                                   cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                   VIDEO_FPS, (VIDEO_WIDTH, VIDEO_HEIGHT), 1)
        self.map_number = 0
        self.new_highlight = True
        self.begin_frames = []
        self.previous_frames = []
        self.processing_clip = False
        self.processing_high = False
        pass

    def refresh(self, file_path):
        if self.processing_high:
            pass
        self.processing_clip = True
        cap = cv2.VideoCapture(file_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0
        start_time = time()
        print('')
        print('Adding {0}'.format(file_path))
        end_frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                break
            # If this clip is the first of a new highlight, store the first second of the clip.
            elif frame_count < VIDEO_FPS and self.new_highlight:
                self.begin_frames.append(frame)
            # Add fade transition effect between the previous clip and current clip
            elif frame_count < VIDEO_FPS:
                new_frame = cv2.addWeighted(self.previous_frames[frame_count], (VIDEO_FPS - frame_count) / VIDEO_FPS,
                                            frame, frame_count / VIDEO_FPS, 0)
                self.out.write(new_frame)
            # Store the last second of the clip
            elif total_frames - frame_count <= VIDEO_FPS + 1:
                end_frames.append(frame)
            else:
                self.out.write(frame)

            frame_count += 1
            if frame_count % 10 == 0:
                print('{:2.2f}% done, {:2.2f}s'.format(100 * frame_count / total_frames, time() - start_time), end='\r')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print('End of clip, time elapsed: ' + str(time() - start_time))
        self.previous_frames = end_frames
        self.new_highlight = False
        new_file_path = 'old_clips/{0}'.format(file_path[6:])
        move(file_path, new_file_path)
        self.processing_clip = False

    def stop(self):
        if self.processing_clip:
            print('')
            print('Still processing a clip')
            pass
        elif not self.begin_frames:
            self.processing_high = True
            print('')
            print('No clips were added... skipping map')
            print('Ending ' + maps[self.map_number] + ' clip collection')
            print('=======================')
            self.out.release()
        else:
            self.processing_high = True
            print('')
            print('Adding last frames...')
            for frame_count in range(VIDEO_FPS):
                new_frame = cv2.addWeighted(self.previous_frames[frame_count], (VIDEO_FPS - frame_count) / VIDEO_FPS,
                                            self.begin_frames[frame_count], frame_count / VIDEO_FPS, 0)
                self.out.write(new_frame)
            self.new_highlight = True
            self.begin_frames = []
            self.previous_frames = []
            print('Ending ' + maps[self.map_number] + ' clip collection')
            print('=======================')
            self.out.release()
            copyfile(LATEST_HIGHLIGHT_REEL_FILENAME,
                     'highlights/{} vs {} {}.mp4'.format(teams[0], teams[1], maps[self.map_number]))
            copyfile(LATEST_HIGHLIGHT_REEL_FILENAME, CURRENT_HIGHLIGHT_REEL_FILENAME)

        self.processing_high = False
        self.map_number += 1
        cv2.destroyAllWindows()

        if self.map_number >= num_maps:
            input('Goodbye :)')
            replay_checker.checking = False  # stop checking for replays (thread will stop as a result)
            sys.exit()
        else:
            self.out = cv2.VideoWriter(LATEST_HIGHLIGHT_REEL_FILENAME,
                                       cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                       VIDEO_FPS, (VIDEO_WIDTH, VIDEO_HEIGHT), 1)
            print('')
            print('=======================')
            print('Beginning ' + maps[self.map_number] + ' clip collection')


class ReplayChecker:
    def __init__(self, hg, folder, keyword, latest_clip_path):
        self.highlight_generator = hg
        self.obs_output_folder = folder
        self.keyword = keyword
        self.thread = Thread(target=self.check_loop, daemon=True)
        self.latest_clip_path = latest_clip_path
        self.checking = True

    def start(self):
        self.thread.start()

    @staticmethod
    def check_file_finished(file_path, samples, interval):
        file_size_list = []
        for x in range(0, samples):
            file_size = getsize(filename=file_path)  # sample the file size of the replay being saved by OBS
            file_size_list.append(file_size)
            sleep(interval)
        outcome = all(x == file_size_list[0] for x in file_size_list)  # checks to see if last 10 samples are equal
        return outcome

    def check_loop(self):
        while self.checking:
            for path in listdir(self.obs_output_folder):
                if self.keyword in path:
                    print("New replay detected, waiting for file to be complete")
                    file_path = self.obs_output_folder + "/" + path
                    if self.check_file_finished(file_path, 10, 0.1):
                        print("File complete")
                        copyfile(file_path, self.latest_clip_path)  # for instant replay
                        self.highlight_generator.refresh(file_path)
                    else:
                        sleep(1)


def update_instant_replay():
    print("Copying latest replay to OBS source...")
    copyfile(LATEST_INSTANT_REPLAY_FILENAME, CURRENT_INSTANT_REPLAY_FILENAME)
    print("Finished copying")


highlight_generator = HighlightGenerator()

stop_hotkey = HotKey([Key.f6], highlight_generator.stop)

instant_replay_hotkey = HotKey([Key.f5], update_instant_replay)

hotkeys = [stop_hotkey, instant_replay_hotkey]


def signal_press_to_hotkeys(key):
    for hotkey in hotkeys:
        hotkey.press(l.canonical(key))
        hotkey.release(l.canonical(key))


replay_checker = ReplayChecker(highlight_generator, "clips", "replay", LATEST_INSTANT_REPLAY_FILENAME)
replay_checker.start()

with Listener(on_press=signal_press_to_hotkeys) as l:
    l.join()
