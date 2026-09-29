### Generating Refresh Token:

1. Fill in CLIENT_ID
   https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://127.0.0.1:5000/spotify_callback&scope=playlist-read-private%20playlist-read-collaborative%20playlist-modify-public%20playlist-modify-private%20user-read-currently-playing%20user-read-playback-state%20user-modify-playback-state

Scope:
| Scope | What it unlocks |
|---|---|
| `playlist-read-private` | View your private playlists |
| `playlist-read-collaborative` | View collaborative playlists |
| `playlist-modify-public` | Edit/add to your public playlists |
| `playlist-modify-private` | Edit/add to your private playlists |
| `user-read-currently-playing` | See what track is currently playing |
| `user-read-playback-state` | See playback details (device, progress, shuffle/repeat state, etc.) |
| `user-modify-playback-state` | Control playback — play/pause, skip, change what's playing (track, album, artist, playlist), seek, volume |

2. Paste above URL in browser and authorize

3. Copy code part from URL but everything before the &

4. Run the following:
   curl.exe -X POST https://accounts.spotify.com/api/token -d grant_type=authorization_code -d code=THE_CODE -d redirect_uri=http://127.0.0.1:5000/spotify_callback -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET

5. Save refresh token
