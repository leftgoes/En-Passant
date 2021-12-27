from collections import Counter
import cv2
from datetime import datetime
from inspect import signature
from lmfit import Model, Parameter
import matplotlib.pyplot as plt
import numpy as np
import os

from input import COLORS, NUMBERS, PLT_STYLE


class Games:
    __slots__ = ('data', 'general')

    def __init__(self):
        self.data: list[list[datetime, ], ] = [[] for _ in range(6)]
        self.general: list[tuple[datetime, int, ]] = []

    @staticmethod
    def _from_input(inp) -> list[int,] or range:  # takes an input and returns a list of ints (indexes)/range
        if inp is None:
            return range(6)

        t = type(inp)
        if t is range:  # return inp immediately if inp is a range object
            return inp

        inp = list(inp) if t is list or t is set else [inp]  # if inp is an int or a str make inp a list with length 1
        return [NUMBERS.index(i) if type(i) is str else i for i in inp]  # if inp is a str return its index in NUMBERS

    @staticmethod
    def gaussian(x, sigma: float, mu: float):  # fitting function
        return np.exp(-(x - mu)**2/(2 * sigma**2))/(sigma * np.sqrt(2 * np.pi))

    @staticmethod
    def linmap(x: float, from_range: tuple[float, float], to_range: tuple[float, float]) -> float:  # map from one range to another
        return to_range[0] + (x - from_range[0]) * (to_range[1] - to_range[0]) / (from_range[1] - from_range[0])

    @staticmethod
    def str(x: int, n: int) -> str:  # convert an int to fixed length str
        x = str(x)
        return (n - len(x)) * '0' + x

    def _fit(self, x, y, mu: float) -> tuple[Parameter, Parameter]:
        args = signature(self.gaussian).parameters.keys()  # get arguments that gaussian takes
        model = Model(self.gaussian)  # use gaussian as fitting function
        result = model.fit(y, x=x, sigma=300, mu=mu)  # σ = 300 seems to be a good initial value
        return result.params['sigma'], result.params['mu']  # return σ and μ as Parameter objects

    def player_most(self, n: int = 1, inp=None) -> list[tuple[str, int], ]:  # the n most common players in self.data
        data = []
        for i in self._from_input(inp):
            for j in self.data[i]:
                for k in j[1]:
                    data.append(k)
        counter = Counter(data)
        return counter.most_common(n)

    def ratings(self, inp=None, start: datetime = None, end: datetime = None) -> list[int, ]:  # list of ints (ratings), use min() and max() to get minimum and maximum rating
        start = datetime(2000, 1, 1) if start is None else start
        end = datetime(3000, 1, 1) if end is None else end
        return [sum((j[2] for j in self.data[i] if start <= j[0] < end), []) for i in self._from_input(inp)]  # add up all the lists with ratings if between start and end

    def read(self, games_path: str, log_path: str) -> None:
        self.read_games(games_path)
        self.read_log(log_path)

    def read_games(self, path: str) -> None:  # read a .csv with the games
        with open(path, 'r') as f:
            lines = [line.split(',') for line in f.read().splitlines()]  # read into list of lists

        for line in lines[1:]:
            names = line[4:6]  # the name of black and white
            ratings = [int(rating) for rating in line[6:8] if rating != '?']  # the ratings of black and white
            i = int(line[0])  # type of checkmate
            self.data[i].append((datetime.strptime(line[2] + ' ' + line[3], "%Y.%m.%d %H:%M:%S"), names, ratings))  # append alongside with time played
        self.data.sort(key=lambda i: i[0])  # sort by time

    def read_log(self, path: str) -> None:  # read a .log
        with open(path, 'r') as f:
            lines = [line.split(',') for line in f.read().splitlines()]  # read into list of lists

        for line in lines[1:]:
            self.general.append(((datetime.strptime(line[1], '%Y-%m')), float(line[2])) + tuple(int(i) for i in line[3:]))  # datetime.strptime(line[1], '%Y-%m') doesn't strip 'datetime', but 'month' from the log file

    def p_ratings(self, start: datetime = None, end: datetime = None, inp=None, fit: bool = False, dots: bool = True, rating_interval: float = 20, llim: float = None, rlim: float = None, ylim: tuple[float, float] = None, show: bool = True) -> list[list[list[tuple, tuple], str, str]]:  # plots the amount of players over the rating (approximately normal distribution)
        plt.close()
        plt.style.use(PLT_STYLE)
        if ylim is not None:
            plt.ylim(*ylim)

        ratings = self.ratings(inp, datetime(2013, 1, 1) if start is None else start, datetime(2022, 1, 1) if end is None else end)

        plt.xlabel('rating')
        plt.ylabel('probability')
        plt.xlim(min(min(r) for r in ratings) - 100 if llim is None else llim, max(max(r) for r in ratings) + 100 if rlim is None else rlim)  # set x-boundaries

        data = [[[(None, None), (None, None)], NUMBERS[i], COLORS[i]] for i in self._from_input(inp)]  # '(None, None), (None, None)' so that it can be unpacked in 'for ((x_p, y_p), (sigma, mu)), label, color in data:' without errors even if 'dots' or 'fit' is False
        for i, r in enumerate(ratings):
            min_r, max_r = min(r), max(r)  # minimum/maximum rating with checkmate type 'NUMBERS[i]'
            _len = max_r - min_r + 1
            x, y = np.arange(min_r, max_r + 1, 1), np.zeros(_len)  # x = [min(r), min(r) + 1, ..., max(r) - 1, max(r)], y = [0, 0, ..., 0, 0], both have length max(r) - min(r) + 1
            for k, n in Counter(r).items():  # Counter counts how many occurrences of each rating is
                y[k - min_r] = n  # set every rating
            y[1500 - min_r] = (y[1499 - min_r] + y[1501 - min_r])/2  # since the starting rating on lichess is 1500, there is a spike at that rating, therefore the the average of rating = 1499 and rating = 1501 is taken
            y /= y.sum()  # normalize such that the area of the gaussian is 1

            if dots:
                x_plot, y_plot = [], []
                for j in range(0, _len, rating_interval):
                    y_val = y[j:min(j + rating_interval, _len)].sum()/rating_interval  # average of the ratings in interval [j, j + rating_interval) to reduce noise
                    if y_val == 0:  # don't add point when there are no players in with rating in interval y_val
                        continue
                    x_plot.append(j + min_r)  # add
                    y_plot.append(y_val)  # point
                data[i][0][0] = (x_plot, y_plot)
            if fit:
                params = self._fit(x, y, x.mean())  # pass mean as initial value for μ, otherwise lmfit raises an Error caused by NaN values, fit the data and get the parameters σ and μ
                data[i][0][1] = params

        for ((x_p, y_p), (sigma, mu)), label, color in data:
            if dots:
                plt.plot(x_p, y_p, 'o', ms=6, label=label, color=color, markeredgecolor='w', markeredgewidth=1)  # plot points
            if fit:
                x_f = np.linspace(*plt.xlim(), 800)  # x_fit
                y_f = self.gaussian(x_f, sigma, mu)
                plt.plot(x_f, y_f, lw=2, label=f'{label}: σ = {round(sigma.value, 2)} ± {round(sigma.stderr, 2)}, μ = {round(mu.value, 2)} ± {round(mu.stderr, 2)}', color=color)  # plot gaussian
            plt.legend()
            if show:
                plt.show()
            elif type(show) is tuple:
                plt.title(start.year)
                fig = plt.gcf()
                fig.set_size_inches(*save[1:])
                fig.tight_layout()
                fig.savefig(save[0], dpi=100, transparent=True)

    def games_sum(self, first_year: int = 2013, last_year: int = 2021, inp=None) -> None:
        plt.style.use(PLT_STYLE)
        plt.ylabel('games')
        plt.title(f'{first_year} - {last_year}')

        start = datetime(first_year, 1, 1)  # set start datetime
        end = datetime(last_year + 1, 1, 1)  # set end datetime

        for i in self._from_input(inp):
            plt.bar(NUMBERS[i], sum(month[i + 5] for month in self.general if start <= month[0] < end), color=COLORS[i])  # sum of games if month between start and end
        plt.tight_layout()
        plt.show()

    def games_t(self, inp=None, absolute: bool = False, show: bool = True) -> tuple[list[float, ], list[tuple[list[int, ], str, str]]]:
        years = [2013 + i * 1 / 12 for i in range(len(self.general))]  # comparable to numpy.linspace
        data = [([], NUMBERS[i], COLORS[i]) for i in self._from_input(inp)]  # list of: tuple of list (number of games), label and color
        for month in self.general:
            for i, j in enumerate(self._from_input(inp)):
                g = month[j + 5] if absolute else [1000000 * month[j + 5] / month[4]]  # divide through total number of games analyzed if not absolute
                data[i][0].append(g)

        if show:
            plt.close()
            plt.style.use(PLT_STYLE)
            plt.xlabel('year')
            y_label = 'games per month' if absolute else 'games per month [ppm]'
            plt.ylabel(y_label)

            for d, label, color in data:
                plt.plot(years, d, label=label, c=color)  # plot data
            plt.legend()
            plt.show()
        return data, years


