# Download and Combine TS Video Segments

This Python script allows you to download and combine `.ts` video segments from a streaming service into a single `.mp4` file. The script is flexible and can handle different segment URL structures, making it adaptable to various streaming services.

## Features

- **Download TS Segments**: Download multiple `.ts` video segments from a streaming service.
- **Combine Segments**: Automatically combine the downloaded `.ts` segments into a single `.mp4` file using `ffmpeg`.
- **Flexible URL Structure**: Accepts a customizable segment URL structure via the `--structure` parameter.
- **Sneaky Mode**: Optional sneaky mode to add delays between downloads, mimicking natural streaming behavior.

## Requirements

- Python 3.x
- `ffmpeg` installed on your system
- Python packages:
  - `requests`
  - `argparse`

You can install the necessary Python packages using pip:

```bash
pip install requests argparse
```
## Installation
Clone the repository or download the script.
Ensure ffmpeg is installed on your system:
```bash
sudo apt-get install ffmpeg
```
## Usage
To use the script, run it with the following command:

```bash
python download-stream.py <first_ts_url> <last_ts_url> --structure <segment_structure> [--sneaky]
```

## Parameters
```bash
<first_ts_url>: The URL of the first .ts segment.
<last_ts_url>: The URL of the last .ts segment.
--structure: The URL structure for the .ts segments with a {} placeholder for the segment number.
--sneaky: (Optional) Enable sneaky mode, which adds a delay between downloads to mimic natural streaming.

python download-stream.py "https://streamcdnm4-ply.com/Puntate/15402551_,1800,2400,.mp4.csmil/seg-1-f2-v1-a1.ts" "https://streamcdnm4-ply.com/Puntate/15402551_,1800,2400,.mp4.csmil/seg-79-f2-v1-a1.ts" --structure "seg-{}-f2-v1-a1.ts" --sneaky
```

This command will:

Download all segments from seg-1-f2-v1-a1.ts to seg-79-f2-v1-a1.ts.
Combine them into a single .mp4 file named output_video.mp4.
Add a 5-second delay between downloads in sneaky mode.

## How it Works
Extracting Pattern and Numbers: The script extracts the base URL, the segment start number, and the segment end number from the provided URLs and structure.
Downloading Segments: It loops through all segment numbers in the specified range, constructs the full URL for each segment, and downloads it.
Combining Segments: The script uses ffmpeg to concatenate the downloaded .ts segments into a single .mp4 file.

## Troubleshooting

400 Bad Request Error: Ensure that the URLs are correctly formatted and not expired. Some streaming services use temporary URLs that may expire.
ffmpeg Errors: Make sure ffmpeg is installed correctly and that the paths to the .ts files in segments_list.txt are correct and accessible.
File Not Found: If the script fails to find certain segments, double-check the segment numbers and ensure the URLs are correct.
