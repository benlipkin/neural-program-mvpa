from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, analysis):
        self._analysis = analysis
        self._embedding = self._analysis.embedding.split("-")[1]
        type = self._analysis.__class__.__name__
        if type in ["MVPA", "PRDA"]:
            self._feature = self._analysis.feature.split("-")[1]
            self.plot = self._plot_decoder
        elif type == "RSA":
            self.plot = self._plot_rsa
        else:
            raise TypeError("Analysis type not handled.")

    def _plot_decoder(self, show=False):
        fname = Path(__file__).parent.joinpath(
            "outputs", "plots", "mvpa", f"{self._feature}_{self._embedding}.png"
        )
        plt.hist(self._analysis.null, bins=25, color="turquoise", edgecolor="black")
        plt.axvline(self._analysis.score, color="black", linewidth=3)
        plt.xlim([0, 1])
        plt.savefig(fname)
        plt.show() if show else plt.clf()

    def _plot_rsa(self, show=False):
        fname = Path(__file__).parent.joinpath(
            "outputs", "plots", "rsa", f"{self._embedding}.jpg"
        )
        ticks = np.arange(self._analysis.corr.coef.shape[0])
        labels = np.array(["_".join(row) for row in self._analysis.corr.axes])
        indices = np.argsort(labels)
        plt.imshow(self._analysis.corr.coef[indices, :][:, indices])
        plt.xticks(ticks, labels[indices], fontsize=5, rotation=90)
        plt.yticks(ticks, labels[indices], fontsize=5)
        plt.clim([0, 1])
        plt.colorbar()
        plt.savefig(fname)
        plt.show() if show else plt.clf()
