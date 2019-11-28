import os

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
from typing import Tuple, Callable
from dataclasses import dataclass
import matplotlib

Patch = matplotlib.patches.Patch
PosVal = Tuple[float, Tuple[float, float]]
Axis = matplotlib.axes.Axes


@dataclass
class AnnotateBars:
    font_size: int = 10
    color: str = "black"
    n_dec: int = 2

    def horizontal(self, ax: Axis, centered=False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_width()
            div = 2 if centered else 1
            pos = (
                p.get_x() + p.get_width() / div,
                p.get_y() + p.get_height() / 2,
            )
            return value, pos

        self._annotate(ax, get_vals, ha="center" if centered else "left", va="center")

    def vertical(self, ax: Axis, centered=False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_height()
            div = 2 if centered else 1
            pos = (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / div)
            return value, pos

        self._annotate(ax, get_vals, ha="center", va="center" if centered else "bottom")

    def _annotate(self, ax: Axis, func: Callable[[Patch], PosVal], **kwargs):
        cfg = {"color": self.color, "fontsize": self.font_size, **kwargs}
        for p in ax.patches:
            value, pos = func(p)
            ax.annotate(f"{value:.{self.n_dec}f}", pos, **cfg)


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


def save_figure(fig: matplotlib.figure.Figure, path: str):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")


set_sizes((12, 8), 10)
data = sns.load_dataset("iris").groupby("species").mean()
fig, axes = plt.subplots(2, 2)
data.plot.bar(ax=axes[0][0])
data.plot.bar(stacked=True, ax=axes[1][0])

data.plot.barh(ax=axes[0][1])
data.plot.barh(stacked=True, ax=axes[1][1])

rotate_xticks(axes[0][0], 0)
rotate_xticks(axes[1][0], 0)

AnnotateBars().vertical(axes[0][0])
AnnotateBars(color="blue").vertical(axes[1][0], True)
AnnotateBars().horizontal(axes[0][1])
AnnotateBars(font_size=8, n_dec=1).horizontal(axes[1][1], True)
save_figure(fig, "./plots/medium/bar-charts.png")
plt.show()
