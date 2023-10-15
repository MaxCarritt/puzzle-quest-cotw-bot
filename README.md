# pquestbot

a bot to play Puzzle Quest - Challenge of the Warlords for the Nintendo DS

<iframe width="560" height="315"
src="https://youtu.be/kb556f0fcpg" 
frameborder="0" 
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen></iframe>

[![Watch the video](https://img.youtube.com/vi/kb556f0fcpg/maxresdefault.jpg)](https://youtu.be/kb556f0fcpg)
https://www.youtube.com/watch?v=kb556f0fcpg

Any emulator should theoretically work,but I'm using DeSmuMe on Windows 11. The current implementation for clicking requires this running on Windows.


*Needed Improvements:*
- Move Optimization:
    - Better skull move optimization, determine if the future game grid results in a series of skulls and prioritize that one. Currently it just picks a skull to be moved over everything else, but this might just mean its lining up other gems by moving a skull
    - Detection of wild gems and logic to detect a series with a wild gem
    - Determine why sometimes it thinks no moves are available
- Game State:
    - Detect if the game board has settled. Currently just waiting arbitrarily some time between moves.
- Use of spells

