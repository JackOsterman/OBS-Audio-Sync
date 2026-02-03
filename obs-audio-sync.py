import time
import threading
from obswebsocket import obsws, requests, events, exceptions
import tomllib

class OBSAudioSync:
    def __init__(self, primary_config, secondary_config, retry_interval=5):
        self.primary_config = primary_config
        self.secondary_config = secondary_config
        self.retry_interval = retry_interval

        self.primary_ws = None
        self.secondary_ws = None

        self.running = True

    def connect_obs(self):
        """Attempts to connect to both OBS instances."""
        while self.running:
            try:
                print("Connecting to primary OBS...")
                self.primary_ws = obsws(**self.primary_config)
                self.primary_ws.connect()
                print("Connected to primary OBS.")

                print("Connecting to secondary OBS...")
                self.secondary_ws = obsws(**self.secondary_config)
                self.secondary_ws.connect()
                print("Connected to secondary OBS.")

                # Register event handlers
                self.primary_ws.register(self.on_volume_changed, events.InputVolumeChanged)
                self.primary_ws.register(self.on_mute_state_changed, events.InputMuteStateChanged)
                return

            except exceptions.OBSSDKError as e:
                print(f"[Connection Error] {e}. Retrying in {self.retry_interval} seconds...")
                self.disconnect()
                time.sleep(self.retry_interval)

    def on_volume_changed(self, event):
        primary_name = event.getInputName()
        volume = event.getInputVolumeMul()
        print(f"[Volume Changed] {primary_name}: {volume}")
        self._safe_call_secondary(requests.SetInputVolume(inputName=primary_name, inputVolumeMul=volume))

    def on_mute_state_changed(self, event):
        primary_name = event.getInputName()
        muted = event.getInputMuted()
        print(f"[Mute Changed] {primary_name}: {'Muted' if muted else 'Unmuted'}")
        request = requests.SetInputMute(inputName=primary_name, inputMuted=muted)
        self._safe_call_secondary(request)

    def _safe_call_secondary(self, request_obj):
        """Wrap calls to secondary OBS in try/except to avoid crash on failure."""
        try:
            self.secondary_ws.call(request_obj)
        except Exception as e:
            print(f"[Secondary Call Failed] {e}")

    def run(self):
        self.connect_obs()

        while self.running:
            try:
                time.sleep(1)
                # keep-alive check or logic could go here
            except (KeyboardInterrupt, SystemExit):
                print("Stopping...")
                self.running = False
                self.disconnect()

    def disconnect(self):
        try:
            if self.primary_ws and self.primary_ws.connected:
                self.primary_ws.disconnect()
        except Exception:
            pass

        try:
            if self.secondary_ws and self.secondary_ws.connected:
                self.secondary_ws.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    print("Initializing...")

    with open("config.toml","rb") as f:
        data = tomllib.load(f)

    sync = OBSAudioSync(data["primary"], data["secondary"])
    sync.run()
