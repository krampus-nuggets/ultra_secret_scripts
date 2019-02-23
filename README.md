# NoRecoil script
#### [UnKnoWnCheaTs] 
Original UnKnoWnCheaTs forum thread is [here](https://www.unknowncheats.me/forum/apex-legends/322650-python-norecoil-script-configs-game-apex.html)

#### [STATUS] 
<span style="color:green">Undetected</span> so far...

#### [IMPORTANT NOTES]
- Game **should be played in "Borderless" mode**.  
- Current Apex Legends config is working with **1920x1080 resolution only**. 
- For other resolutions you may create and share your own configs. How to do it read below.

#### [CONTENTS OF ARCHIVE]
`requirements.txt` - list of required python libs (use Python3 pls).  
`very_secret_script.py` - main script  
`pattern_generator.py` - script that helps you to get correct recoil configs  
`overlay_label.py` - just a class to draw overlay label  
`image_search.py` - just some funcs to work with images (detect current weapons)  
`keyboard_input.py` - this one I downloaded from web (simple methods didn't work)  
`weapon_data/` - here you should store configs as `GAMENAME.json` files and images inside `GAMENAME_img/` dir.  

#### [INSTALLATION]
All you need for this script is Python3 with libs listed in `requirements.txt`.  
- Download and install Python3 from official site (use Google, pls).  
- Then install `pip` for python3 (Google again).  
- And then from `cmd` you can run command: `pip install <lib_name>`  
Run this for each lib listed in `requirements.txt`  

#### [RUN SCRIPT]
To run this script you should use `cmd` command.  
`python ./very_secret_script.py CONFIG`  
Where CONFIG is the name of config (without .json) stored in `weapon_data/` dir  
As example for running NoRecoil script for Apex Legends use:  
`python ./very_secret_script.py apex`  

#### [KEYBINDINGS]
**F4** - Trun on/off NoRecoil  
**F10** - Stop script  
**NUM_4** - Previous weapon  
**NUM_6** - Next weapon  

For Apex Legends I gathered wapons images so my script will autodetect what weapon you're using ath the moment (only when NoRecoil is On). No need to manually switch it with NUM_4 and NUM_6.  
It works **ONLY in borderless 1920x1080**.

#### [CONFIGS]
You can create your own configs for different games and my script should work well with them. Just use same format of .json file to store your config.  
**.json config formatting:**
```json
{
  "weapons": [
    {
      "name": "WeaponNameToDisplay",
      "rpm": 6000,
      "check_image": "weapon_image.png",
      "check_area": [0, 0, 1920, 1080],
      "pattern": [
        [0, 0],
        [0, -5]
      ]
    }
  ]
}
```
So it's basically a dictionary with a list of weapons under a key "weapons".  
Each weapon in list should have keys:  
`"name"` - string with weapon name.  
`"rpm"` - RPM (rounds per minute) weapon stat. Can be googled or found on wiki of almost any game.  
`"check_image"` - filename of image to check. File must be placed in `"./weapon_data/CONFIG_img/"` directory. Can be set to **null** if you have no images or just don't know/want to check. Then use manual weapon switching.  
`"check_area"` - area on the screen where script should look for `check_image`. List of `[x1, y1, x2, y2]`.  
`"pattern"` - List with weapon recoil pattern. Each item in this list is `[dx, dy]`. It's differences in `x` and `y` from previous shot. Can be gathered with method described below.  
**NOTE:** if you will use `image_search` for detecting current weapon try to use as small images as possible and as small areas as possible (like I do in Apex Legends config). Large images/areas may do *weapon_detector* run slowly.  

#### [RECOIL PATTERN GENERATOR]
Also for easier config making I wrote a small script that will help you to gather recoil patterns. This script have some description in it but I will share my method of gathering recoil patterns.
- Go to Training Mode.
- Pick weapon you want to get recoil pattern.
- Stand in front of clear wall. Bullet-prints must have nice visibility.
- Shot out whole magazine without moving your mouse to get recoil image on the wall.
- Do PrintScreen and paste it to Paint.
- Run my script `pattern_generator.py`
- Back to Paint: Zoom image to 200% and press F4 to activate pattern_generator script.
- Now click each bulletprint one by one from first to last. You should hear "beep" sound each time you click.
- When you finished -> press F10 to stop script.
- Done! Now you can find recoil pattern in `tracked_pattern.txt` inside folder near the script. It is compatible with .json config format.

#### [APEX LEGENDS CONFIG]
I wrote a sample config for Apex Legends.  
It contains all weapons data and weapons images (for weapon autodetect). But I'm too lazy guy so I've filled recoil patterns only for light-ammo automatic weapons:  
**Alternator,**  
**R-99,**  
**R-301,**  
**RE-45**.  
You can fill other weapons *recoil_patterns* by yourself using method I described above.  
Also recoil_patterns I gathered may be a little bit not accurate (was too tired to snipe small pixels on my screen) so you can share your *recoil_patterns* with community in [this thread](https://www.unknowncheats.me/forum/apex-legends/322650-python-norecoil-script-configs-game-apex.html).  

#### [Meh?!]
I will be glad to hear any suggestions how I can improve this script!  
Also you can try to build your configs for other games (or recoil_patterns for Apex Legends weapons) and share 'em in [this thread](https://www.unknowncheats.me/forum/apex-legends/322650-python-norecoil-script-configs-game-apex.html) or with pull requests.  

#### Thanks for reading!
