"""
Ayman Momin
UCID: 30192494
Assignment 3
CPSC 441
"""

import socket
import threading
import random
from datetime import datetime
import re

# Panda-themed data
PANDA_EMOJIS = ["🐼", "🎍", "🎋", "🌿", "🍃"]
PANDA_FACTS = [
    "Pandas spend around 14 hours a day eating bamboo! 🌱",
    "Baby pandas are born pink and weigh only about 100 grams! 🍼",
    "A group of pandas is called an embarrassment! 😳",
    "Pandas have a 'thumb' (actually an extended wrist bone) to grip bamboo! 👍",
    "Newborn pandas are 1/900th the size of their mothers—smaller than a stick of butter! 🧈",
    "Pandas can poop up to **40 times a day** because bamboo is low in nutrients! 💩",
    "They have vertical slit pupils (like cats!) for better night vision! 😼",
    "Pandas are solitary animals and mark territory with scent glands! 👃",
    "Wild pandas live about 20 years, but in captivity, they live up to 30! 🎂",
    "Pandas don’t hibernate—they migrate to warmer areas instead! 🌞",
    "Their black-and-white fur helps them blend into snowy mountains and dark forests! ❄️🌲",
    "Pandas can climb trees as early as 6 months old! 🌳",
    "Despite eating bamboo, their digestive system is designed for meat! 🥩 (They just prefer bamboo!)",
    "Pandas can swim and use it to escape predators! 🏊",
]

