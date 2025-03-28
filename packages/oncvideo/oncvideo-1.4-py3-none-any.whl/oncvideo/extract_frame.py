"""Function to extract frames from videos"""

from pathlib import Path
import tempfile
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import cv2
from ._utils import download_file, to_timedelta, strftd2, parse_file_path, run_ffmpeg
from .utils import name_to_timestamp
from ._iterate_ffmpeg import iterate_ffmpeg, iterate_init

def _ffmpeg_run_frame(input_file, output_file, skip, params, f, subfolder, video_name):
    """
    Create ffmpeg command and run and 
    write in a csv file for the generated frames
    """
    # rename output to extract frames
    file_name = output_file.stem
    outfolder = output_file.parent
    output_file = f"{outfolder / file_name}_%05d.jpg"

    # Create ffmpeg command and run
    ff_cmd = ['ffmpeg'] + skip + ['-i', input_file] + params['ffmpeg'] + [output_file]
    run_ffmpeg(ff_cmd, filename=file_name)

    # rename frames to correct timestamp
    d = outfolder.glob(file_name + "_*.jpg")
    dout = pd.DataFrame({'filename_old': list(d), 'original_video': video_name})
    if len(dout) > 0: # didn't extracted any frame (e.g. file length is lower than interval)
        dout['filename_split'] = dout['filename_old'].apply(lambda x: x.stem.split('_'))
        dout['timestamp'] = dout['filename_split'].str[-2]

        if dout['timestamp'].str.contains('Z-', regex=False).any():
            dout['timestamp'] = dout['timestamp'].str.split('-').str[0]

        dout['timestamp'] = pd.to_datetime(dout['timestamp'], format='%Y%m%dT%H%M%S.%fZ', utc=True)
        dout['timeadd'] = (dout['filename_split'].str[-1].astype(float) *
            params['interval'] - params['interval2'])
        dout['timestamp'] = dout['timestamp'] + pd.to_timedelta(dout['timeadd'], unit='sec')
        dout['filename'] = (dout['filename_split'].str[:-2].str.join('_') + '_' +
            dout['timestamp'].dt.strftime('%Y%m%dT%H%M%S.%f').str[:-3] + 'Z.jpg')

        for _, row2 in dout.iterrows():
            row2['filename_old'].rename(row2['filename_old'].with_name(row2['filename']))

        # save csv with all frames names + original videos
        if subfolder != '':
            dout['subfolder'] = subfolder[:-1]
            dout = dout[['subfolder', 'filename', 'original_video', 'timestamp']]
        else:
            dout = dout[['filename', 'original_video', 'timestamp']]

        dout.to_csv(f, mode='a', index=False, header=False, lineterminator='\n')
    else:
        with open("log_download.txt", 'a', encoding="utf-8") as ferr:
            ferr.write(f"No frame was extracted from: {input_file.name}\n")


def extract_frame(source, interval, output='frames', trim=False,
    deinterlace=False, rounding_near=False):
    """
    Extract frames at a given interval

    Parameters
    ----------
    source : str or pandas.DataFrame
        A pandas DataFrame, a path to .csv file, or a Glob pattern to
        match multiple files (use \*)
    interval : float
        Interval, in seconds, to extract frames (e.g. a value of 10 will
        extract one frame every 10 seconds).
    output : str, default 'output'
        Name of the output folder to save converted videos
    trim : bool, default False
        Trim video files to match the initial search query
    deinterlace : bool, default False
        Deinterlace video before getting the frames.
    rounding_near : bool, default False
        Grab frames at the middle of each interval (default ffmpeg
        behavior). If False, will grab frames at the start of each interval.
    """
    header = 'filename,original_video,timestamp\n'

    if interval < 1.0:
        vf_cmd = f'fps={1/interval}'
    elif interval == 1.0:
        vf_cmd = 'fps=1'
    else:
        vf_cmd = f'fps=1/{interval}'

    if deinterlace:
        vf_cmd = 'pp=ci|a,' + vf_cmd

    if rounding_near:
        interval2 = interval / 2
    else:
        vf_cmd = vf_cmd + ':round=up'
        interval2 = interval

    params = {'ffmpeg': ['-vf', vf_cmd,
            '-qmin', '1', '-q:v', '1'],
        'interval': interval,
        'interval2': interval2
    }

    iterate_ffmpeg(source, output, header, trim, _ffmpeg_run_frame, params)


