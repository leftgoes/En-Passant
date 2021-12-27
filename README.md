![](figures/logo.png)

- En-Passant
- Format
- Data
  - Jan 2013 - Dec 2018
  - Color palette
- games.py
- gif.py
- Old code
- Some Games

# En-Passant
![](figures/logo.gif)
- get all games (*my estimate from most common to least common*) on [lichess.org](https://lichess.org/) with

  0. *king* the king delivering checkmate
  1. *qbishop* underpromoting to a bishop with mate
  2. *qknight* underpromoting to a knight with mate
  3. *kcastle* kingside castling with mate
  4. *qcastle* queenside castling with mate
  5. *enpassant* en passant mate
    
- all pgn files from [lichess database](https://database.lichess.org/)
- *until 2016:* under [En-Passant/data](data) in .csv format
- *all data:* uploaded to [Google Drive](https://drive.google.com/drive/folders/1CwcH0tKB3Gq-M4ZNeDIyZ1CfaqueTHOo?usp=sharing)

# Format
The data is written to a .csv file seperated by ,'s.

- **number:** type of checkmate delivered
  - 0: *king*
  - 1: *qbishop*
  - 2: *qknight*
  - 3: *kcastle*
  - 4: *qcastle*
  - 5: *enpassant*
- **path:** append to 'https://lichess.org/' to get full url
- **date:** UTC date of the game
- **time:** UTC time of the game
- **white**
- **black**
- **white elo**
- **black elo**
- **time control**
- **event:** type of the game
- **moves:** moves in pgn format (some with clock or evaluation data)
## Example
0,csrzdu82,2013.01.01,20:23:57,Trebizonde,FF4,1715,1508,300+10,Rated Classical game,1. e4 b6 2. d4 ...

- *0*: the king delivering checkmate
- *url*: https://lichess.org/csrzdu82
- *played (UTC)*: 2013.01.01 20:23:57
- *white:* Trebizonde, 1715
- *black:* FF4, 1508
- *time control:* 300+10 or 5+10
- *event:* Rated Classical game
- *moves:* 1. e4 b6 2. d4 ...

# Data
## Jan 2013 - Dec 2018
**Rating probability distribution**

![](figures/2013-1-2019-1.gif?raw=true)

**Number of games**

![](figures/2013-1-2019-1-s.png?raw=true)

**Number of games per month**

![](figures/2013-1-2019-1-g.png?raw=true)

**Number of games per month per million**

![](figures/2013-1-2019-1-gpm.png?raw=true)

## Color palette
The colors are based on the [lichess chessboard](https://lichess.org/analysis).

<p align="center"><img src="figures/colors.png" /></p>

#f0d9b5, #b58863, #b57563, #b5534b, #ca6565, #ff9f9f

# games.py
All of the code I used to make the diagrams is here. Parts of it are quite messy though and I'll have to clean them up in the future.
- **read:**
    - **read_games:** read the .csv file
    - **read_log:** read the log file
- **p_ratings:** probablity distribution in time interval
    - **_fit:** fit data with a gaussian
- **games_t:** number of games over time (relative or absolute)
- **games_sum:** sum of games over time
- **ratings_sum_t:** sum of rating every year over time (figures get saved in *folder* as .png files)
- **_from_year:** → **_from_interval:** get the relevant data from time interval
- **_from_input:** str, int, range, list are converted to list

# gif.py
This code was used to make rapid screenshots of the [lichess board](https://lichess.org/analysis). Those screenshots were then converted to a GIF with [GIMP](https://www.gimp.org/) for [some games](README.md#some-games).
- **test:** show a screenshot of *region*
- **gif:** save screenshots to *folder*

# Old code
[This](old) is code without OOP from July 2021. There I had only implemented en passant mates. I searched for all en passant mates until 28.02.2018

# Some Games

![](games/yTHX1AmK.gif?raw=true)
https://lichess.org/yTHX1AmK

![](games/C56jMMwJ.gif?raw=true)
https://lichess.org/C56jMMwJ

![](games/IsQiLytk.gif?raw=true)
https://lichess.org/IsQiLytk

![](games/qt0fCmCF.gif?raw=true)
https://lichess.org/qt0fCmCF

![](games/J7hU9ZhQ.gif?raw=true)
https://lichess.org/J7hU9ZhQ

![](games/713ynukD.gif?raw=true)
https://lichess.org/713ynukD

![](games/n1sYKpUy.gif?raw=true)
https://lichess.org/n1sYKpUy

![](games/BQZgi3HO.gif?raw=true)
https://lichess.org/BQZgi3HO

![](games/15yWW38A.gif?raw=true)
https://lichess.org/15yWW38A

![](games/MQu042Yx.gif?raw=true)
https://lichess.org/MQu042Yx

![](games/zC0viWG7.gif?raw=true)
https://lichess.org/zC0viWG7
