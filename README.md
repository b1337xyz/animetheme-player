## Introduction

This is a Python script that lets you search for an anime and play its opening or ending theme songs using the mpv media player. The script uses the AnimeThemes API to get the available theme songs and the fzf to prompt the user for selections.

## Requirements

- Python 3.x
- requests module (can be installed via pip)
- mpv media player (must be installed separately)
- install fzf as well (depending on your OS)

## Usage

```
git clone https://github.com/b1337xyz/animetheme-player.git
python3 animetheme.py
```

## Limitations

- The script only searches for TV and OVA anime titles.
- The script only supports playing opening and ending theme songs.
- The script only plays one theme song at a time.
- The script requires an active internet connection to function properly.

## Credits

- AnimeThemes for providing the API used by the script.
- The creators and contributors of the requests and mpv modules used by the script.
