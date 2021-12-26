![# En-Passant](https://github.com/leftgoes/En-Passant/blob/main/figures/logo.png)
- En-Passant
- Format
- Data
  - Jan 2013 - Dec 2018
  - Color palette
- games.py
- gif.py
- Old code
- Some Games

![](https://github.com/leftgoes/En-Passant/blob/main/figures/logo.gif)
- get all games (*my estimate from most common to least common*) on [lichess.org](https://lichess.org/) with

  0. *king* the king delivering checkmate
  1. *qbishop* underpromoting to a bishop with mate
  2. *qknight* underpromoting to a knight with mate
  3. *kcastle* kingside castling with mate
  4. *qcastle* queenside castling with mate
  5. *enpassant* en passant mate
    
- all pgn files from [lichess database](https://database.lichess.org/)
- *until 2016:* under [En-Passant/data](https://github.com/leftgoes/En-Passant/tree/main/data) in .csv format
- *all data:* uploaded to [Google Drive](https://drive.google.com/drive/folders/1CwcH0tKB3Gq-M4ZNeDIyZ1CfaqueTHOo?usp=sharing) due to large files

## Format
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

## Data
### Jan 2013 - Dec 2018
**Rating probability distribution**

![](https://github.com/leftgoes/En-Passant/blob/main/figures/2013-1-2019-1.gif?raw=true)

**Number of games**

![](https://github.com/leftgoes/En-Passant/blob/main/figures/2013-1-2019-1-s.png?raw=true)

**Number of games per month**

![](https://github.com/leftgoes/En-Passant/blob/main/figures/2013-1-2019-1-g.png?raw=true)

**Number of games per month per million**

![](https://github.com/leftgoes/En-Passant/blob/main/figures/2013-1-2019-1-gpm.png?raw=true)

### Color palette
The colors were chosen such that their inverse would be similar to the default lichess board colors (*this is just because matplotlib draws a white background as default but I want it to be black*)

<p align="center"><img src="https://github.com/leftgoes/En-Passant/blob/main/figures/colors.png" /></p>

#0f264a, #13283a, #4a8a9c, #184144, #359a9a, #006060

#f0d9b5, #b58863, #b57563, #b5534b, #ca6565, #ff9f9f

## games.py
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

## gif.py
This code was used to make rapid screenshots of the [lichess board](https://lichess.org/analysis). Those screenshots were then converted to a GIF with [GIMP](https://www.gimp.org/).
- **test:** show a screenshot of *region*
- **gif:** save screenshots to *folder*

## Old code
[This](https://github.com/leftgoes/En-Passant/tree/main/old) is (*in my opinion more ugly*) code without OOP from July 2021. There I had only implemented en passant mates. I searched for all en passant mates until 28.02.2018

## Some Games

![](https://github.com/leftgoes/En-Passant/blob/main/games/yTHX1AmK.gif?raw=true)
https://lichess.org/yTHX1AmK

![](https://github.com/leftgoes/En-Passant/blob/main/games/C56jMMwJ.gif?raw=true)
https://lichess.org/C56jMMwJ

![](https://github.com/leftgoes/En-Passant/blob/main/games/IsQiLytk.gif?raw=true)
https://lichess.org/IsQiLytk

![](https://github.com/leftgoes/En-Passant/blob/main/games/qt0fCmCF.gif?raw=true)
https://lichess.org/qt0fCmCF

![](https://github.com/leftgoes/En-Passant/blob/main/games/J7hU9ZhQ.gif?raw=true)
https://lichess.org/J7hU9ZhQ

![](https://github.com/leftgoes/En-Passant/blob/main/games/713ynukD.gif?raw=true)
https://lichess.org/713ynukD

![](https://github.com/leftgoes/En-Passant/blob/main/games/n1sYKpUy.gif?raw=true)
https://lichess.org/n1sYKpUy

![](https://github.com/leftgoes/En-Passant/blob/main/games/BQZgi3HO.gif?raw=true)
https://lichess.org/BQZgi3HO

![](https://github.com/leftgoes/En-Passant/blob/main/games/15yWW38A.gif?raw=true)
https://lichess.org/15yWW38A

![](https://github.com/leftgoes/En-Passant/blob/main/games/MQu042Yx.gif?raw=true)
https://lichess.org/MQu042Yx

![](https://github.com/leftgoes/En-Passant/blob/main/games/zC0viWG7.gif?raw=true)
https://lichess.org/zC0viWG7
