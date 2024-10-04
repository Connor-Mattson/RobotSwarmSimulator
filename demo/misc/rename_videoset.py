import os
FILE_DIR = "/Users/connor/Desktop/test_videos"
EXT = ".gif"

if __name__ == "__main__":
    for i, fn in enumerate(os.listdir(FILE_DIR)):
        if fn[-len(EXT):] == EXT:
            os.rename(os.path.join(FILE_DIR, fn), os.path.join(FILE_DIR, f"{i}{EXT}"))