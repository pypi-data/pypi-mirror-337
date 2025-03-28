"""Functions to allow to run commands in the terminal"""
import argparse
from pathlib import Path
from .utils import onc
from ._utils import strftd
from .list_files import list_file, list_file_batch
from .dives_onc import get_dives
from .video_info import video_info
from .didson_file import didson_info
from .extract_frame import extract_frame, extract_fov
from .timelapse import make_timelapse, align_frames
from .download_files import download_files, to_mp4
from .ts_download import download_ts, merge_ts
from .seatube import download_st, link_st, rename_st

# Default functions used by each subcommand
def flist(args):
    """
    use list_file and save output
    """
    onc_ob = onc(args.token)
    df = list_file(onc_ob, deviceCode=args.deviceCode, deviceId=args.deviceId,
        locationCode=args.locationCode, dive=args.dive, deviceCategoryCode=args.deviceCategoryCode,
        dateFrom=args.dateFrom, dateTo=args.dateTo, quality=args.quality,
        extension=args.extension, statistics=args.statistics)
    if args.statistics:
        df['duration'] = df['duration'].dt.total_seconds().apply(strftd)
    df.to_csv(args.output, index=False)


def fbatch(args):
    """
    use list_file_batch and save output
    """
    onc_ob = onc(args.token)
    df = list_file_batch(onc_ob, args.csvfile, quality=args.quality, extension=args.extension,
                         statistics=args.statistics)
    if args.statistics:
        df['duration'] = df['duration'].dt.total_seconds().apply(strftd)
    df.to_csv(args.output, index=False)


def fgetdives(args):
    """
    use get_dives and save output
    """
    onc_ob = onc(args.token)
    df = get_dives(onc_ob, False)
    df.to_csv(args.output, index=False)


def finfo(args):
    """
    use get_dives and save output
    """
    video_info(args.source, args.output, args.interlaced)


def fdidson(args):
    """
    run didson_info function
    """
    didson_info(args.source, args.output)


def fdownload(args):
    """
    run download_files function
    """
    download_files(args.source, args.output, args.trim)


def fextframe(args):
    """
    run extract_frame function
    """
    extract_frame(args.source, args.interval, args.output,
                  args.trim, args.deinterlace, args.rounding_near)


def ftomp4(args):
    """
    use get_dives and save output
    """
    to_mp4(args.source, args.output, args.trim,
           args.deinterlace, args.target_quality,
           args.keep_audio, args.yuv420, args.h265)


def fextfov(args):
    """
    run extract_fov function
    """
    if args.timestamps is not None:
        args.timestamps = args.timestamps.split(",")
    extract_fov(args.source, args.timestamps, args.clip_or_sharpest,
                args.duration, args.output, args.deinterlace)


def fdownloadts(args):
    """
    run download_ts function
    """
    onc_ob = onc(args.token)
    args.deviceCategoryCode = args.deviceCategoryCode.split(",")
    download_ts(onc_ob, args.source, args.deviceCategoryCode, args.output,
        args.options)


def fmergets(args):
    """
    run merge_ts function
    """
    out = merge_ts(args.source, args.ts_data, args.tolerance, args.data_search)
    out.to_csv(args.output, index=False, na_rep='NA')


def fdownloadst(args):
    """
    run download_st function
    """
    onc_ob = onc(args.token)
    df = download_st(onc_ob, args.url, args.extension)
    if args.url.endswith('.csv'):
        df.to_csv("videos_seatube.csv", index=False)
    else:
        print(df['url'])
        print("Frame expected at ", df['video_time'])
        print("File name for the frame: ", df['frame_filename'])


def flinkst(args):
    """
    run link_st function
    """
    onc_ob = onc(args.token)

    df = link_st(onc_ob, args.source)

    if df.shape[0] == 1:
        print(df['url'].iloc[0])
    else:
        df.to_csv(args.output, index=False)


