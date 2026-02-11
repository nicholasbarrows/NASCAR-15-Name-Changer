# NASCAR 15 Name Changer Tool

## Features

* Changing names of all 46 playable drivers in NASCAR '15

## Usage

* When launching the program, it will prompt you to choose the `ARCHIVE0.AR` file from your NASCAR '15 installation
* Navigate to your NASCAR '15 install (for most, it will be at `C:/Program Files (x86)/Steam/steamapps/common/NASCAR 15`)
* Navigate into the `data` folder and select the file named `ARCHIVE0.AR`
* You should now see a list of all 46 drivers in the game, a textbox next to them, and a number on the far right. The number represents the amount of space you have left in your input
* Note that leaving the input blank will retain the driver's original name
* Due to the way the game stores strings containing the driver names, by default, the chosen custom names are limited to be less than or equal to the length of the original driver's name. However, there is the option to go beyond this limit and overwrite data in certain cases.
* Disabling `Safe Mode` will allow you to overwrite data that is mostly unused in cases where drivers have space after their name. While I haven't thoroughly tested it, none of the issues I've found are anything game breaking. But, if you want to be extra cautious, leave Safe Mode on.
* Refer to the next section for more information about Safe Mode and character limit behavior
* After setting your names, click the `Patch Game with New Names` button. Give it a few seconds and you should see a message saying `Game patched successfully!`.
* Next time you load the game, you should see the new names you set

Tip: I would recommend replacing `J.J. Yeley` with `JJ Yeley`. That will stop his full name from showing up on his driver tag and on the leaderboard.

## Safe Mode

As mentioned before, when `Safe Mode` is turned on, the input for the names is limited to the length of the original driver's name. However, disabling Safe Mode allows you to overwrite extra data when available. This data is mostly unused (the exceptions are mentioned below), and any issues _should_ be visual.

### Unchanged Limits

The following drivers have the same character limit regardless of if safe mode is turned on or not. In other words, these drivers will always be limited to the length of their original name. This is due to the string of another driver being directly after them.

| Driver                   | Character Limit
| -----------------------  |:-------------:|
| Jamie McMurray           | 14            |
| Brad Keselowski          | 15            |
| Kevin Harvick*           | 13            |
| Kasey Kahne              | 11            |
| Denny Hamlin             | 12            |
| Casey Mears              | 11            |
| Ricky Stenhouse Jr.      | 19            |
| Matt Kenseth             | 12            |
| Joey Logano              | 11            |
| Ty Dillon                | 9             |
| David Gilliland          | 15            |
| Kurt Busch               | 10            |
| AJ Allmendinger          | 15            |
| Michael Waltrip          | 15            |
| Martin Truex Jr.         | 16            |
| Dale Earnhardt Jr.       | 18            |

