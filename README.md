# Online Music Tools

Various python scripts for interacting with Spotify. 
Uses [Spotipy](https://github.com/plamere/spotipy).

To use these scripts, you have to set your credentials for the Spotify API. 
Check out [Spotify for Developers](https://developer.spotify.com) to learn how to 
get your credentials. This projects uses the Authorization Code Flow, so you will 
need a **client id**, a **client secret** and a **redirect URI**. To set the credentials,
create a file named `.env` in your working directory, with the following content:

```.env
CLIENT_ID=<your_client_id>
CLIENT_SECRET=<your_client_secret>
REDIRECT_URI=<your_redirect_uri>
```

This project uses `python-dotenv` to read this file and set the environment variables
automatically (see `spotify.py`).

I am also supplying a `requirements.txt` file for use with `pip`, but I am using 
Anaconda, so it may not be up-to-date, and your mileage may vary. 
However, most of those packages are dependencies,
to see which packages you actually need to install, see the source code.
