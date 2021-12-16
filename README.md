# En-Passant
- get all games (*my estimate from most common to least common*) on [lichess.org](https://lichess.org/) with

  0. the king delivering checkmate
  1. underpromoting to a bishop with mate
  2. underpromoting to a knight with mate
  3. kingside castling with mate
  4. queenside castling with mate
  5. en passant mate
    
- all pgn files from https://database.lichess.org/
- *until 2016:* under [En-Passant/data](https://github.com/leftgoes/En-Passant/tree/main/data) in .csv format
- *2017 and after:* uploaded to Google Drive due to large file size

## Data
**Number of games between Jan 2013 and Jan 2018**
![](https://github.com/leftgoes/En-Passant/blob/main/figures/2013-1-2018-1.png?raw=true)

**Colors**
The colors were chosen such that their inverse would be similar to the lichess color palette (*this is just because matplotlib draws a white background as default but I want it to be black*)
![](https://github.com/leftgoes/En-Passant/blob/main/figures/colors.png?raw=true)

#0f264a, #13283a, #4a8a9c, #184144, #359a9a, #006060

#f0d9b5, #b58863, #b57563, #b5534b, #ca6565, #ff9f9f

## Format
The data is written to a .csv file seperated by ,'s.

- **number:** type of checkmate delivered
  - 0: *king*
  - 1: *qbishop*
  - 2: *qknight*
  - 3: *kcastle*
  - 4: *qcastle*
  - 5: *enpassant*
- **path:** append to 'https://lichess.org/' to get the link of the game
- **date:** UTC date of the game
- **time:** UTC time of the game
- **white**
- **black**
- **white elo**
- **black elo**
- **time control**
- **event**
- **moves:** moves in pgn format (some with clock or evaluation data)

## Old code
[This](https://github.com/leftgoes/En-Passant/tree/main/old) is (*in my opinion more ugly*) code without OOP from July 2021. There I had only implemented en passant mates. I searched for all en passant mates until 28.02.2018

## Example Games

![](https://github.com/leftgoes/En-Passant/blob/main/games/qt0fCmCF.gif?raw=true)
https://lichess.org/qt0fCmCF

![](https://github.com/leftgoes/En-Passant/blob/main/games/n1sYKpUy.gif?raw=true)
https://lichess.org/n1sYKpUy

![](https://github.com/leftgoes/En-Passant/blob/main/games/BQZgi3HO.gif?raw=true)
https://lichess.org/BQZgi3HO

![](https://github.com/leftgoes/En-Passant/blob/main/games/C56jMMwJ.gif?raw=true)
https://lichess.org/C56jMMwJ

![](https://github.com/leftgoes/En-Passant/blob/main/games/IsQiLytk.gif?raw=true)
https://lichess.org/IsQiLytk

![](https://github.com/leftgoes/En-Passant/blob/main/games/15yWW38A.gif?raw=true)
https://lichess.org/15yWW38A

![](https://github.com/leftgoes/En-Passant/blob/main/games/MQu042Yx.gif?raw=true)
https://lichess.org/MQu042Yx

![](https://github.com/leftgoes/En-Passant/blob/main/games/zC0viWG7.gif?raw=true)
https://lichess.org/zC0viWG7
