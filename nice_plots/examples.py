import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
from typing import Tuple, Callable
from dataclasses import dataclass
import matplotlib

Patch = matplotlib.patches.Patch
PosVal = Tuple[float, Tuple[float, float]]

@dataclass
class Annotate:
    ax: matplotlib.axes.Axes
    font_size: int = 10
    color: str = "black"
    n_dec: int = 2

    def horizontal(self):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_width()
            pos = (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2)
            return value, pos

        self._annotate(get_vals, ha="left", va="center")

    def vertical(self):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_height()
            pos = (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height())
            return value, pos

        self._annotate(get_vals, ha="center", va="bottom")

    def _annotate(self, func: Callable[[Patch], PosVal], **kwargs):
        cfg = {"color": self.color, "fontsize": self.font_size, **kwargs}
        for p in self.ax.patches:
            value, pos = func(p)
            self.ax.annotate(f"{value:.{self.n_dec}f}", pos, **cfg)


def rotate_xticks(ax: matplotlib.axes, degrees=45):
    ax.set_xticklabels(ax.get_xticklabels(), rotation=degrees)


def set_sizes(fig_size: Tuple[int, int] = (9, 6), font_size: int = 10):
    plt.rcParams["figure.figsize"] = fig_size
    plt.rcParams["font.size"] = font_size
    plt.rcParams["xtick.labelsize"] = font_size
    plt.rcParams["ytick.labelsize"] = font_size
    plt.rcParams["axes.labelsize"] = font_size
    plt.rcParams["axes.titlesize"] = font_size
    plt.rcParams["legend.fontsize"] = font_size


set_sizes((12, 8), 10)
data = sns.load_dataset("iris").groupby("species").mean()
fig, axes = plt.subplots(2, 2)
data.plot.bar(ax=axes[0][0])
data.plot.bar(stacked=True, ax=axes[1][0])

data.plot.barh(ax=axes[0][1])
data.plot.barh(stacked=True, ax=axes[1][1])

rotate_xticks(axes[0][0],0)
rotate_xticks(axes[1][0],0)

Annotate(axes[0][0]).vertical()
Annotate(axes[1][0]).vertical()
Annotate(axes[0][1]).horizontal()
Annotate(axes[1][1]).horizontal()
plt.show()
