# Copy Map Link (QGIS Plugin)

A QGIS plugin to copy map links from the map canvas for various services.

## Features

*   **Multiple Providers:** Generate links for:
    *   Google Maps
    *   OpenStreetMap
    *   Bing Maps
    *   Yandex Maps
    *   Geo URI (generic)
*   **Zoom Support:** Links now include the approximate zoom level based on your current map canvas scale.
*   **WGS84 Transformation:** Automatically transforms coordinates from your project CRS to WGS84 (EPSG:4326).

## Usage

1.  Right-click anywhere on the QGIS map canvas.
2.  Hover over the **"Copy Map Link"** menu item.
3.  Select the desired map provider from the submenu.
4.  The link is copied to your clipboard.

## Example Output

*   **Google Maps:** `https://www.google.com/maps?q=-6.886,107.605&z=15`
*   **OpenStreetMap:** `https://www.openstreetmap.org/?mlat=-6.886&mlon=107.605#map=15/-6.886/107.605`

## Installation

This plugin can be installed via the QGIS Plugin Manager once available, or manually by copying the files to your QGIS plugins directory.

## License

GNU General Public License v3.0
