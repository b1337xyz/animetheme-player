#!/usr/bin/env python3
from optparse import OptionParser
import requests
import subprocess as sp


UA = "Mozilla/5.0 (compatible; MSIE 8.0; Windows 98; Win 9x 4.90; Trident/4.0)"
MAL = 'https://myanimelist.net/search/prefix.json?type=anime&keyword={}&v=1'
API = 'https://api.animethemes.moe/anime?include=animesynonyms,series,animethemes,animethemes.animethemeentries.videos,animethemes.song,animethemes.song.artists,studios,images,resources&fields%5Banime%5D=id,name,slug,year&filter%5Bhas%5D=resources&filter%5Bsite%5D=myanimelist&filter%5Bexternal_id%5D={}'  # noqa: E501
FZF_OPTS = [
    '-m',
    '--height', '20%',
    '--bind', 'ctrl-a:select-all'
]


def fzf(args: list) -> str:
    try:
        proc = sp.Popen(
            ['fzf'] + FZF_OPTS,
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            universal_newlines=True
        )
        out = proc.communicate('\n'.join(args))
        if proc.returncode != 0:
            return None
        return [i for i in out[0].split('\n') if i]
    except KeyboardInterrupt:
        pass


def parse_arguments():
    parser = OptionParser()
    parser.add_option('--no-video', action='store_true')
    return parser.parse_args()


def play(pl, o):
    # TODO:
    #   - add support to other players
    #   - add support to mpv ipc

    opts = [f'--playlist={pl}']
    if o.no_video:
        opts += ['--no-video']
    sp.run(['mpv'] + opts)


def main():
    opts, args = parse_arguments()

    if args:
        animetitle = ' '.join(args)
    else:
        animetitle = input("Give an anime title: ").strip()

    while True:
        themetype = input("Opening or Ending [OP/ED]: ").strip().upper()
        if themetype in ['OP', 'ED']:
            break
        print('Invalid option')

    data = requests.get(MAL.format(animetitle)).json()
    animeinfo = data['categories'][0]['items']
    animes = {
        f"{gotanimeid['name']}": str(gotanimeid["id"])
        for gotanimeid in animeinfo
        if gotanimeid.get("payload", {}).get('media_type') in ["TV", "OVA"]
    }
    selectedtitle = fzf(animes)
    try:
        selectedid = animes[selectedtitle[0]]
    except KeyError:
        print("Invalid selection.")
        return

    r = requests.get(API.format(selectedid), headers={'user-agent': UA})
    if r.status_code != 200:
        print(f"Error occurred: {r.status_code} {r.text}")
        return

    data = r.json()
    if not data["anime"]:
        print("Not found, probably not added yet!")
        return

    animethemes = data["anime"][0]["animethemes"]
    available_themes = dict()
    for theme in animethemes:
        if theme['type'] != themetype:
            continue
        title = theme['song']['title']
        available_themes[title] = []
        for entry in theme['animethemeentries']:
            for video in entry['videos']:
                available_themes[title].append(video['link'])

    videos = []
    for title in fzf(available_themes.keys()):
        videos += available_themes[title]

    if videos:
        playlist = '/tmp/animethemes.links'
        open(playlist, 'w').write('\n'.join(videos))
        play(playlist, opts)


if __name__ == "__main__":
    main()