\*Kevin Harvick is a special case. When disabling `Safe Mode`, a new option, labelled `Overwrite Sam Hornish Jr's name` will become available. Sam Hornish's name directly follows Kevin Harvick, which means if Harvick's name extends past its boundary, Sam Hornish's name will be overwritten. Since Hornish never appears as an AI driver in this game, I implemented the ability to overwrite his name, if you so desire. By enabling the `Overwrite Sam Hornish Jr's name` option, Harvick's character limit will be increased at the cost of overwriting Hornish's name. The only time this would be noticeable is on the driver selection screen or if you choose to play as Hornish.

### Increased Limits

#### Known Issues

Some drivers have known issues if you disable safe mode. None of these issues are game-breaking, but are worth mentioning. I put them in order from most to least noticeable. I will update this list if I find more.



| Driver          | Normal Limit | Limit with Safe Mode Off | Issues After x Characters | Issue                                                                                                                                                              |
|-----------------|--------------|--------------------------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ryan Blaney     | 11           | 31                       | 11                        | Going beyond 11 characters will overwrite the team name for HScott Motorsports, which is shown in the race results and season standings pages                      |
| Jeb Burton      | 10           | 31                       | 24                        | Going beyond 24 will overwrite the team name for Go Green Racing                                                                                                   |
| Michael Annett  | 14           | 31                       | 29                        | Going beyond 29 will overwrite the explanation for the "Brake Indicator" assist in the assist menu                                                                 |
| Kyle Larson     | 11           | 31                       | 11                        | Going beyond 11 will overwrite the names of the "Window" and "Side" camera labels, which show up when viewing replays                                              |
| Justin Allgaier | 15           | 31                       | 28                        | Going beyond 28 will overwrite a string containing the word "Engine". I have no idea if this string is even used anywhere, so this one might not even be an issue. Unrelated, but Justin Allgaier is canonically trans in NASCAR '15. The variable determining if a driver is male was mistakenly entered as `false` for Allgaier.  |

#### No Known Issues

Here's a full list of the increased character limits if you disable safe mode. The only known issue with any of these is it can sometimes mess with the track stats on the loading screen, but that's so minor I didn't feel the need to include it as an actual issue. The reason you'll see a lot of 31's on this table is because the max length of a string is 31, the game will truncate it if it goes beyond 31. Not every driver has enough excess data after them to get all the way to 31 characters though. I also included the data that is overwritten when using the full extra space for those curious. I'm not even 100% sure why some of this is even here to begin with. There are several names that are not only not in this game, but not in _any_ Eutechnyx game (some haven't even been in any official NASCAR game at all).

| Driver            | Normal Limit | Limit with Safe Mode Off | Overwritten Data                                                                                                                                                           |
|-------------------|--------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Austin Dillon     | 13           | 29                       | A string containing the name `Brendan Gaughan`                                                                                                                             |
| Kevin Harvick     | 13           | 13/31                    | See above note, there is an option to overwrite Sam Hornish Jr's name. Hylton's name is also overwritten by Harvick if that option is used                                 |
| Trevor Bayne      | 12           | 31                       | Believe it or not, the data directly after Bayne's name is trivia about his 2009 Nationwide Season (left over from NASCAR 2011)                                            |
| Bubba Wallace Jr. | 17           | 31                       | His hometown and a message about reconnecting controllers                                                                                                                  |
| Regan Smith       | 11           | 25                       | A string containing the name `Reed Sorenson`                                                                                                                               |
| Sam Hornish Jr.   | 15           | 28/0                     | A string containing the name `James Hylton`                                                                                                                                |
| Danica Patrick    | 14           | 31                       | Her hometown and a string containing the name `Peter Sospenzo`                                                                                                             |
| Tony Stewart      | 12           | 26                       | A string containing the name `David Stremme`                                                                                                                               |
| Clint Bowyer      | 12           | 31                       | Strings containing the names `Jeff Burton` and `Trevor Boys`                                                                                                               |
| Greg Biffle       | 11           | 23                       | A string containing the name `Dave Blaney`                                                                                                                                 |
| Kyle Busch        | 10           | 31                       | Strings containing the names `Patrick Carpentier`, `Ted Christopher`, and `Derrike Cope`                                                                                   |
| Carl Edwards      | 12           | 31                       | Strings containing the names `Bill Elliott` and `Mike Garvey`                                                                                                              |
| Erik Jones        | 12           | 19                       | The word `Michigan`. As far as I can tell, this is just for it being his home state and nothing important                                                                  |
| J.J. Yeley        | 10           | 31                       | A string containing `Richard Perry Motorsports`. Considering this string has a typo, I assume it's not used                                                                |
| Jeff Gordon       | 11           | 24                       | A string containing the name `Robby Gordon`                                                                                                                                |
| Chase Elliott     | 13           | 31                       | The name `Paulie Harraka`, Harraka's hometown `Wayne, NJ`, and Harraka's made up team in NASCAR '14, `PH LLC`                                                              |
| Paul Menard       | 11           | 31                       | Strings containing the names `Juan Pablo Montoya` and `Joe Nemechek`                                                                                                       |
| Ryan Newman       | 11           | 21                       | A string containing the name `Max Papis`                                                                                                                                   |
| Bobby Labonte     | 13           | 31                       | Strings containing the names `Carl Long`, `Mark Martin`, and `Eric McClure`                                                                                                |
| David Ragan       | 11           | 31                       | Strings containing the names `Tony Raines`, `David Reutimann`, `Elliott Sadler`, and `Boris Said`                                                                          |
| Cole Whitt        | 10           | 31                       | Strings containing the names `Landon Cassill`, `Ken Schrader`, `Tim Andrews`, and `Kenny Wallace`                                                                          |
| Aric Almirola     | 13           | 31                       | Strings containing the names `Marcos Ambrose`, `John Andretti`, `Brandon Ash`, `Dexter Bean`, and `Norm Benning`                                                           |
| Jimmie Johnson    | 14           | 25                       | A string containing the name `P.J. Jones`                                                                                                                                  |
| Brian Vickers     | 13           | 26                       | A string containing the name `Mike Wallace`                                                                                                                                |
| Michael McDowell  | 16           | 31                       | Strings containing the names `Scott Speed` and `Scott Wimmer`                                                                                                              |
| Josh Wise         | 9            | 31                       | Strings containing `Brian Johnson`, `Doug Richert`, and `Kevin Harvick Inc.`. Like Bayne and Danica, pretty clear leftovers from NASCAR 2011 (first game they appeared in) |


## Uninstall

Note that even if you re-patch the game with the default names, the ARCHIVE0.AR file will still not be 1:1 to the default file. It shouldn't really matter, but, if you want to restore your file to the vanilla version, simply validate your game files on Steam.

## Third-Party Tools

This project includes QuickBMS, developed by Luigi Auriemma. Furthermore, a script for QuickBMS, also written by Luigi Auriemma, is included as well. This project would definitely not have been possible without QuickBMS, so a big thank you to them.

QuickBMS is licensed under the GNU General Public License v2.0 (GPL-2.0)

Source code for QuickBMS is available at: https://github.com/LittleBigBug/QuickBMS

## Screenshots
![Image](https://github.com/user-attachments/assets/086a0640-e2f7-4d74-8a66-c4ffb481781a)
![Image](https://github.com/user-attachments/assets/6b063aec-7377-4f73-9e3c-cdcf10e5fc4c)
