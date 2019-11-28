import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
from typing import Tuple, Callable
from dataclasses import dataclass
import matplotlib

Patch = matplotlib.patches.Patch
PosVal = Tuple[float, Tuple[float, float]]


@dataclass
class AnnotateBars:
    ax: matplotlib.axes.Axes
    font_size: int = 10
    color: str = "black"
    n_dec: int = 2

    def horizontal(self, centered=False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_width()
            div = 2 if centered else 1
            pos = (
                p.get_x() + p.get_width() / div,
                p.get_y() + p.get_height() / 2,
            )
            return value, pos

        self._annotate(get_vals, ha="center" if centered else "left", va="center")

    def vertical(self, centered=False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_height()
            div = 2 if centered else 1
            pos = (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / div)
            return value, pos

        self._annotate(get_vals, ha="center", va="center" if centered else "bottom")

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

rotate_xticks(axes[0][0], 0)
rotate_xticks(axes[1][0], 0)

AnnotateBars(axes[0][0]).vertical()
AnnotateBars(axes[1][0], color="blue").vertical(True)
AnnotateBars(axes[0][1]).horizontal()
AnnotateBars(axes[1][1], font_size=8, n_dec=1).horizontal(True)
plt.show()
