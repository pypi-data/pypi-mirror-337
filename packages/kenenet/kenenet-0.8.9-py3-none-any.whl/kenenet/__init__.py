import inspect, sys, zhmiscellany, keyboard, mss, time, linecache, types, os, random, pyperclip, inspect, datetime, atexit, re
import numpy as np
from PIL import Image
from collections import defaultdict

from pydub import AudioSegment
from pydub.playback import play
import random
import threading
import pyaudio
import time
from pydub import AudioSegment
from zhmiscellany._processing_supportfuncs import _ray_init_thread
import zhmiscellany.processing
global timings, ospid, debug_mode
ospid, debug_mode = None, False
timings = {}

def quick_print(message, l=None):
    if l: sys.stdout.write(f"\033[38;2;0;255;26m{l} || {message}\033[0m\n")
    else: sys.stdout.write(f"\033[38;2;0;255;26m {message}\033[0m\n")

def get_pos(key='f10', kill=False):
    coord_rgb = []
    coords = []
    def _get_pos(key, kill=False):
        while True:
            keyboard.wait(key)
            x, y = zhmiscellany.misc.get_mouse_xy()
            with mss.mss() as sct:
                region = {"left": x, "top": y, "width": 1, "height": 1}
                screenshot = sct.grab(region)
                rgb = screenshot.pixel(0, 0)
            color = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
            reset = "\033[38;2;0;255;26m"
            coord_rgb.append({'coord': (x,y), 'RGB': rgb})
            coords.append((x,y))
            pyperclip.copy(f'coords_rgb = {coord_rgb}\ncoords = {coords}')
            quick_print(f"Added Coordinates: ({x}, {y}), RGB: {rgb} {color}████████{reset} to clipboard", lineno)
            if kill:
                quick_print('killing process')
                zhmiscellany.misc.die()
    quick_print(f'Press {key} when ever you want the location')
    frame = inspect.currentframe().f_back
    lineno = frame.f_lineno
    _get_pos(key, kill)

def timer(clock=1):
    if clock in timings:
        elapsed = time.time() - timings[clock][0]
        frame = inspect.currentframe().f_back
        lineno = frame.f_lineno
        if clock == 1:
            quick_print(f'Timer took \033[97m{elapsed}\033[0m seconds', f'{lineno}-{timings[clock][1]}')
        else:
            quick_print(f'Timer {clock} took \033[97m{elapsed}\033[0m seconds', f'{lineno}-{timings[clock][1]}')
        del timings[clock]
        return elapsed
    else:
        ct = time.time()
        frame = inspect.currentframe().f_back
        lineno = frame.f_lineno
        timings[clock] = (ct, lineno)

class _Config:
    EXCLUDED_NAMES = {'Config', 'VariableTracker', 'track_variables', 'stop_tracking',
                      'track_frame', 'sys', 'inspect', 'types', 'datetime', 'quick_print',
                      'self', 'cls', 'args', 'kwargs', '__class__'}
    EXCLUDED_FILES = {'<string>', '<frozen importlib', 'importlib', 'abc.py', 'typing.py', '_collections_abc.py'}
    SHOW_TIMESTAMPS = True
    EXCLUDE_INTERNALS = True

class _VariableTracker:
    _instance = None
    
    @classmethod
    def _get_instance(cls):
        if cls._instance is None:
            cls._instance = _VariableTracker()
        return cls._instance
    
    def __init__(self):
        self.active = False
        self.frame_locals = {}
        self.global_vars = {}
    
    def _format_value(self, value):
        try:
            return repr(value)
        except:
            return f"<{type(value).__name__} object>"
    
    def _print_change(self, name, old, new, lineno, scope="Global"):
        quick_print(f"{scope} '{name}' changed from {self._format_value(old)} -> {self._format_value(new)}", lineno)
    
    def _should_track(self, name):
        return not (name.startswith('_') and name not in ('__name__', '__file__')) and name not in _Config.EXCLUDED_NAMES
    
    def _start_tracking(self, module_name):
        if self.active: return
        module = sys.modules[module_name]
        self.global_vars = {name: value for name, value in module.__dict__.items() if self._should_track(name)}
        sys.settrace(_track_frame)
        self.active = True
        frame = inspect.currentframe().f_back.f_back
        lineno = frame.f_lineno
        quick_print(f"Started debugging", lineno)
    
    def _stop_tracking(self):
        if not self.active: return
        sys.settrace(None)
        self.frame_locals.clear()
        self.global_vars.clear()
        self.active = False
        frame = inspect.currentframe().f_back.f_back
        lineno = frame.f_lineno
        quick_print(f"Stopped debugging", lineno)

