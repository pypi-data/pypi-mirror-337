from enum import Enum


class QuestionCategories(Enum):
    GENERAL_KNOWLEDGE = 9
    ENTERTAINMENT_BOOKS = 10
    ENTERTAINMENT_FILM = 11
    ENTERTAINMENT_MUSIC = 12
    ENTERTAINMENT_MUSICALS_THEATRES = 13
    ENTERTAINMENT_TELEVISION = 14
    ENTERTAINMENT_VIDEO_GAMES = 15
    ENTERTAINMENT_BOARD_GAMES = 16
    SCIENCE_NATURE = 17
    SCIENCE_COMPUTERS = 18
    SCIENCE_MATHEMATICS = 19
    MYTHOLOGY = 20
    SPORTS = 21
    GEOGRAPHY = 22
    HISTORY = 23
    POLITICS = 24
    ART = 25
    CELEBRITIES = 26
    ANIMALS = 27
    VEHICLES = 28
    ENTERTAINMENT_COMICS = 29
    SCIENCE_GADGETS = 30
    ENTERTAINMENT_JAPANESE_ANIME_MANGA = 31
    ENTERTAINMENT_CARTOON_ANIMATIONS = 32


class QuestionDifficulties(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionTypes(Enum):
    MULTIPLE = "multiple"
    BOOLEAN = "boolean"
    ANY = "any"


class QuestionEncodings(Enum):
    DEFAULT = "default"
    URL3986 = "url3986"
    BASE64 = "base64"


class ResponseCodes(Enum):
    SUCCESS = 0
    NO_RESULTS = 1
    INVALID_PARAMETER = 2
    TOKEN_NOT_FOUND = 3
    TOKEN_EMPTY = 4
    TOKEN_INVALID = 5