class Figures(Games):
    def __init__(self, games_path: str, log_path: str):
        super().__init__()
        self.read(games_path, log_path)

    def save_plt(self, path: str) -> None:  # save current plt figure
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        fig.tight_layout()
        fig.savefig(path, dpi=100, transparent=True)
        print(f'[saved] {path}')

    def rating_probability__year(self, inp=None, last_year: int = 2020, ylim: tuple[float, float] = None, fit: bool = True, dots: bool = True, rating_interval: float = 20):
        plt.style.use(PLT_STYLE)
        ratings = sum(self.ratings(inp), [])  # get every occurrence of every rating into list
        llim, rlim = min(ratings) - 100, max(ratings) + 100  # set x-boundaries
        for year in range(2013, last_year + 1):  # last_year should be included
            for i in self._from_input(inp):
                self.p_ratings(date(year, 1, 1), date(year + 1, 1, 1), i, fit, dots, rating_interval, llim, rlim, ylim, (f'p_{NUMBERS[i]}__{year}.png', 18.5, 10.5))  # dots, rating_interval, ylim are inputted
                print(f'[saved] p_{NUMBERS[i]}__{year}.png')

    def player_most__type(self, inp=None, n: int = 10):
        plt.style.use(PLT_STYLE)
        for i in self._from_input(inp):
            raw = []  # get every occurrence of every name into list
            for j in self.data[i]:
                for k in j[1]:
                    raw.append(k)

            last_m = 0
            for j, (player, m) in enumerate(Counter(raw).most_common()):  # Counter(raw).most_common() returns a list of tuples with every element and it's count
                if j >= n and m != last_m:  # checking for m != last_m is (imo) necessary because without it names that are at index n, n + 1 and so on in the list but still have the same number as at index n - 1 won't be shown
                    break
                last_m = m
                plt.bar(player, m, color=COLORS[j % 6])

            plt.ylabel('games')
            self.save_plt(f'n_{NUMBERS[i]}__player.png')
            plt.clf()  # clf() to remove the existing bars

    def number_games__month(self, inp=None, absolute: bool = False, month_interval: int = 3):  # animating development in monthly games
        plt.style.use(PLT_STYLE)
        plt.xlabel('year')
        plt.ylabel('games per month' if absolute else 'games per month [ppm]')

        data, t = self.games_t(inp, absolute, False)  # get x, y data

        plt.xlim(t[0] - 0.3, t[-1] + 0.3)  # set left, right and
        plt.ylim(min(0, min(min(d[0]) for d in data)), 1.1 * max(max(d[0]) for d in data))  # bottom, top boundaries so that they stay constant

        for n in range(0, len(data[0][0]), month_interval):
            for d, label, color in data:
                plt.plot(t[:n], d[:n], label=label, c=color)  # plot number of games until n-th month
            m = str(round(12 * (t[n] % 1)) + 1)  # get months from years
            self.save_plt(f'{label}__month_{int(t[n])}-{"0" if len(m) == 1 else ""}{m}')


def year(a: int, b: int = None) -> tuple[datetime, datetime]:
    b = a + 1 if b is None else b + 1
    return datetime(a, 1, 1), datetime(b, 1, 1)


if __name__ == '__main__':
    games = Games()
    games.read(DATA_CSV, LOG_FILE)
