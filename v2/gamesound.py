"""Module: SnakeMusic."""

import vlc


class SnakeMusic:
    """Class for setting background music.

    Usage:

    >> tracks = [
        (1, "path/to/song_1.mp3"),
        ("two", "path/to/song_2.mpd")
    ]

    >> background_music = SnakeMusic(tracks)

    to play track:

    >> background_music.playtrack(1)
    >> background_music.playtrack("two")
    >> background_music.playtrack(tracks[0][0])

    to stop music:

    >> background_music.stoptrack()

    to add new track:

    >> background_music.addtrack((3, "path/to/song_3.mp3"))

    >> background_music.removetrack("two")

    """

    def __init__(self, tracks: list[tuple[int | str, str]]) -> None:
        """Initialze the SnakeMusic class.

        Raises:
            TypeError: if internal vlc functions fail

        """
        instance = vlc.Instance()
        if not isinstance(instance, vlc.Instance):
            raise TypeError("well, dont know how we fix this")
        self.instance = instance
        instance.log_unset()
        self.player = self.instance.media_list_player_new()
        self.tracks = {x[0]: self.instance.media_new(x[1]) for x in tracks}
        for x in self.tracks.values():
            x.parse_with_options(vlc.MediaParseFlag(0x0), 10)
        media_list = vlc.MediaList([x for x in self.tracks.values()])
        self.player.set_media_list(media_list)
        self.player.set_playback_mode(vlc.PlaybackMode(2))

    def playtrack(self, id: int | str) -> None:
        """Play a track from given id.

        Raises:
            ValueError: if  track is not found.

        """
        track = self.tracks.get(id)
        if track is None:
            raise ValueError("track not found")
        self.player.play_item(track)

    def stoptrack(self) -> None:
        """Stop currently playing track."""
        self.player.stop()

    def addtrack(self, track: tuple[str | int, str]) -> None:
        """Add track to internal list."""
        self.tracks[track[0]] = self.instance.media_new(track[1])
        media_list = vlc.MediaList([x for x in self.tracks.values()])
        self.player.set_media_list(media_list)

    def removetrack(self, track: str | int) -> None:
        """Remove track from internal list."""
        del self.tracks[track]
        media_list = vlc.MediaList([x for x in self.tracks.values()])
        self.player.set_media_list(media_list)

    @property
    def tracks(self) -> dict[str | int, vlc.Media]:
        """Internal dictionary of tracks to play from."""
        return self.__tracks

    @tracks.setter
    def tracks(self, tracks: dict[str | int, vlc.Media]) -> None:
        self.__tracks = tracks

    @property
    def instance(self) -> vlc.Instance:
        """Internal vlc instance."""
        return self.__instance

    @instance.setter
    def instance(self, instance: vlc.Instance) -> None:
        if not isinstance(instance, vlc.Instance):
            raise TypeError("well, dont know how we fix this")
        self.__instance = instance

    @property
    def player(self) -> vlc.MediaListPlayer:
        """Internal music player."""
        return self.__player

    @player.setter
    def player(self, player: vlc.MediaListPlayer) -> None:
        if not isinstance(player, vlc.MediaListPlayer):
            raise TypeError("wrong way go back")
        self.__player = player
