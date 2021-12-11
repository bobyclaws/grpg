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


class Kaeya(GrpgCharacter):

    def __init__(self, level=1):

        self.name = "Kaeya"
        # inherent parameters, not tweakable.
        inherent = {
            "Element": "Cryo",
            "Level": level,
            "Stats": {
                "Base HP": {
                    1: 976,
                    20: 2506,
                    20.5: 3235,
                    40: 4846,
                    40.5: 5364,
                    50: 6170,
                    50.5: 6860,
                    60: 7666,
                    60.5: 8184,
                    70: 8989,
                    70.5: 9507,
                    80: 10312,
                    80.5: 10830,
                    90: 11636
                },
                "Base ATK": {
                    1: 19,
                    20: 48,
                    20.5: 62,
                    40: 93,
                    40.5: 103,
                    50: 118,
                    50.5: 131,
                    60: 147,
                    60.5: 157,
                    70: 172,
                    70.5: 182,
                    80: 198,
                    80.5: 208,
                    90: 223
                },
                "Base DEF": {
                    1: 66,
                    20: 171,
                    20.5: 220,
                    40: 330,
                    40.5: 365,
                    50: 420,
                    50.5: 467,
                    60: 522,
                    60.5: 557,
                    70: 612,
                    70.5: 647,
                    80: 702,
                    80.5: 737,
                    90: 792
                },
                "Energy Recharge": {
                    1: 0,
                    20: 0,
                    20.5: 0,
                    40: 0,
                    40.5: 6.7,
                    50: 6.7,
                    50.5: 13.3,
                    60: 13.3,
                    60.5: 13.3,
                    70: 13.3,
                    70.5: 20,
                    80: 20,
                    80.5: 26.7,
                    90: 26.7
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
                    "DMG": {
                        1: [
                            53.75,
                            51.69,
                            65.27,
                            70.86,
                            88.24
                        ],
                        2: [
                            58.13,
                            55.89,
                            70.59,
                            76.63,
                            95.42
                        ],
                        3: [
                            62.5,
                            60.1,
                            75.9,
                            82.4,
                            102.6
                        ],
                        4: [
                            68.75,
                            66.11,
                            83.49,
                            90.64,
                            112.86
                        ],
                        5: [
                            73.13,
                            70.32,
                            88.8,
                            96.41,
                            120.04
                        ],
                        6: [
                            78.13,
                            75.13,
                            94.88,
                            103,
                            128.25
                        ],
                        7: [
                            85,
                            81.74,
                            103.22,
                            112.06,
                            139.54
                        ],
                        8: [
                            91.88,
                            88.35,
                            111.57,
                            121.13,
                            150.82
                        ],
                        9: [
                            98.75,
                            94.96,
                            119.92,
                            130.19,
                            162.11
                        ],
                        10: [
                            106.25,
                            102.17,
                            129.03,
                            140.08,
                            174.42
                        ],
                        11: [
                            114.84,
                            110.43,
                            139.47,
                            151.41,
                            188.53
                        ],
                        12: [
                            124.95,
                            120.15,
                            151.74,
                            164.73,
                            205.12
                        ],
                        13: [
                            135.06,
                            129.87,
                            164.01,
                            178.06,
                            221.71
                        ],
                        14: [
                            145.16,
                            139.59,
                            176.29,
                            191.38,
                            238.3
                        ]

                    },
                    "Level": 10
                },
                "charge": {
                    "DMG": {
                        1: [55.04, 73.1],
                        2: [59.52, 79.05],
                        3: [64, 85],
                        4: [70.4, 93.5],
                        5: [74.88, 99.45],
                        6: [80, 106.25],
                        7: [87.04, 115.6],
                        8: [94.08, 124.95],
                        9: [101.12, 134.3],
                        10: [108.8, 144.5],
                        11: [117.6, 156.19],
                        12: [127.95, 169.93],
                        13: [138.3, 183.68],
                        14: [148.65, 197.42]
                    },
                    "Level": 10,
                    "Stamina Cost": {
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
                "plunge": {
                    "DMG": {
                        1: 63.93,
                        2: 69.14,
                        3: 74.34,
                        4: 81.77,
                        5: 86.98,
                        6: 92.93,
                        7: 101.1,
                        8: 109.28,
                        9: 117.46,
                        10: 126.38,
                        11: 135.3,
                        12: 144.22,
                        13: 153.14,
                        14: 162.06
                    },
                    "Level": 10
                },
                "skill": {
                    "Skill DMG": {
                        1: 191.2,
                        2: 205.54,
                        3: 219.88,
                        4: 239,
                        5: 253.34,
                        6: 267.68,
                        7: 286.8,
                        8: 305.92,
                        9: 325.04,
                        10: 344.16,
                        11: 363.28,
                        12: 382.4,
                        13: 406.3,
                        14: 430.2
                    },
                    "CD": {
                        1: 6,
                        2: 6,
                        3: 6,
                        4: 6,
                        5: 6,
                        6: 6,
                        7: 6,
                        8: 6,
                        9: 6,
                        10: 6,
                        11: 6,
                        12: 6,
                        13: 6,
                        14: 6
                    },
                    "Level": 10
                },
                "burst": {
                    "Skill DMG": {
                        1: 77.6,
                        2: 83.42,
                        3: 89.24,
                        4: 97,
                        5: 102.82,
                        6: 108.64,
                        7: 116.4,
                        8: 124.16,
                        9: 131.92,
                        10: 139.68,
                        11: 147.44,
                        12: 155.2,
                        13: 164.9,
                        14: 174.6
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
                    "Duration": {
                        1: 8,
                        2: 8,
                        3: 8,
                        4: 8,
                        5: 8,
                        6: 8,
                        7: 8,
                        8: 8,
                        9: 8,
                        10: 8,
                        11: 8,
                        12: 8,
                        13: 8,
                        14: 8
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
                    },
                    "Level": 10
                }
            }
        }

        super().__init__(inherent)