## taken from https://emojicombos.com/panda
PANDA_ASCII = {
    "hey": r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠉⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠛⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣷⣶⣤⣙⠻⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⢃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡙⠉⠉⠉⠙⠻⣿
⣿⣿⣿⣿⣿⣿⣿⡟⢠⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠙
⣿⡿⠿⠿⢿⣿⣿⢀⣿⣿⡿⠋⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⢠
⡿⠀⠀⠀⠀⠙⠻⢸⣷⣴⡇⠀⠀⠐⠃⣰⣿⣿⣿⣿⣿⡿⠏⠙⠻⣿⣿⣿⣿⡆⢀⣴⣿
⣷⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⠦⣤⣤⣾⣿⣿⠙⠛⢿⣿⠁⢠⠀⠀⠈⣿⣿⣿⡇⣽⣿⣿
⣿⣆⠀⠀⠀⠀⠀⠀⠘⢿⣶⣾⣿⣿⣿⣄⠛⠀⠶⠖⣿⣆⠈⠀⠀⢀⣿⣿⣿⠃⣿⣿⣿
⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣷⣶⣾⣿⣿⡗⢶⣶⣿⡇⣿⠃⣼⣿⣿⣿
⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣮⣹⣿⠟⢁⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣦⢠⣤⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠀⠰⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡇⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⣷⣦⣤⣶⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢨⣭⣉⣛⣛⠉⠉⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣦⣀⣀⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
""",
    "sleeping": r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⡿⣿⠟⢿⡯⣿⢫⡗⣴⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣶⣾⣦⣾⣷⣿⣶⣷⣾⠿⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣄⣠⠤⠴⠞⠓⠶⠤⣶⣶⣶⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡻⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀
⠀⠀⢠⣾⣿⣶⡤⢴⠁⠀⠀⣠⣴⣶⣦⣄⠀⠀⠀⢠⣾⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠘⣿⠋⠁⠀⣿⠀⠀⢸⣿⣿⣟⣻⣿⠇⠀⠀⠘⢿⣯⣽⣿⣆⠀⠀⠀
⠀⠀⢰⠃⠀⠀⠀⢹⠀⠀⠀⠻⠿⠿⠿⠋⠀⠀⠻⠛⠀⠉⠉⠁⣸⠀⠀⠀
⣤⣶⣼⡀⠀⠀⠀⣼⣿⣷⣶⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⠀⣀⣴⣧⡀⠀⠀
⠻⠿⠿⠷⠤⠤⠤⠿⠿⠿⠿⠿⠿⠿⠿⣇⠤⠤⠤⠴⠶⠿⠿⠿⠿⠁⠀⠀
""",
    "thanks": r"""
⣿⣿⣿⢿⣿⣿⠿⣿⡿⠻⣿⠻⣿⡟⡿⣿⠟⢿⡿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿
⣏⣅⢠⣾⠀⠛⠀⡟⠀⠂⠙⢠⠘⠁⡇⡀⢴⣿⣷⡈⢋⡴⢡⣦⠈⠁⣿⠉⣿
⣿⣿⠘⣿⣀⣿⣄⣀⣿⣿⣀⣸⣧⣰⣠⣿⣄⣹⣿⣇⣸⣷⡘⠛⣠⠘⠟⣠⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⢛⣉⣭⣭⣭⣭⣍⣉⠛⢋⣥⣤⣉⠻⣿⣿⠡⡬⢹⣿
⣿⣿⣿⠿⠿⡿⢋⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣤⡟⢩⣍⢿⡆⢻⣿⣷⣶⣿⣿
⣿⡟⢡⣾⠟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣭⣿⠇⣼⢟⣟⠛⣛⠻
⣿⣇⠹⡟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⠀⣿⡸⣿⣿⡌⢃
⣿⣿⣦⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⣮⣭⣵⣿
⣿⣿⣿⢸⣿⡿⠿⣿⣿⡿⢿⣿⣇⠀⠈⣿⣿⣿⣿⣿⣿⣿⡇⣸⡰⠴⣹⣿⣿
⣿⣿⣿⠀⣿⣯⡤⣬⡟⠇⠹⢛⣿⣷⢺⣿⣷⣝⣿⡿⣿⣿⠁⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠈⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣜⣿⢿⣻⠇⢶⣌⢥⠘⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣷⣌⠙⣁⡤⡙⢿⣿⣿⣿⣿⣿⣿⡟⢡⣶⣿⣿⡇⢰⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⢰⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣇⠸⣿⣿⡿⢃⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡈⢿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣬⡅⠐⣿⣿⣿⣿⣿⣿⣿⣿
""",
    "shy": r"""
    ⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡤⠶⠶⠒⠒⠒⠒⢲⣴⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠘⠿⢿⣿⣿⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⣀⣀⠀⠀⠀⠀⢀⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀
⠀⠀⠀⢠⡾⠀⢀⣾⣿⣿⣷⠀⠀⢠⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀
⠀⠀⢀⠟⠀⠀⢸⣿⣿⣿⡿⠤⠤⠈⢿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀
⠀⠀⣿⠀⠀⠀⠀⠙⡟⠁⣶⣶⡆⠀⠈⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀
⠀⠀⠹⡄⠀⠀⠀⠀⡇⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣧⠀⠀⠀⠀
⠀⠀⠀⢹⡄⠀⠀⠀⠙⢦⠀⢠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣋⣿⣆⠀⠀⠀
⠀⠀⠀⣾⣿⢶⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣴⠾⣟⠛⢻⠿⡏⠁⢿⡀⠀⠀
⠀⠀⣾⣿⢿⣴⡄⢈⡙⠛⠛⠷⠶⠶⠶⠾⠿⠛⣛⣯⣥⣾⠿⠐⠀⠀⠁⡀⢹⣧⠀⠀
⠀⣸⣯⣿⣆⣸⣷⠈⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⣿⠁⠀⠀⠀⠀⠀⠀⣿⣿⡆⠀
⢰⣿⠀⣿⡼⡇⣿⣆⠁⠀⠀⠀⠀⠀⠀⠀⣠⡄⢀⣾⣇⠀⠀⠀⠀⠀⠀⢀⣿⣿⣷⠀
⢸⣿⠀⡟⢸⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠙⢂⣾⠏⠁⠆⠀⠀⠀⠀⠀⢘⣿⣿⠿⡄
⢸⣿⠀⡗⠀⠐⠀⣦⡿⣷⣤⣀⣀⣀⣀⣀⣠⣿⡃⠀⠀⠀⠀⠀⠀⠀⢡⣾⠋⠀⠀⣧
⠈⣿⡄⢷⣬⠀⠐⠃⡈⠿⣯⡉⠉⠉⠉⣽⣿⠟⠁⠀⠀⠀⠀⠀⠀⣀⣾⠋⠀⠀⠀⣿
⢠⡟⣿⡁⡿⠀⠀⠀⠀⠢⠜⢷⡄⣠⡾⣋⠁⠀⠀⠀⠀⠀⠀⢀⣶⠿⠁⠀⠀⠀⠀⣿
⢸⡇⠈⠻⣦⡀⠀⢀⣀⠰⣦⣌⣿⡟⢘⣿⠀⠀⠀⠀⢀⣠⡼⠟⠁⠀⠀⠀⠀⠀⢀⡟
⠀⢱⣀⠀⠈⠻⢦⣄⣐⣺⣷⣿⡟⠻⣿⣥⣤⣤⡶⠾⠛⠉⠀⠀⠀⠀⠀⠀⢀⣴⣿⠁
⠀⠀⢿⣷⣦⣄⣀⠈⠉⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣟⣻⡟⠀
⠀⠀⠈⢿⣷⣿⣟⠛⠶⠶⢶⣤⣤⣤⣤⣠⣤⣤⣤⣤⣤⣴⣶⡾⠛⣻⣿⣿⣿⡟⠁⠀
⠀⠀⠀⠈⠻⣿⡿⢸⣷⡄⣤⠀⠀⠁⠀⠀⠀⠈⢀⣀⣀⠀⡿⣫⢻⣿⠿⣷⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠙⢿⡀⢨⣄⡻⠀⠀⠀⠀⠈⡛⠀⠈⠉⣉⣀⠀⠀⠘⣿⣶⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣷⣀⡙⠻⠷⢶⣶⣶⣴⣿⣶⣶⠿⠟⠁⠀⠀⠀⣹⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⣇⠀⠀⠀⠀⠀⠀⣼⣇⠀⠀⠀⠀⠀⠀⠀⢀⣲⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣿⣇⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⣰⢿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣶⣦⣦⣤⣼⣭⣿⠀⢠⣅⣀⣂⣰⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣽⣯⣿⣿⠞⠛⠷⣶⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀
""",
"dab": r"""
⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠠⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡶⢧
⠀⠀⠀⠀⣀⠔⠉⠁⠀⠀⠀⠀⢀⣥⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⣠⣇⣸
⠀⠀⢀⠌⠀⠀⢠⠖⠀⠀⠀⠴⢿⣞⡻⣿⡇⠀⠀⠀⠀⠀⢀⣠⣴⡶⡟⣿⣿⠟
⠀⣠⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣇⣤⣴⠒⠚⡿⣧⣤⣬⣿⡿⠋⠁⠀
⣼⣿⡟⢿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢀⣿⣇⣹⣀⣶⣿⣿⡿⠋⠁⡂⠀⠀⢀
⠙⠿⠷⡟⠀⠀⠀⠀⠀⠀⢠⣾⣷⣶⣀⣼⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠇⠀⠀⠅
⠀⠀⠀⠘⢄⠀⣾⣿⡿⢀⣨⣽⠛⠉⣿⣿⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⡃
⠀⠀⠀⠀⢸⣿⠿⠿⠾⠿⠌⠀⣀⣿⠟⠁⠀⠉⡋⠱⡀⠀⠀⠀⠀⠀⡇⠀⡐⠀
⠀⠀⠀⠀⠈⢿⣀⣒⣀⣰⣴⡾⠟⠁⠀⠀⠀⠀⡘⡀⢰⠀⠀⠀⠀⠀⠀⠀⠂⠀
⠀⠀⠀⠀⠀⠀⡙⠓⠛⠛⠉⠀⠀⠀⠀⠀⠀⡇⠀⠃⡀⡆⠀⠀⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⠢⠀⣸⠀⠀⠄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢀⣼⣿⣧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠿⢻⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⡋⠀⠙⢶⣤⣤⣄⠤⠤⠤⢶⣯⣥⢄⠀⣾⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⠁⣀⣴⣿⠟⠉⠀⠀⠀⠀⠀⠈⠙⢿⣷⣿⢿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣤⢿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⠃⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣾⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣖⣶⣄⠀⠀⠀
⠀⠀⠘⠿⠿⠷⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⠿⠿⠿⠋⠀⠀⠀
""",
"swag": r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢨⣿⣿⣶⣮⡝⠋⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡿⢉⡝⣿⣿⣿⣿⣿⣿⣿⣿⣄⣴⣿⣿⣿⣿⣿⡀⠀⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣌⡢⡘⢿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⣿⣿
⣿⣿⣿⣿⠃⠻⣦⣻⣿⣿⣿⡿⣸⡟⢻⣿⣿⠻⢿⣿⣿⣿⠋⠻⣧⢿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢋⣉⡥⠔⠊⢉⣿⣿
⣿⣿⣿⣿⠇⠀⢺⠛⠿⣼⣿⣧⣿⡀⣸⣿⣇⠀⠀⢻⣿⣿⠀⠀⠈⠈⠻⣿⣿⣿⣿⠿⠇⠀⢿⣇⠀⠀⢀⣾⣿⣿⣿
⣿⣿⣿⣿⡆⣤⣾⠆⠀⠈⠙⠛⠉⢻⡿⠿⣿⣦⣴⣾⠟⠁⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⢠⡏⠀⣴⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡈⠁⠀⠀⠀⠀⠀⠀⠀⠳⠴⠿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠷⠐⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢀⣠⣀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣷⡀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠿⠟⠁⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⢀⣤⣭⣥⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
""",
"shocked": r"""
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠉⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡛⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⠀⢠⡄⠀⢠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣦⢄⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡹⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⣶⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢣⣾⣿⣿⣿⣿⣿⣿⣿⡟⠋⠀⠀⠈⠉⠉⠘⠻⣿⣿⣷⡹⣿⡿⠛⠛⠉⠉⠙⠿⣷⠹⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⡟⣻⡇⠀⣠⣶⣶⣶⣄⡀⠀⠀⠈⡛⢿⡇⠀⠆⣠⣤⣶⣶⣦⡀⢹⣧⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⠛⠀⠈⠁⠉⠡⠔⠮⢍⢳⣄⠀⠀⣸⡇⢠⡾⠟⠩⠭⠭⡙⠇⣸⣿⣇⢻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⢇⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣶⠋⠩⢳⠀⢹⣇⡜⣿⣇⢧⠀⠰⠊⠉⢳⡀⠀⠸⣿⣿⣦⠻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣄⠀⠑⠤⣄⡠⠜⠀⣾⣿⡟⠹⣿⡎⣧⠐⠤⢤⡼⠃⣴⡧⠙⣿⣿⣧⢹⣿⣿⣿⣿
⣿⣿⣿⣿⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⠙⠂⠀⠀⠀⠀⢀⣼⣿⠋⠁⢀⣽⣧⡹⣧⡀⠀⠠⠴⠛⡇⠀⢸⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⣛⣒⣒⣠⣴⣿⣿⢣⣾⡗⠛⠿⣿⣿⡎⣿⣦⣤⣀⣐⣁⣤⣿⣿⣿⣧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡇⠀⠉⠀⠀⠀⢈⠁⢀⣧⡹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⣿⠟⣋⣵⣿⣿⡿⠖⡀⣀⣠⣶⣹⣖⡙⢿⣿⣦⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣫⠁⣴⠿⠟⠉⠀⠈⠁⠂⠙⡆⣘⡻⣷⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡇⠘⠻⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⠋⣴⣿⣇⣸⣁⢀⡤⢤⣤⣤⣴⠶⣤⣄⢸⣿⣼⡞⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠇⠀⠀⠈⠙⠿⣿⣿⣿⣿⣏⠿⣿⡏⠀⠻⠍⢻⣿⣿⢷⠀⠀⠈⠉⠉⠉⣿⡿⣻⠯⢹⣿⣿⢿⡟⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠘⠛⠿⣿⣿⣷⣿⣿⡆⠀⠀⠀⢻⣦⣴⣶⣶⣿⡟⣻⣿⣿⣼⠋⢀⣾⣿⡷⠋⠀⠘⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢿⣿⣦⣀⠀⠀⠉⠋⠙⠛⠛⠀⠈⠙⠋⢁⣴⣿⠟⠋⢀⣠⣤⣷⡈⠻⣿⣿⣿⣿
⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠒⠠⠄⠀⠀⠀⠀⣠⡴⠾⠟⠋⠁⠀⢤⣼⣿⣿⣿⠛⡄⠙⣿⣿⣿
⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢻⣿⣿⠄⠀⠀⠀⠘⣿⣿
⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⣀⠀⠀⠀⠀⠙⠘⠿⣯⠀⠀⠀⠀⠀⢹⣿
⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣦⣯⣾⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣶⣦⣴⣤⡀⠀⠀⠀⠀⢿
""",
}

class PandaServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # List of (client_socket, username)
        self.lock = threading.Lock()
        self.master_log = "server_master.log"
        
        # Initialize master log
        with open(self.master_log, "a") as f:
            f.write(f"\n=== Server started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    def log_master(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            with open(self.master_log, "a", encoding="utf-8") as f:  # Add encoding="utf-8"
                f.write(f"[{timestamp}] {message}\n")

    def log_client(self, log_filename, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_filename, "a", encoding="utf-8") as f:  # Add encoding="utf-8"
            f.write(f"[{timestamp}] {message}\n")
            
    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server is listening on {self.host}:{self.port}...")
        while True:
            client_socket, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        username = client_socket.recv(1024).decode('utf-8')
        
        # Check if the username is already connected
        with self.lock:
            existing_users = [user[1] for user in self.clients]
            if username in existing_users:
                client_socket.send("❌ This panda name is already in the grove!".encode())
                client_socket.close()
                return  # Prevent duplicate connections
        
        # Create client-specific log
        safe_username = re.sub(r'[^a-zA-Z0-9]', '_', username)
        client_log = f"client_{safe_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        with self.lock:
            self.clients.append((client_socket, username, client_log))
        
        # Log connections
        self.log_master(f"{username} joined the chat")
        self.log_client(client_log, f"Connected to server as '{username}'")

        self.broadcast(f"{PANDA_EMOJIS[0]} {username} joined the grove!", exclude=client_socket)

        try:
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    # Log message/command
                    self.log_master(f"{username} sent: {message}")
                    self.log_client(client_log, f"You sent: {message}")

                    if message.startswith('@'):
                        # Pass client_log to handle_command
                        self.handle_command(client_socket, message, username, client_log)
                    else:
                        self.broadcast(f"{random.choice(PANDA_EMOJIS)} {username}: {message}")
                except OSError: # Catch socket closure errors
                    break
        except ConnectionResetError:
            pass # Already handled by OSError
        finally:
            self.remove_client(client_socket, username, client_log) # Ensure cleanup
    
    
    def handle_command(self, client_socket, command, username, client_log): 
        if command.startswith('@bonus'):
            parts = command.split(' ', 1)
            if len(parts) == 2:
                keyword = parts[1].lower()
                ascii_art = PANDA_ASCII.get(keyword)
                if ascii_art:
                    self.broadcast(f"{username}:\n{ascii_art}")
                    self.log_client(client_log, f"Shared ASCII art for '{keyword}'")
                else:
                    client_socket.send(f"🐼 No ASCII found for this mood! Try: {PANDA_ASCII.keys()}".encode())
                    self.log_client(client_log, f"Failed to find ASCII art for '{keyword}'")
            else:
                client_socket.send("❌ Usage: @bonus <key>".encode())
        elif command == '@bamboo':
            fact = random.choice(PANDA_FACTS)
            client_socket.send(f"📚 Panda Fact: {fact}".encode('utf-8'))
            self.log_client(client_log, f"Received panda fact: {fact}")
        elif command == '@grove':
            users = [user[1] for user in self.clients]
            client_socket.send(f"🌿 Connected Pandas: {', '.join(users)}".encode('utf-8'))
        elif command == '@leaves':
            # Notify client to close gracefully (DO NOT call remove_client here)
            client_socket.send("🍂 You have left the grove. Farewell!".encode('utf-8'))
        else:
            client_socket.send("❌ Invalid command!".encode('utf-8'))

    def remove_client(self, client_socket, username, client_log):
        with self.lock:
            self.clients = [c for c in self.clients if c[0] != client_socket]  # Compare socket
        client_socket.close()
        
        # Log disconnection
        self.log_master(f"{username} left the chat")
        self.log_client(client_log, "Disconnected from server")
        self.broadcast(f"🍂 {username} left the grove...")
        
    def broadcast(self, message, exclude=None):
        with self.lock:
            for entry in self.clients:  # Iterate over tuples with 3 elements
                client = entry[0]      # First element is client_socket
                username = entry[1]    # Second is username
                if client != exclude:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        continue

if __name__ == "__main__":
    server = PandaServer()
    server.start()