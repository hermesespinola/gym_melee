# Gym Melee
Gym melee is a tool that helps melee players improve their playing based upon the analysis of their games.

## Installation (linux only)
- Clone this version of dolphin from @altf4: https://github.com/altf4/dolphin/tree/memorywatcher-rebased. 
- Checkout to branch *memorywatcher-rebased*.
- Compile and install, following the instructions in the emulator's repository.
- Create a soft link of the dolphin/installation/path/Build/Binaries directory to *$HOME/.local/share/dolphin-emu* since the *libmeele* library expects the binaries to be there.
- Make sure the command dolphin-emu is available and if not link the dolphin executable to /usr/local/bin/dolphin-emu.
- Place a copy of a Super Smash Bros. Melee v1.02 NTSC iso in the *gym_melee* directory and name it 'Super Smash Bros. Melee (v1.02).iso'.
The program only works inside Tec de Monterrey Campus Guadalajara (plss don't mess with the db thnxs), or you can replace all MongoClient references in the code (in main.py, usersgraph.py and userstats.py) to your own running mongodb instance.

## Asumptions
- No items.
- A stock should not last more than _ minutes.
- No pauses if possible.
- Only 1V1.
- The first player must be a real player.
- The second player can be a real player or a bot.

## Use
### Play the game
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
  
Example of usage:
```bash
python3 main.py --opponent 3 --port 1 --controller gcna --aicontroller ps4 --p1name Zegerd --p2name Azen
```
The above would run smash assuming the first player will play on port 3 with a gamecube controller, the second player on port 1 with a ps4 controller and there is no bot, so the character and stage flags are ignored. The first player will have a profile with the name Zegerd and the second player the name Azen.

### analyze data
Run the userstats.py script (it may take a while) followed with the name of the user you want to analyze, this should be runned if there are new games for that user. For example:
```bash
python3 userstats.py Jorge
```

### Show results
Run the usergraph.py script followed with the name of the user you want to plot. For example:
```bash
python3 usergraph.py Jorge
```

This will produce graphs for different playing variables of that user, namely, offensive, defensive, combos and spamming. The y axis are the earned points and the x axis are all the stocks you've played in chronological order.