def frenamest(args):
    """
    run rename_st function on multiple files
    """
    path = Path(args.path)
    directory = path.parent
    for f in directory.rglob(path.name):
        newname = rename_st(f.name)
        f.rename(newname)

def fmaketimelapse(args):
    """
    run make_timelapse function
    """
    def point2int(point):
        if point is not None:
            point = point.split(',')
            point = [int(x) for x in point]
        return point

    args.time_xy = point2int(args.time_xy)
    args.caption_xy = point2int(args.caption_xy)
    make_timelapse(args.folder, args.time_display, args.time_format, args.time_offset,
                    args.fps, args.fontSize, args.logo, args.caption, args.time_xy, args.caption_xy)

def falign(args):
    """
    align images
    """
    align_frames(args.folder, args.method, args.reference)


def main(args=None):
    """
    Create parser for arguments
    """
    help_input = "A folder containing video files, or a csv file with list of \
        archived filenames (output of 'list' command)."

    parser = argparse.ArgumentParser(
        description="Commands to list and process videos files archived in Ocean3.0.")
    parser.set_defaults(func=lambda args: parser.print_help())

    subparsers = parser.add_subparsers(title="Valid commands",
        description="For more details on one command: oncvideo <command> -h")

    # List command
    subparser_list = subparsers.add_parser(
        'list', help="List video files for a specific camera between two dates")
    subparser_list.add_argument('-t', '--token', help='API token')
    group_list = subparser_list.add_mutually_exclusive_group(required=True)
    group_list.add_argument(
        '-dc', '--deviceCode', help='Get videos from a specific Device')
    group_list.add_argument(
        '-di', '--deviceId', help='Get videos from a specific DeviceId')
    group_list.add_argument(
        '-lc', '--locationCode', help='Get videos from a specific Location')
    group_list.add_argument('-dive', help='Get videos from a specific Dive')

    subparser_list.add_argument('-dcc', '--deviceCategoryCode', default='VIDEOCAM',
        help="Only used for locationCode. Usually 'VIDEOCAM' for fixed cameras and 'ROV_CAMERA' \
        for ROVs. 'ask' will list available options and ask user to choose one. Default 'VIDEOCAM'")
    subparser_list.add_argument('-from',
        '--dateFrom', help='Return videos after specified datetime. Can be any format that is parsed \
        by pandas.to_datetime. If None, will search all videos since the device \
        was first deployed.')
    subparser_list.add_argument('-to',
        '--dateTo', help='Return videos before specified datetime. Can be any format that is parsed \
        by pandas.to_datetime. If None, will search all videos until the current date.')
    subparser_list.add_argument('-q', '--quality', default='ask',
        help="Quality of the videos to use. Usually should be LOW, 1500, 5000, UHD. 'ask' will \
        list available options and ask user to choose one. 'all' will get all available videos.")
    subparser_list.add_argument('-ext', '--extension', default="mp4",
        help="File extension to search. Default to 'mp4'. 'ask' will list \
        available options and ask user to choose one. 'all' will get all available videos.")
    subparser_list.add_argument('-s', '--statistics', action="store_false",
        help='Do not save video durations and file sizes.')

    subparser_list.add_argument('-o', '--output', default="videos.csv",
                                help="File name to output video filenames. Default 'videos.csv'")
    subparser_list.set_defaults(func=flist)

    # List Batch command
    subparser_blist = subparsers.add_parser(
        'blist', help="List video files based on parameters stored in a csv file.")
    subparser_blist.add_argument('-t', '--token', help='API token')
    subparser_blist.add_argument(
        'csvfile', help='Csv file with arguments to iterate')

    subparser_blist.add_argument('-q', '--quality', default='ask',
        help="Quality of the videos to use. Usually should be LOW, 1500, 5000, UHD. 'ask' will \
        list available options and ask user to choose one. 'all' will get all available videos.")
    subparser_blist.add_argument('-ext', '--extension', default="mp4",
        help="File extension to search. Default to 'mp4'. 'ask' will list \
        available options and ask user to choose one. 'all' will get all available videos.")
    subparser_blist.add_argument('-s', '--statistics', action="store_false",
        help='Do not save video durations and file sizes.')
    subparser_blist.add_argument('-k', '--keep', action="store_true",
        help='Keep other columns from csvfile into the output.')
    subparser_blist.add_argument('-o', '--output', default="videos.csv",
        help="File name to output video filenames. Default 'videos.csv'")
    subparser_blist.set_defaults(func=fbatch)

    # get dives
    subparser_dives = subparsers.add_parser(
        'getDives', help="Create a csv file listing dives from Oceans3.0")
    subparser_dives.add_argument('-t', '--token', help='API token')
    subparser_dives.add_argument('-o', '--output', default="dives.csv",
                                 help="File name to output dives. Default 'dives.csv'")
    subparser_dives.set_defaults(func=fgetdives)

    # getInfo
    subparser_info = subparsers.add_parser(
        'info', help="Extract video information (duration, resolution, fps)")
    subparser_info.add_argument('source', help=help_input)
    subparser_info.add_argument('-o', '--output', default="video_info.csv",
        help="File name to write information. Default 'video_info.csv'")
    subparser_info.add_argument('-i', '--interlaced', action="store_true",
        help='Check if video is interlaced or not using the idet filter.')
    subparser_info.set_defaults(func=finfo)

    # getDIDSON
    subparser_didson = subparsers.add_parser(
        'didson', help="Extract information of DIDSON files")
    subparser_didson.add_argument('source', help=help_input)
    subparser_didson.add_argument('-o', '--output', default="DIDSON_info.csv",
        help="File name to write information. Default 'DIDSON_info.csv'")
    subparser_didson.set_defaults(func=fdidson)

    # Download
    subparser_download = subparsers.add_parser(
        'download', help="Download files")
    subparser_download.add_argument(
        'source', help="A csv file with list of archived filenames (output of 'list' command).")
    subparser_download.add_argument('-o', '--output', default="output",
        help="Folder to download files. Default 'output'")
    subparser_download.add_argument('-t', '--trim', action="store_true",
        help='Trim video files to match the initial search query.')
    subparser_download.set_defaults(func=fdownload)

    # Convert to mp4
    subparser_tomp4 = subparsers.add_parser(
        'tomp4', help="Convert video to mp4 format")
    subparser_tomp4.add_argument(
        'source', help=help_input)
    subparser_tomp4.add_argument('-o', '--output', default="output",
        help="Folder to download files. Default 'output'")
    subparser_tomp4.add_argument('-t', '--trim', action="store_true",
        help='Trim video files to match the initial search query.')
    subparser_tomp4.add_argument('-d', '--deinterlace', action="store_true",
        help='Deinterlace video. Default to False.')
    subparser_tomp4.add_argument('-crf', '--target_quality', type=float,
        help='Set CRF (quality level) in ffmpeg.')
    subparser_tomp4.add_argument('-a', '--keep_audio', action="store_true",
        help='Keep audio in the video.')
    subparser_tomp4.add_argument('-y', '--yuv420', action="store_true",
        help='Force YUV420 color space.')
    subparser_tomp4.add_argument('-p', '--h265', action="store_true",
        help='Use H.265 encoding instead of H.264.')
    subparser_tomp4.set_defaults(func=ftomp4)

    # extract Frame
    subparser_extframe = subparsers.add_parser(
        'extframe', help="Extract frames from video files")
    subparser_extframe.add_argument('source', help=help_input)
    subparser_extframe.add_argument('interval', type=float,
        help="Get frames every 'X' seconds. Default to 1 second.")
    subparser_extframe.add_argument('-o', '--output', default="frames",
        help="Folder to download frames. Default 'frames'")
    subparser_extframe.add_argument('-t', '--trim', action="store_true",
        help='Trim video files to match the initial search query.')
    subparser_extframe.add_argument('-d', '--deinterlace', action="store_true",
        help='Deinterlace video. Default to False.')
    subparser_extframe.add_argument('-n', '--rounding_near', action="store_true",
        help='Use ffmpeg default Timestamp rounding method (near) for fps filter.\
        Default to False (stills start in the beginning of the video).')
    subparser_extframe.set_defaults(func=fextframe)

    # extract FOV
    subparser_extframe = subparsers.add_parser(
        'extfov', help="Extract FOVs (frames or videos) from video files")
    subparser_extframe.add_argument('source', help=help_input)
    subparser_extframe.add_argument('-s', '--timestamps',
        help="Get frames at the specific timestamps, in seconds or mm:ss.f format.\
        Can be a comma separated list to extract multiple FOVs.\
        If 'durations' is supplied, will extract clips starting at each timestamp or get \
        the sharpest frame within the duration.")
    subparser_extframe.add_argument('-c', '--clip_or_sharpest', default='sharpest',
        help=" Either 'clip' or 'sharpest'. If 'clip', the function will save clips instead of framegrabs,\
        If 'sharpest', will save the sharpest frame only within the clip. Only usd if durations is supplied.")
    subparser_extframe.add_argument('-t', '--duration', required=False,
        help="Duration of the FOVs to download, in seconds or mm:ss.f format.")
    subparser_extframe.add_argument('-o', '--output', default="fovs",
        help="Folder to download files. Default 'fovs'")
    subparser_extframe.add_argument('-d', '--deinterlace', action="store_true",
        help='Deinterlace video before getting frame. Default to False.')
    subparser_extframe.set_defaults(func=fextfov)

    # download time series
    subparser_downloadts = subparsers.add_parser(
        'downloadTS', help="Donwload timeseries data that corresponds to the same \
        time period as the video files")
    subparser_downloadts.add_argument('source', help=help_input)
    subparser_downloadts.add_argument('deviceCategoryCode',
        help="Category Code of data to download. E.g. NAV, CTD, OXYSENSOR, etc. \
        Can be a comma separated list.")
    subparser_downloadts.add_argument('-t', '--token', help='API token')
    subparser_downloadts.add_argument('-o', '--output', default="output",
        help="Name of the output folder to save files. Default 'output'")
    subparser_downloadts.add_argument('-p', '--options', choices=['fixed','rov'], default="fixed",
        help="Set options for search querry. If 'fixed', return clean resampled data \
        for every minute, and maximum gap of one day between queries. \
        If 'rov', return raw (not resampled) data, and set a maximum gap of one hour between queries.")
    subparser_downloadts.set_defaults(func=fdownloadts)

    # merge time series
    subparser_mergets = subparsers.add_parser(
        'mergeTS', help="Merge timestamps from source and retrive the \
        closest data avaiable inside the ts_data folder")
    subparser_mergets.add_argument('source', help=help_input)
    subparser_mergets.add_argument('ts_data', help="Folder containg csv files of TSSD \
        downloaded from Oceans 3.")
    subparser_mergets.add_argument('-o', '--output', default="merged.csv",
        help="Name of the merged file. Default 'merged.csv'")
    subparser_mergets.add_argument('-t', '--tolerance', type=float, default=15,
        help="Tolarance, in seconds, for timestamps to be merged. Default to 15.")
    subparser_mergets.add_argument('-d', '--data_search', action="store_true",
        help="Read data downloaded from the Data Search webpage.")
    subparser_mergets.set_defaults(func=fmergets)

    # download video from Seatube
    subparser_downloadst = subparsers.add_parser(
        'downloadST', help="Generate download link for the correspoding video based on the Seatube link.")
    subparser_downloadst.add_argument('url',
        help="The link generated by Seatube V3 or csv file with 'seatube_link' column.")
    subparser_downloadst.add_argument('-t', '--token', help='API token')
    subparser_downloadst.add_argument('-e', '--extension', default="mov",
        help="File extension to download video. Default to 'mov'")
    subparser_downloadst.set_defaults(func=fdownloadst)

    # generate link for Seatube
    subparser_linkst = subparsers.add_parser(
        'linkST', help="Generate a Seatube link from filenames following the Oceans 3 naming \
        convention. For now, only supports video avaiable in Seatube V3.")
    subparser_linkst.add_argument('source', help=help_input)
    subparser_linkst.add_argument('-t', '--token', help='API token')
    subparser_linkst.add_argument('-o', '--output', default='output_link.csv',
        help="Output file to save results. Default to 'output_link.csv'")
    subparser_linkst.set_defaults(func=flinkst)

    # rename framegraps from Seatube
    subparser_renamest = subparsers.add_parser(
        'renameST', help="Rename framegrabs from Seatube to correct timestamp.")
    subparser_renamest.add_argument('path', help="Path to a file, or a Glob pattern to match \
        multiple files (use *).")
    subparser_renamest.set_defaults(func=frenamest)

    # Generate timelapse video from images
    subparser_maketimelapse = subparsers.add_parser(
        'timelapse', help="Generate timelapse video from images")
    subparser_maketimelapse.add_argument('folder', default="fovs",
        help="Path to a folder where .jpg images are stored. Default 'fovs'.")
    subparser_maketimelapse.add_argument('-t', '--time_display', default="elapsed",
            help="How to print the time on the frame. 'elapsed' will display as elapsed time since first \
        frame, offset by 'time_offset'. 'current' will display the current real time of the frame. \
        'none' will not display time.")
    subparser_maketimelapse.add_argument('-f', '--time_format',
        help="Format how the timestamp will be writen on the video. For time_display='current', check formating \
        options for 'strftime'. For time_display='elapsed', options are %%y %%m %%w %%d %%H %%M %%S for years, months, \
        weeks, days, hours, minutes, seconds. Default '%%Y/%%m/%%d %%Hh' if time_display='current', and '%%d days %%{H}h' \
        if time_display='elapsed'")
    subparser_maketimelapse.add_argument('-o', '--time_offset', default=0,
        help="Offset the time displayed in the frame if time_display='elapsed'. \
        Passed to pd.to_timedelta, check it's documentation for options.")
    subparser_maketimelapse.add_argument('-r', '--fps', type=float, default=10,
        help="Timelapse video FPS. Default 10.")
    subparser_maketimelapse.add_argument('-e', '--fontSize', type=float, default=44,
        help="Font scale for the timestamp. Default 44.")
    subparser_maketimelapse.add_argument('-l', '--logo', action="store_true",
        help="Include ONC logo on the video.")
    subparser_maketimelapse.add_argument('-c', '--caption',
        help="Insert a caption at the bottom of the screen.")
    subparser_maketimelapse.add_argument('--time_xy',
        help="Coordinates of the bottom-left corner of the time text. Must be two ints separated by comma")
    subparser_maketimelapse.add_argument('--caption_xy',
        help="Coordinates of the bottom-left corner of the caption. Must be two ints separated by comma.")
    subparser_maketimelapse.set_defaults(func=fmaketimelapse)


    # Align frames
    subparser_align = subparsers.add_parser(
        'align', help="Align frames")
    subparser_align.add_argument('folder', default="fovs",
        help="Path to a folder where .jpg images are stored. Default 'fovs'.")
    subparser_align.add_argument('-m', '--method', choices=['ORB', 'ECC', 'ORB+ECC'], default="ORB+ECC",
        help="Algorithm used for alignment: Feature Matching (ORB), ECC Image Alignment, or both.")
    subparser_align.add_argument('-r', '--reference', default="middle",
        help="Define the reference frame which other frames will be aligned to. Can be \
            'first', 'middle', 'last', 'previousX' or filename of the image to be used. Default 'middle'.")
    subparser_align.set_defaults(func=falign)

    args = parser.parse_args(args)
    args.func(args)


if __name__ == '__main__':
    main()
