# OBS Audio Mixer Sync

### *Drive two OBS Audio mixers from one instance.*

# Overview
For my personal setup, sometimes I use only my main PC, sometimes I use my second PC as an encode machine. To maintain flexibility with using multiple audio tracks on both setups, I send all of my audio sources via NDI from the Main PC to the Encode PC with identical audio track settings. I wrote this script so that my stream deck buttons will work in either configuration
# Prerequisites
- Python 3.11 or higher
- Two OBS Instances
  - identically named audio sources
  - websocket server enabled

# Setup

1. Clone the repo 
    ``` 
    git clone https://github.com/JackOsterman/OBS-Audio-Mixer-Sync.git
    cd OBS-Audio-Mixer-Sync
    ```
2. Install requirements
    ```
    pip install -r requirements.txt
    ```
3. Create `config.toml`, either by creating the file yourself or renaming `config-template.toml`. Add your configuration based on `Tools > WebSocket Server Settings > Show Connect Info`
   ```
   # OBS Instance that will send and drive the volume mixer for both instances
    [primary]
    host = "0.0.0.0" # Local IP Address of Primary OBS Instance
    port = 4455 # Local Port of  Primary OBS Instance
    password = "password" # OBS Websocket Password of Primary OBS Instance

    # OBS Instance that will receive and follow the volume mixer
    [secondary]
    host = "0.0.0.0" # Local IP Address of Secondary OBS Instance
    port = 4455 # Local Port of Secondary OBS Instance
    password = "password" # OBS Websocket Password of Secondary OBS Instance
    ```
4. Ensure Audio Sources are named ***identically*** in both OBS Instances
5. Run the script
   ```
   py obs-audio-mixer-sync.py
   ```