def _track_frame(frame, event, arg):
    tracker = _VariableTracker._get_instance()
    if not tracker.active or event != 'line': return _track_frame
    # Skip tracking if function name is 'quick_print'
    if frame.f_code.co_name == 'quick_print':
        return _track_frame
    scope = "Global" if frame.f_code.co_name == '<module>' else f"Local in '{frame.f_code.co_name}'"
    current_vars = {name: value for name, value in (frame.f_locals if scope != "Global" else frame.f_globals).items() if tracker._should_track(name)}
    line_number = frame.f_lineno  # Capture the line number where the change occurred
    if scope == "Global":
        for name, value in current_vars.items():
            if name not in tracker.global_vars:
                tracker._print_change(name, None, value, line_number, scope)
            elif tracker.global_vars[name] != value:
                tracker._print_change(name, tracker.global_vars[name], value, line_number, scope)
        tracker.global_vars.update(current_vars)
    else:
        frame_id = id(frame)
        if frame_id not in tracker.frame_locals:
            for name, value in current_vars.items():
                tracker._print_change(name, None, value, line_number, scope)
        else:
            for name, value in current_vars.items():
                if name not in tracker.frame_locals[frame_id]:
                    tracker._print_change(name, None, value, line_number, scope)
                elif tracker.frame_locals[frame_id][name] != value:
                    tracker._print_change(name, tracker.frame_locals[frame_id][name], value, line_number, scope)
        tracker.frame_locals[frame_id] = current_vars
    if event == 'return' and scope != "Global": del tracker.frame_locals[id(frame)]
    return _track_frame


def debug():
    global debug_mode
    if not debug_mode:
        debug_mode = True
        caller_frame = inspect.currentframe().f_back
        module_name = caller_frame.f_globals['__name__']
        tracker = _VariableTracker._get_instance()
        tracker._start_tracking(module_name)
        caller_frame.f_trace = _track_frame
    else:
        debug_mode = False
        _VariableTracker._get_instance()._stop_tracking()

def pp(msg='caca', subdir=None, pps=3):
    import os, subprocess
    os_current = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    if subdir: os.chdir(subdir)
    def push(message):
        os.system('git add .')
        os.system(f'git commit -m "{message}"')
        os.system('git push -u origin master')
    def pull():
        os.system('git pull origin master')
    def push_pull(message):
        push(message)
        pull()
    result = subprocess.run(['git', 'rev-list', '--count', '--all'], capture_output=True, text=True)
    result = int(result.stdout.strip()) + 1
    for i in range(pps):
        push_pull(msg)
    quick_print('PP finished B======D')
    os.chdir(os_current)

def save_img(img, name=' ', reset=True, file='temp_screenshots', mute=False):
    global ospid
    if os.path.exists(file):
        if reset and ospid is None:
            zhmiscellany.fileio.empty_directory(file)
            quick_print(f'Cleaned folder {file}')
    else:
        quick_print(f'New folder created {file}')
        zhmiscellany.fileio.create_folder(file)
    ospid = True
    frame = inspect.currentframe().f_back
    lineno = frame.f_lineno
    if isinstance(img, np.ndarray):
        save_name = name + f'{time.time()}'
        img = Image.fromarray(img)
        img.save(fr'{file}\{save_name}.png')
        if not mute: quick_print(f'Saved image as {save_name}', lineno)
    else:
        quick_print(f"Your img is not a fucking numpy array you twat, couldn't save {name}", lineno)


class AudioPlayer:
    def __init__(self, file):
        self.file = file
        self.active_audio = {}
    
    def _stream_audio(self, sound, stop_event, chunk=1024):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(sound.sample_width),
            channels=sound.channels,
            rate=sound.frame_rate,
            output=True
        )
        raw_data = sound.raw_data
        for i in range(0, len(raw_data), chunk):
            if stop_event.is_set():
                break
            stream.write(raw_data[i:i + chunk])
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    class _AudioLooper:
        def __init__(self, sound, stop_event, stream_func, loop=True):
            self.sound = sound
            self.loop = loop
            self.stop_event = stop_event
            self.stream_func = stream_func
            self.thread = threading.Thread(target=self._loop_audio, name="AudioLooperThread", daemon=True)
            self.thread.start()
        
        def _loop_audio(self):
            while not self.stop_event.is_set():
                self.stream_func(self.sound, self.stop_event)
                if not self.loop:
                    break
        
        def stop(self):
            self.stop_event.set()
            self.thread.join()
    
    def play(self, loop=False, range=(0.9, 1.1)):
        file_sound = AudioSegment.from_mp3(self.file)._spawn(
            AudioSegment.from_mp3(self.file).raw_data,
            overrides={'frame_rate': int(AudioSegment.from_mp3(self.file).frame_rate * random.uniform(*range))}
        )
        stop_event = threading.Event()
        looper = self._AudioLooper(file_sound, stop_event, self._stream_audio, loop=loop)
        self.active_audio[id(file_sound)] = looper
    
    def stop(self, file_sound=None):
        if file_sound:
            file_sound_id = id(file_sound)
            if file_sound_id in self.active_audio:
                self.active_audio[file_sound_id].stop()
                del self.active_audio[file_sound_id]
        else:
            for looper in self.active_audio.values():
                looper.stop()
            self.active_audio.clear()