def extract_fov(source, timestamps=None, clip_or_sharpest='sharpest', duration=None, output='fovs', deinterlace=False):
    """
    Extract FOVs from videos

    Extract framegrabs or clips for each video at given timestamps 

    Parameters
    ----------
    source : str or pandas.DataFrame
        A pandas DataFrame, a path to .csv file, or a Glob pattern to
        match multiple files (use \*)
    timestamps : str, float, or list
        A timestamp or a list of timestaps where the framegrabs will be extracted.
        Can be a float indicating the number of seconds or a string in the format
        mm:ss.f, from the start of the video. If None (the default), it will try to
        get the timestamps from the column 'fovs' in the source.
    clip_or_sharpest : {'sharpest', 'clip'}
        If 'clip', the function will save clips instead of framegrabs, with
        duration given in seconds. The start of the clips are given by 'timestamps'.
        If 'sharpest', will save the sharpest frame only within the clip.
        This argument is ignored if duration is None.
    duration : float
        The duration of the FOVs, given in seconds or mm:ss.f format.
    output : str, default 'fovs'
        Name of the output folder to save images/videos.
    deinterlace : bool, default False
        Deinterlace video before getting the frames. This argument is ignored
        for clips, since the stream is copied from the original video.
    """
    df, has_group, need_download = parse_file_path(source)

    fov_csv = 'fovs' in df

    if fov_csv:
        df['fovs'] = df['fovs'].str.split(',')
        df['fovs'] = df['fovs'].apply(lambda x: [to_timedelta(y) if y != '' else '' for y in x])

        df['subfolder'] = df['fovs'].apply(lambda x: [f'FOV{y+1}' for y in list(range(len(x)))])
        maxfov = df['fovs'].apply(len).max()
        fovfolder = [f'FOV{y+1}' for y in list(range(maxfov))]

    else:
        if timestamps is None:
            raise ValueError("You must provide a timestamp to extract the FOV,",
            "or the csv file must contain the column 'fovs'")
        if not isinstance(timestamps, list):
            timestamps = [timestamps]
        fovs = [to_timedelta(x) for x in timestamps]
        df['fovs'] = [fovs for _ in range(len(df))]
        fovfolder = [f'FOV_{strftd2(x)}' for x in fovs]
        df['subfolder'] = [fovfolder for _ in range(len(df))]

    # header for the output csv

    header = f"original_video,{','.join(fovfolder)}\n"

    df, folder, f = iterate_init(output, header, df, has_group)

    if deinterlace:
        vf_cmd = ['-vf', 'pp=ci|a']
    else:
        vf_cmd = []

    if duration is not None:
        duration = str(duration)

        match clip_or_sharpest:
            case 'clip':
                sharpest = False
            case 'sharpest':
                sharpest = True
            case _:
                raise ValueError("'clip_or_sharpest' must be a string either 'clip' or 'sharpest'")


    # start for loop
    pbar = tqdm(total=df.shape[0], desc = 'Processed files')

    try:
        for name, group in df.groupby('group'):

            if has_group:
                outfolder = folder / Path(name)
                outfolder.mkdir(exist_ok=True)
            else:
                outfolder = folder

            # Create folder for each FOV
            if fov_csv:
                maxfov = group['fovs'].apply(len).max()
                fovs = [f'FOV{y+1}' for y in list(range(maxfov))]

                for fov in fovs:
                    p = outfolder / Path(fov)
                    p.mkdir(exist_ok=True)
            else:
                for fov in fovfolder:
                    p = outfolder / Path(fov)
                    p.mkdir(exist_ok=True)

            # extract frames for each video
            for _, row in group.iterrows():
                # download video
                file_name_p = Path(row['filename'])
                if need_download:
                    tmpfile = tempfile.gettempdir() / file_name_p
                    download_file(row['urlfile'], tmpfile)
                    tmpfile_str = str(tmpfile)
                else:
                    tmpfile_str = row['urlfile']

                # get timestamp of file
                timestamp = name_to_timestamp(file_name_p.name)
                oldname_dc = timestamp.dc

                # Extract frame/video for each FOV
                filename_fovs = []
                for fov, p in zip(row['fovs'], row['subfolder']):

                    if fov == '':
                        filename_fovs.append(new_name.name)
                        continue

                    newtime = (timestamp + fov).strftime('%Y%m%dT%H%M%S.%f')[:-3]
                    filename = f"{oldname_dc}_{newtime}Z{file_name_p.suffix}"
                    new_name_p = Path(filename)
                    fov_str = str(fov.total_seconds())

                    if duration is None:
                        new_name = outfolder / p / new_name_p.with_suffix('.jpg')
                        ff_cmd = ['ffmpeg', '-ss', fov_str, '-i',
                            tmpfile_str] + vf_cmd + ['-frames:v', '1', '-update', '1',
                            '-qmin', '1', '-q:v', '1', new_name]
                        run_ffmpeg(ff_cmd, filename=new_name.name)

                    else:
                        new_name = outfolder / p / new_name_p
                        ff_cmd =['ffmpeg', '-ss', fov_str,
                            '-i', tmpfile_str, '-t', duration, '-c', 'copy', new_name]
                        run_ffmpeg(ff_cmd, filename=new_name.name)
                        
                        if sharpest:
                            sharpest_frame, time = extract_sharpest_frame(str(new_name))
                            new_name.unlink()

                            if sharpest_frame is not None:

                                newtime = (timestamp + fov + time).strftime('%Y%m%dT%H%M%S.%f')[:-3]
                                filename = f"{oldname_dc}_{newtime}Z.jpg"
                                new_name = outfolder / p / Path(filename)

                                cv2.imwrite(str(new_name), sharpest_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                            

                    filename_fovs.append(new_name.name)

                if need_download:
                    tmpfile.unlink()

                # save csv with video name
                if has_group:
                    f.write(f"{name},{row['filename']},{','.join(filename_fovs)}\n")
                else:
                    f.write(f"{row['filename']},{','.join(filename_fovs)}\n")

                pbar.update()

    finally:
        pbar.close()
        f.close()


def extract_sharpest_frame(video_path, brt_thr=50):
    """
    Select the frame with highest sharpness from a video
    Also excludes black frames, with median brightness below brt_thr
    Return the selected frame and time, in seconds, where the frame was
    """
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frame rate
    skip = fps // 2
    
    if not cap.isOpened():
        return

    sharpest_frame = None
    max_sharpness = 0
    count = -1
    frame_number = 0

    while True:
        count += 1
        if count % skip != 0: # skip every half second
            ret = cap.grab()
            continue

        ret, frame = cap.read()
        if not ret:
            break  # Exit when video ends

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if np.median(gray) < brt_thr:
            continue

        # Compute Laplacian variance (sharpness)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Keep the sharpest frame
        if sharpness > max_sharpness:
            max_sharpness = sharpness
            frame_number = count
            sharpest_frame = frame.copy()

    cap.release()

    time = pd.to_timedelta(frame_number / fps, unit='s')

    return sharpest_frame, time
