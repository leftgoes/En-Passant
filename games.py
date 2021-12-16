from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from inspect import getsource


from main import NUMBERS
COLORS = ['#0f264a', '#13283a', '#4a8a9c', '#184144', '#359a9a', '#006060']  # '#f0d9b5', '#b58863', '#b57563', '#b5534b', '#ca6565', '#ff9f9f'


class Games:
    __slots__ = ('data', 'games_file', 'log_data', 'log_games', 'log_file')

    def __init__(self, games_file: str, log_file: str):
        self.log_file = log_file
        self.games_file = games_file

        self.data: list[list[datetime, ], ]
        self.log_data: list[list[int, ], ]
        self.log_games: list[int, ]

    @staticmethod
    def gaussian(x, s, m):
        return np.exp(-(x - m)**2/(2 * s**2))/(s * np.sqrt(2 * np.pi))

    @staticmethod
    def linmap(value: float, actual_bounds: tuple[float, float], desired_bounds: tuple[float, float]) -> float:
        return desired_bounds[0] + (value - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (actual_bounds[1] - actual_bounds[0])

    @staticmethod
    def str(x: int, n: int) -> str:
        x = str(x)
        return (n - len(x)) * '0' + x

    @staticmethod
    def _from_input(inp) -> list or range:
        if inp is None:
            return range(6)

        t = type(inp)
        if t is range:
            return inp

        inp = list(inp) if t is list or t is set else [inp]
        return [NUMBERS.index(i) if type(i) is str else i for i in inp]

    @staticmethod
    def month_from_datetime(d: datetime) -> int:
        return 12 * (d.year - 2013) + d.month - 1

    @staticmethod
    def get_param(result):
        parameters, report = [['variable', 'value', '+/-']], result.fit_report()
        for parm in report[report.find('[[Variables]]') + 18:report.find('[[Correlations]]')].replace('\n', '').split(
                '    '):
            parm_data = [parm[0]]
            for p in parm.split(' '):
                try:
                    parm_data.append(float(p))
                except ValueError:
                    pass
            parameters.append(parm_data)
        return parameters

    def fit(self, x, y):
        for line in getsource(self.gaussian).splitlines():
            if line.find('def') != -1:
                args = line[line.find(',') + 2:line.find(')')].replace(' ', '').split(',')
                break
        else:
            raise Exception
        initial = dict(zip(args, [1 for _ in args]))
        model = Model(self.gaussian)
        return self.get_param(model.fit(y, x=x, **initial))

    def from_year(self, year: int, *args, **kwargs):
        return self.from_interval(date(year, 1, 1), date(year + 1, 1, 1), *args, **kwargs)

    def from_interval(self, start: date, end: date, game: bool = True, player: bool = False, rating_mean: bool = None, rating: bool = False, inp=None) -> list[str, ]:
        indices = self._from_input(inp)

        ratings, names, games_no = [[] for _ in indices], [{} for _ in indices], [0 for _ in indices]
        for i in range(len(indices)):
            for d in self.data[i]:
                if d[0].date() > end:
                    break
                elif d[0].date() < start:
                    continue

                if game:
                    games_no[i] += 1
                if player:
                    for n in d[1]:
                        if n in names:
                            names[i][n] += 1
                        else:
                            names[i][n] = 1
                if rating_mean is True or rating_mean is False:
                    for r in d[2]:
                        ratings[i].append(int(r))

        data = [f'{start.year}.{start.month}', f'{end.year}.{end.month}']
        if game:
            data.append(games_no)
        if rating:
            rating_data = []
            for rat in ratings:
                min_rat, max_rat = min(rat), max(rat)
                num = round(max_rat - min_rat)
                rat_data = np.zeros(num)
                for r in rat:
                    rat_data[round(self.linmap(r, (min_rat, max_rat), (0, num - 1)))] += 1

                # accounting for the fact that lichess ratings start at 1500 which means that there are more players with that rating
                i_1500 = round(self.linmap(1500, (min_rat, max_rat), (0, num - 1)))
                rat_data[i_1500] = (rat_data[i_1500 - 1] + rat_data[i_1500 + 1])/2

                rat_data /= rat_data.sum()
                rating_data.append((np.linspace(min_rat, max_rat, num), rat_data))  # x
            data.append(rating_data)
            return data
        if player:
            player_data = []
            for n in names:
                max_value = max(n.values())
                if max_value == 1:
                    player_data.append([1])
                else:
                    player_data.append([max_value] + [i for i, j in n.items() if j == max_value])
            data.append(player_data)
        if rating_mean is True:
            data.append([sum(r)/len(r) for r in ratings])
        elif rating_mean is False:
            for r in ratings:
                r.sort()
            data.append([r[len(r)//2] for r in ratings])
        return data

    def read(self):
        self.read_games()
        self.read_log()

    def read_games(self):
        with open(self.games_file, 'r') as f:
            lines = f.read().splitlines()

        self.data = [[] for _ in range(6)]
        for line in lines[1:]:
            line_data = line.split(',')
            names = line_data[4:6]
            ratings = [int(rating) for rating in line_data[6:8] if rating != '?']
            self.data[int(line_data[0])].append((datetime.strptime(line_data[2] + ' ' + line_data[3], "%Y.%m.%d %H:%M:%S"), names, ratings))

    def read_log(self):
        with open(self.log_file, 'r') as f:
            lines = f.read().splitlines()

        self.log_data, self.log_games = [[] for _ in range(6)], []
        first = lines[0].split(',')
        i = first.index(NUMBERS[0]) if lines[0].find(NUMBERS[0]) != -1 else -6
        j = first.index('games detected') if lines[0].find('games detected') != -1 else -8

        for line in lines[1:]:
            s = line.split(',')
            self.log_games.append(int(s[j]))
            line_data = s[i:]
            for k, g in enumerate(line_data):
                self.log_data[k].append(int(g))

    def p_ratings(self, start: date, end: date, inp=None, fit: bool = False, dots: bool = True, rating_interval: float = 15):
        data = self.from_interval(start, end, False, False, True, True, inp)

        plt.title(f'{data[0]} - {data[1]}')
        plt.xlabel('rating')
        plt.ylabel('probability')
        for i, (x, y) in zip(self._from_input(inp), data[2]):#
            if dots:
                x_min = x.min()
                x_len, y_len = len(x), len(y)
                x_plot, y_plot = [], []
                for j in range(0, x_len, rating_interval):
                    x_plot.append(j + x_min)
                    y_plot.append(y[j:min(j + rating_interval, y_len)].sum()/rating_interval)
                plt.plot(x_plot, y_plot, 'o', ms=2, label=NUMBERS[i])
            if fit:
                x_mean = x.mean()
                args = self.fit(x - x_mean, y)[1:]
                sigma, mu = args[0][1], args[1][1]
                x_fit = np.linspace(x[0] - x_mean, x[-1] - x_mean, 500)
                y_fit = self.gaussian(x_fit, sigma, mu)
                plt.plot(x_fit + x_mean, y_fit, lw=2, label=f'{NUMBERS[i]}: σ = {round(sigma, 2)}, μ = {round(mu + x_mean, 2)}')
        plt.legend()
        plt.show()

    def games_t(self, inp=None, absolute: bool = False, legend: bool = True, show: bool = True):
        plt.close()
        plt.xlabel('years after Jan 2013')
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from inspect import getsource


from main import NUMBERS
COLORS = ['#0f264a', '#13283a', '#4a8a9c', '#184144', '#359a9a', '#006060']  # '#f0d9b5', '#b58863', '#b57563', '#b5534b', '#ca6565', '#ff9f9f'


class Games:
    __slots__ = ('data', 'games_file', 'log_data', 'log_games', 'log_file')

    def __init__(self, games_file: str, log_file: str):
        self.log_file = log_file
        self.games_file = games_file

        self.data: list[list[datetime, ], ]
        self.log_data: list[list[int, ], ]
        self.log_games: list[int, ]

    @staticmethod
    def gaussian(x, s, m):
        return np.exp(-(x - m)**2/(2 * s**2))/(s * np.sqrt(2 * np.pi))

    @staticmethod
    def linmap(value: float, actual_bounds: tuple[float, float], desired_bounds: tuple[float, float]) -> float:
        return desired_bounds[0] + (value - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (actual_bounds[1] - actual_bounds[0])

    @staticmethod
    def str(x: int, n: int) -> str:
        x = str(x)
        return (n - len(x)) * '0' + x

    @staticmethod
    def _from_input(inp) -> list or range:
        if inp is None:
            return range(6)

        t = type(inp)
        if t is range:
            return inp

        inp = list(inp) if t is list or t is set else [inp]
        return [NUMBERS.index(i) if type(i) is str else i for i in inp]

    @staticmethod
    def _get_param(result):
        parameters, report = [['variable', 'value', '+/-']], result.fit_report()
        for parm in report[report.find('[[Variables]]') + 18:report.find('[[Correlations]]')].replace('\n', '').split(
                '    '):
            parm_data = [parm[0]]
            for p in parm.split(' '):
                try:
                    parm_data.append(float(p))
                except ValueError:
                    pass
            parameters.append(parm_data)
        return parameters

    def _fit(self, x, y):
        for line in getsource(self.gaussian).splitlines():
            if line.find('def') != -1:
                args = line[line.find(',') + 2:line.find(')')].replace(' ', '').split(',')
                break
        else:
            raise Exception
        initial = dict(zip(args, [1 for _ in args]))
        model = Model(self.gaussian)
        return self._get_param(model.fit(y, x=x, **initial))

    def _from_year(self, year: int, *args, **kwargs):
        return self._from_interval(date(year, 1, 1), date(year + 1, 1, 1), *args, **kwargs)

    def _from_interval(self, start: date, end: date, game: bool = True, player: bool = False, rating_mean: bool = None, rating: bool = False, inp=None) -> list[str, ]:
        indices = self._from_input(inp)

        ratings, names, games_no = [[] for _ in indices], [{} for _ in indices], [0 for _ in indices]
        for i in range(len(indices)):
            for d in self.data[i]:
                if d[0].date() > end:
                    break
                elif d[0].date() < start:
                    continue

                if game:
                    games_no[i] += 1
                if player:
                    for n in d[1]:
                        if n in names:
                            names[i][n] += 1
                        else:
                            names[i][n] = 1
                if rating_mean is True or rating_mean is False:
                    for r in d[2]:
                        ratings[i].append(int(r))

        data = [f'{start.year}.{start.month}', f'{end.year}.{end.month}']
        if game:
            data.append(games_no)
        if rating:
            rating_data = []
            for rat in ratings:
                min_rat, max_rat = min(rat), max(rat)
                num = round(max_rat - min_rat)
                rat_data = np.zeros(num)
                for r in rat:
                    rat_data[round(self.linmap(r, (min_rat, max_rat), (0, num - 1)))] += 1

                # accounting for the fact that lichess ratings start at 1500 which means that there are more players with that rating
                i_1500 = round(self.linmap(1500, (min_rat, max_rat), (0, num - 1)))
                rat_data[i_1500] = (rat_data[i_1500 - 1] + rat_data[i_1500 + 1])/2

                rat_data /= rat_data.sum()
                rating_data.append((np.linspace(min_rat, max_rat, num), rat_data))  # x
            data.append(rating_data)
            return data
        if player:
            player_data = []
            for n in names:
                max_value = max(n.values())
                if max_value == 1:
                    player_data.append([1])
                else:
                    player_data.append([max_value] + [i for i, j in n.items() if j == max_value])
            data.append(player_data)
        if rating_mean is True:
            data.append([sum(r)/len(r) for r in ratings])
        elif rating_mean is False:
            for r in ratings:
                r.sort()
            data.append([r[len(r)//2] for r in ratings])
        return data

    def read(self):
        self.read_games()
        self.read_log()

    def read_games(self):
        with open(self.games_file, 'r') as f:
            lines = f.read().splitlines()

        self.data = [[] for _ in range(6)]
        for line in lines[1:]:
            line_data = line.split(',')
            names = line_data[4:6]
            ratings = [int(rating) for rating in line_data[6:8] if rating != '?']
            self.data[int(line_data[0])].append((datetime.strptime(line_data[2] + ' ' + line_data[3], "%Y.%m.%d %H:%M:%S"), names, ratings))

    def read_log(self):
        with open(self.log_file, 'r') as f:
            lines = f.read().splitlines()

        self.log_data, self.log_games = [[] for _ in range(6)], []
        first = lines[0].split(',')
        i = first.index(NUMBERS[0]) if lines[0].find(NUMBERS[0]) != -1 else -6
        j = first.index('games detected') if lines[0].find('games detected') != -1 else -8

        for line in lines[1:]:
            s = line.split(',')
            self.log_games.append(int(s[j]))
            line_data = s[i:]
            for k, g in enumerate(line_data):
                self.log_data[k].append(int(g))

    def p_ratings(self, start: date, end: date, inp=None, fit: bool = False, dots: bool = True, rating_interval: float = 15):
        data = self._from_interval(start, end, False, False, True, True, inp)

        plt.title(f'{data[0]} - {data[1]}')
        plt.xlabel('rating')
        plt.ylabel('probability')
        for i, (x, y) in zip(self._from_input(inp), data[2]):#
            if dots:
                x_min = x.min()
                x_len, y_len = len(x), len(y)
                x_plot, y_plot = [], []
                for j in range(0, x_len, rating_interval):
                    x_plot.append(j + x_min)
                    y_plot.append(y[j:min(j + rating_interval, y_len)].sum()/rating_interval)
                plt.plot(x_plot, y_plot, 'o', ms=2, label=NUMBERS[i])
            if fit:
                x_mean = x.mean()
                args = self._fit(x - x_mean, y)[1:]
                sigma, mu = args[0][1], args[1][1]
                x_fit = np.linspace(x[0] - x_mean, x[-1] - x_mean, 500)
                y_fit = self.gaussian(x_fit, sigma, mu)
                plt.plot(x_fit + x_mean, y_fit, lw=2, label=f'{NUMBERS[i]}: σ = {round(sigma, 2)}, μ = {round(mu + x_mean, 2)}')
        plt.legend()
        plt.show()

    def games_t(self, inp=None, absolute: bool = False, legend: bool = True, show: bool = True):
        plt.close()
        plt.xlabel('years after Jan 2013')
        y_label = 'games' if absolute else 'games per million'
        plt.ylabel(y_label)

        years = [i * 1 / 12 for i in range(len(self.log_games))]
        for i in self._from_input(inp):
            if type(i) is str:
                i = NUMBERS.index(i)
            data = self.log_data[i] if absolute else [1000000 * month / self.log_games[i] for i, month in enumerate(self.log_data[i])]
            plt.plot(years, data, label=NUMBERS[i], c=COLORS[i])

        if show:
            if legend:
                plt.legend()
            plt.show()

    def games_sum(self, start: date = None, end: date = None, inp=None, figsize: tuple[float, float] = None, show: bool = True):
        if start is None:
            start = date(2013, 1, 1)
        if end is None:
            end = date(2018, 1, 1)
        inp = self._from_input(inp)

        plt.close()
        if figsize is not None:
            plt.figure(figsize=figsize)
        plt.title(f'{start.year}.{start.month} - {end.year}.{end.month}')
        plt.ylabel('games')

        data = self._from_interval(start, end, True, False, None, None, inp)
        for i in inp:
            plt.bar(NUMBERS[i], data[2][i], color=COLORS[i])

        if show:
            plt.show()

    def ratings_sum_t(self, folder: str, inp=None):
        with open(self.log_file, 'r') as f:
            lines = f.read().splitlines()

        j = lines[0].split(',').index('month')
        first = datetime.strptime(lines[1].split(',')[j], "%Y-%m")
        last = datetime.strptime(lines[-1].split(',')[j], "%Y-%m")

        month = first
        for i in range(round((last - first).days/30)):
            self.sum(month.date(), (month + relativedelta(months=1)).date(), inp, (15, 10), False)
            plt.title(f'{month.year}.{month.month}')
            plt.savefig(f'{folder}\\frm{self.str(i, 4)}.png')
            plt.close()
            month += relativedelta(months=1)


if __name__ == '__main__':
    games = Games(CSV, LOG)
    games.read()
