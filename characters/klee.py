import logging
import random
import os
import json

from ..talent_impl import auto

from ..compute import E
from ..event import Event

from ..clock import clock

from ..util import get_opponent
from ..GrpgCharacter import GrpgCharacter


class Klee(GrpgCharacter):

    def __init__(self, level=1):

        self.name = "Klee"
        # inherent parameters, not tweakable.

        inherent = {
            "Level": level,
            "Stats": {
                "Base HP": {
                    1: 801,
                    20: 2077,
                    20.5: 2764,
                    40: 4136,
                    40.5: 4623,
                    50: 5319,
                    50.5: 5970,
                    60: 6673,
                    60.5: 7161,
                    70: 7870,
                    70.5: 8358,
                    80: 9076,
                    80.5: 9563,
                    90: 10287
                },
                "Base ATK": {
                    1: 24,
                    20: 63,
                    20.5: 84,
                    40: 125,
                    40.5: 140,
                    50: 161,
                    50.5: 180,
                    60: 202,
                    60.5: 216,
                    70: 238,
                    70.5: 253,
                    80: 274,
                    80.5: 289,
                    90: 311
                },
                "Base DEF": {
                    1: 48,
                    20: 124,
                    20.5: 165,
                    40: 247,
                    40.5: 276,
                    50: 318,
                    50.5: 357,
                    60: 399,
                    60.5: 428,
                    70: 470,
                    70.5: 500,
                    80: 542,
                    80.5: 572,
                    90: 615
                },
                "Pyro DMG Bonus": {
                    1: 0,
                    20: 0,
                    20.5: 0,
                    40: 0,
                    40.5: 7.2,
                    50: 7.2,
                    50.5: 14.4,
                    60: 14.4,
                    60.5: 14.4,
                    70: 14.4,
                    70.5: 21.6,
                    80: 21.6,
                    80.5: 28.8,
                    90: 28.8
                },
                "Crit Rate": {
                    1: 5,
                    20: 5,
                    20.5: 5,
                    40: 5,
                    40.5: 5,
                    50: 5,
                    50.5: 5,
                    60: 5,
                    60.5: 5,
                    70: 5,
                    70.5: 5,
                    80: 5,
                    80.5: 5,
                    90: 5
                },
                "Crit DMG": {
                    1: 50,
                    20: 50,
                    40: 50,
                    50: 50,
                    60: 50,
                    70: 50,
                    80: 50,
                    90: 50
                }
            },
            "Talents": {
                "auto": {
                    "Level": 10,
                    "DMG": {
                        1: [
                            72.16,
                            62.4,
                            89.92
                        ],
                        2: [
                            77.57,
                            67.08,
                            96.66
                        ],
                        3: [
                            82.98,
                            71.76,
                            103.41
                        ],
                        4: [
                            90.2,
                            78,
                            112.4
                        ],
                        5: [
                            95.61,
                            82.68,
                            119.14
                        ],
                        6: [
                            101.02,
                            87.36,
                            125.89
                        ],
                        7: [
                            108.24,
                            93.6,
                            134.88
                        ],
                        8: [
                            115.46,
                            99.84,
                            143.87
                        ],
                        9: [
                            122.67,
                            106.08,
                            152.86
                        ],
                        10: [
                            129.89,
                            112.32,
                            161.86
                        ],
                        11: [
                            137.39,
                            118.81,
                            171.21
                        ],
                        12: [
                            147.21,
                            127.3,
                            183.44
                        ],
                        13: [
                            157.02,
                            135.78,
                            195.67
                        ],
                        14: [
                            166.83,
                            144.27,
                            207.9
                        ]
                    }
                },
                "charge": {
                    "Level": 10,
                    "DMG": {
                        1: [157.36],
                        2: [169.16],
                        3: [180.96],
                        4: [196.7],
                        5: [208.5],
                        6: [220.3],
                        7: [236.04],
                        8: [251.78],
                        9: [267.51],
                        10: [283.25],
                        11: [299.61],
                        12: [321.01],
                        13: [342.42],
                        14: [363.82]
                    },
                    "Stamina Cost": {
                        1: 50,
                        2: 50,
                        3: 50,
                        4: 50,
                        5: 50,
                        6: 50,
                        7: 50,
                        8: 50,
                        9: 50,
                        10: 50,
                        11: 50,
                        12: 50,
                        13: 50,
                        14: 50
                    }
                },
                "plunge": {
                    "Level": 10,
                    "DMG": {
                        1: 56.83,
                        2: 61.45,
                        3: 66.08,
                        4: 72.69,
                        5: 77.31,
                        6: 82.6,
                        7: 89.87,
                        8: 97.14,
                        9: 104.41,
                        10: 112.34,
                        11: 120.27,
                        12: 128.2,
                        13: 136.12,
                        14: 144.05
                    }
                },
                "skill": {
                    "Level": 10,
                    "Jumpy Dumpty DMG": {
                        1: 95.2,
                        2: 102.34,
                        3: 109.48,
                        4: 119,
                        5: 126.14,
                        6: 133.28,
                        7: 142.8,
                        8: 152.32,
                        9: 161.84,
                        10: 171.36,
                        11: 180.88,
                        12: 190.4,
                        13: 202.3,
                        14: 214.2
                    },
                    "Mine DMG": {
                        1: 32.8,
                        2: 35.26,
                        3: 37.72,
                        4: 41,
                        5: 43.46,
                        6: 45.92,
                        7: 49.2,
                        8: 52.48,
                        9: 55.76,
                        10: 59.04,
                        11: 62.32,
                        12: 65.6,
                        13: 69.7,
                        14: 73.8
                    },
                    "Mine Duration": {
                        1: 15,
                        2: 15,
                        3: 15,
                        4: 15,
                        5: 15,
                        6: 15,
                        7: 15,
                        8: 15,
                        9: 15,
                        10: 15,
                        11: 15,
                        12: 15,
                        13: 15,
                        14: 15
                    },
                    "CD": {
                        1: 20,
                        2: 20,
                        3: 20,
                        4: 20,
                        5: 20,
                        6: 20,
                        7: 20,
                        8: 20,
                        9: 20,
                        10: 20,
                        11: 20,
                        12: 20,
                        13: 20,
                        14: 20
                    }
                },
                "burst": {
                    "Level": 10,
                    "Sparks 'n' Splash DMG": {
                        1: 42.64,
                        2: 45.84,
                        3: 49.04,
                        4: 53.3,
                        5: 56.5,
                        6: 59.7,
                        7: 63.96,
                        8: 68.22,
                        9: 72.49,
                        10: 76.75,
                        11: 81.02,
                        12: 85.28,
                        13: 90.61,
                        14: 95.94
                    },
                    "Duration": {
                        1: 10,
                        2: 10,
                        3: 10,
                        4: 10,
                        5: 10,
                        6: 10,
                        7: 10,
                        8: 10,
                        9: 10,
                        10: 10,
                        11: 10,
                        12: 10,
                        13: 10,
                        14: 10
                    },
                    "CD": {
                        1: 15,
                        2: 15,
                        3: 15,
                        4: 15,
                        5: 15,
                        6: 15,
                        7: 15,
                        8: 15,
                        9: 15,
                        10: 15,
                        11: 15,
                        12: 15,
                        13: 15,
                        14: 15
                    },
                    "Energy Cost": {
                        1: 60,
                        2: 60,
                        3: 60,
                        4: 60,
                        5: 60,
                        6: 60,
                        7: 60,
                        8: 60,
                        9: 60,
                        10: 60,
                        11: 60,
                        12: 60,
                        13: 60,
                        14: 60
                    }
                }
            }
        }

        super().__init__(inherent)