def load_audio(mp3_path):
    _ray_init_thread.join()
    return zhmiscellany.processing.synchronous_class_multiprocess(AudioPlayer, mp3_path)

def time_func(func, loop=10000, *args, **kwargs):
    func_name = getattr(func, '__name__', repr(func))
    frame = inspect.currentframe().f_back
    lineno = frame.f_lineno
    start = time.time()
    for _ in range(loop):
        func(*args, **kwargs)
    elapsed = time.time() - start
    quick_print(f'{loop:,}x {func_name} took {elapsed}', lineno)
    return elapsed



_timings = defaultdict(list)
_block_timings = defaultdict(float)
_current_context = None
_line_start_time = None
_stack = []
_ignore_line = {'frame = inspect.currentframe().f_back', 'filename = frame.f_code.co_filename', 'if _current_context is None:', 'sys.settrace(None)'}

def time_code(label=None):
    global _current_context, _timings, _line_start_time, _block_timings, _stack, _ignore_line
    
    # Get the frame of the caller
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    
    if _current_context is None:
        # First call - start timing
        _current_context = label or f"timing_{len(_timings)}"
        quick_print(f"⏱️ Starting timing for context: {_current_context}")
        _line_start_time = time.time()
        _block_timings.clear()
        _stack = []
        
        # Define the trace function
        def trace_function(frame, event, arg):
            global _line_start_time, _stack
            
            # Track function calls and returns
            if event == 'call':
                func_name = frame.f_code.co_name
                if func_name != 'time_code':
                    _stack.append((func_name, time.time()))
                return trace_function
            
            elif event == 'return':
                if _stack:
                    func_name, start_time = _stack.pop()
                    elapsed = time.time() - start_time
                    _block_timings[f"Function: {func_name}"] += elapsed
                return None
            
            elif event == 'line':
                # Get current line information
                lineno = frame.f_lineno
                line_content = linecache.getline(frame.f_code.co_filename, lineno).strip()
                
                # Skip empty lines or comments
                if not line_content or line_content.startswith('#'):
                    return trace_function
                
                # Check if we should stop tracing
                if "time_code" in line_content and _current_context is not None:
                    # This might be the ending call, let's continue execution
                    return trace_function
                
                # Record elapsed time since last line
                current_time = time.time()
                if _line_start_time is not None:
                    elapsed = current_time - _line_start_time
                    _timings[_current_context].append((lineno, line_content, elapsed))
                    
                    # Track loop timings
                    if re.match(r'\s*(for|while)\s+', line_content):
                        loop_id = f"Loop at line {lineno}: {line_content[:40]}{'...' if len(line_content) > 40 else ''}"
                        _block_timings[loop_id] += elapsed
                
                # Set new start time for next line
                _line_start_time = current_time
            
            return trace_function
        
        # Start tracing
        sys.settrace(trace_function)
    
    else:
        sys.settrace(None)
        context = _current_context
        _current_context = None
        _line_start_time = None
        
        if not _timings[context]:
            quick_print(f"No timing data collected for context: {context}")
            return
        
        sorted_timings = sorted(_timings[context], key=lambda x: x[2], reverse=True)
        
        quick_print(f"\n⏱️ Detailed timing results for context: {context}")
        quick_print("-" * 80)
        quick_print(f"{'Line':>6} | {'Time':>12} | Code")
        quick_print("-" * 80)
        
        for lineno, line_content, elapsed in sorted_timings:
            if line_content not in _ignore_line:
                quick_print(f"{lineno:6d} | {elapsed:12.6f} | {line_content}")
        
        quick_print("-" * 80)
        total_time = sum(elapsed for _, _, elapsed in _timings[context])
        quick_print(f"Total execution time: {total_time * 1000:.6f} ms")
        
        if _block_timings:
            quick_print("\n📊 Summary of function and loop execution times:")
            quick_print("-" * 80)
            quick_print(f"{'Block Type':^40} | {'Time':>12} | {'% of Total':>10}")
            quick_print("-" * 80)
            
            # Sort block timings by time
            sorted_blocks = sorted(_block_timings.items(), key=lambda x: x[1], reverse=True)
            
            for block, elapsed in sorted_blocks:
                percentage = (elapsed / total_time) * 100 if total_time > 0 else 0
                quick_print(f"{block[:40]:40} | {elapsed:12.6f} | {percentage:10.2f}%")
            
            quick_print("-" * 80)
        
        # Clear the timing data for this context
        del _timings[context]
        _block_timings.clear()

class k:
    pass

current_module = sys.modules[__name__]
for name, func in inspect.getmembers(current_module, inspect.isfunction):
    if not name.startswith('_'):
        setattr(k, name, func)

if '__main__' in sys.modules:
    sys.modules['__main__'].__dict__['k'] = k
