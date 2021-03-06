import logging
import pytest
import subprocess
import sys

import rasterio

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def test_write_colormap_err(tmpdir):

    with rasterio.drivers():

        with rasterio.open('tests/data/shade.tif') as src:
            meta = src.meta

        tiffname = str(tmpdir.join('foo.tif'))

        with rasterio.open(tiffname, 'w', **meta) as dst:
            with pytest.raises(ValueError):
                dst.write_colormap(1, {0: (255, 0, 0, 255), 255: (0, 0, 0, 0)})


def test_write_colormap(tmpdir):

    with rasterio.drivers():

        with rasterio.open('tests/data/shade.tif') as src:
            shade = src.read_band(1)
            meta = src.meta

        tiffname = str(tmpdir.join('foo.png'))
        meta['driver'] = 'PNG'

        with rasterio.open(tiffname, 'w', **meta) as dst:
            dst.write_band(1, shade)
            dst.write_colormap(1, {0: (255, 0, 0, 255), 255: (0, 0, 0, 0)})
            cmap = dst.colormap(1)
            assert cmap[0] == (255, 0, 0, 255)
            assert cmap[255] == (0, 0, 0, 0)

        with rasterio.open(tiffname) as src:
            cmap = src.colormap(1)
            assert cmap[0] == (255, 0, 0, 255)
            assert cmap[255] == (0, 0, 0, 0)

    # subprocess.call(['open', tiffname])

