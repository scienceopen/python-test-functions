from matplotlib.pyplot import figure, draw, close
from pathlib import Path


def genimgseries(odir: Path) -> list[Path]:
    if figure is None:
        raise ImportError("pip install matplotlib")

    odir = Path(odir).expanduser()

    fg = figure(1, figsize=(0.5, 0.5))
    # fg.set_visible(False)
    ax = fg.gca()

    flist = []
    for i in range(10):
        ax.clear()
        ax.axis("off")

        ax.text(0, 0, str(i), fontsize=36)

        draw()

        fn = odir / f"{i}.png"
        flist.append(fn)

        fg.savefig(fn, bbox_inches="tight", pad_inches=0)

    close(fg)

    return flist
