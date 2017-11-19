# Gym Melee
Gym melee is a tool that helps melee players improve their playing based upon the analysis of their games.

## Installation (only linux)
Install this version of dolphin: https://github.com/altf4/dolphin/tree/memorywatcher-rebased, checkout to branch memorywatcher-rebased, compile and install, then create a soft link of the dolphin/installation/path/Build/Binaries directory to $HOME/.local/share/dolphin-emu since libmeele expects the binaries to be there. Make sure the command dolphin-emu is available and if not link the dolphin executable to /usr/local/bin/dolphin-emu.
Place a copy of a Super Smash Bros. Melee v1.02 NTSC iso in the gym_melee directory and name it 'Super Smash Bros. Melee (v1.02).iso'.
The program only works inside Tec de Monterrey Campus Guadalajara, or you can all MongoClient references in the code to your own running mongodb instance.

## Asumptions
- No items.
- A stock should not last more than _ minutes.
- No pauses if possible.
- Only 1V1.
- The first player must be a real player.
- The second player can be a real player or a bot.

## Use
To start the game run the main.py script, the default behaviour is to use a gamecube controller adapter in the first port, a random policy bot using fox in the second port, in the battlefield stage and profile names of Jorge and Carlos. The game will automatically select the bot's character and the stage (if the bot is playing). to tweak this behaviour you can use these flags:

- '--port':
  + The controller port the second player will play on.
  + Default to 2.
- '--opponent':
  + The controller port the first player will play on.
  + Default to 1.
- '--controller':
  + The controller type of the first player, options are gcna, ps4, xbox and unplugged
  + Default to 'gcna'.
- '--aicontroller':
  + The controller type of the second player. options are gcna, ps4, xbox, bot and unplugged
  + Default to 'bot'.
- '--debug':
  + Activate debug mode.
- '--character':
  + The bot selected character.
  + Default to 'fox'.
- '--stage':
  + The bot selected stage.
  + Default to 'battlefield'.
- '--p1name':
  + Profile name for player one
  + Default to 'Jorge'
- '--p2name'
  + Profile name for player two.
  + Default to 'Carlos'
