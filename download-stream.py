import os
import re
import sys
import requests
import subprocess
import argparse
import time

def download_and_combine_ts_files(base_url, start_num, end_num, segment_pattern, sneaky_mode=False):
    if not os.path.exists("video_segments"):
        os.makedirs("video_segments")

    ts_urls = []
    avg_duration = 5  # Assume an average duration of 5 seconds per .ts file

    for i in range(start_num, end_num + 1):
        ts_url = base_url + segment_pattern.format(i)
        ts_urls.append(ts_url)
        ts_file = f"video_segments/segment_{i}.ts"
        print(f"Downloading {ts_url} to {ts_file}...")
        try:
            response = requests.get(ts_url)
            if response.status_code == 200:
                with open(ts_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded segment {i}")
            else:
                print(f"Failed to download {ts_url}: {response.status_code}")
            
            # Sneaky mode: Sleep for the average duration between downloads
            if sneaky_mode:
                print(f"Sneaky mode: sleeping for {avg_duration} seconds...")
                time.sleep(avg_duration)
                
        except Exception as e:
            print(f"Failed to download {ts_url}: {e}")

    print("All segments downloaded. Combining into a single video file...")
    
    # Use full paths in the segments_list.txt
    segment_files = [f"file '{os.path.abspath(f'video_segments/segment_{i}.ts')}'" for i in range(start_num, end_num + 1)]
    with open("segments_list.txt", "w") as f:
        f.write("\n".join(segment_files))

    output_file = "output_video.mp4"
    try:
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", "segments_list.txt", "-c", "copy", output_file
        ])
        print(f"Video saved as {output_file}")
    except Exception as e:
        print(f"Failed to combine video segments: {e}")

def extract_pattern_and_numbers(first_url, last_url, structure):
    # Use the provided structure to extract the base URL and pattern
    match_first = re.search(r'(.*\/)' + re.escape(structure).replace(r'\{\}', r'(\d+)'), first_url)
    match_last = re.search(r'(\d+)', last_url)

    if match_first and match_last:
        base_url = match_first.group(1)
        start_num = int(match_first.group(2))
        end_num = int(match_last.group(1))
        segment_pattern = structure

        return base_url, start_num, end_num, segment_pattern
    else:
        print("Failed to extract pattern from URLs.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Download and combine .ts video segments")
    parser.add_argument("first_ts_url", help="The URL of the first .ts segment")
    parser.add_argument("last_ts_url", help="The URL of the last .ts segment")
    parser.add_argument("--structure", required=True, help="The structure of the segment URL with a '{}' placeholder for the segment number")
    parser.add_argument("--sneaky", action="store_true", help="Enable sneaky mode with delays between downloads")

    args = parser.parse_args()

    base_url, start_num, end_num, segment_pattern = extract_pattern_and_numbers(args.first_ts_url, args.last_ts_url, args.structure)
    
    print(f"Base URL: {base_url}")
    print(f"Start Number: {start_num}")
    print(f"End Number: {end_num}")
    print(f"Segment Pattern: {segment_pattern}")
    
    download_and_combine_ts_files(base_url, start_num, end_num, segment_pattern, args.sneaky)

if __name__ == "__main__":
    main()

