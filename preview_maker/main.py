import random
import pathlib
from moviepy.video.io import VideoFileClip
import moviepy.editor as mp


def mini_clips_times(count, start_range, end_range):
    """
    This function will return {count} number of mini clips start and end times as tuples in a list
    :param count: number of mini clips
    :param start_range: start range
    :param end_range: end range
    :return: [(start,end),...]
    """
    ranges = []
    miniRangesDurations = (end_range - start_range)/count
    for i in range(count):
        k = random.randrange(start_range + (i*miniRangesDurations),start_range +  (i*miniRangesDurations) +miniRangesDurations )
        ranges.append(
            (k,k+5)
        )
    return ranges

def check_file_exists(path):
    return pathlib.Path(path).exists()

def generate_full_vieo_object(filepath):
    return VideoFileClip.VideoFileClip(filepath)

def generate_mini_clips_objects_array(VideoFile, clipsTimeRanges):
    return [VideoFile.subclip(startTime, endTime) for startTime, endTime in clipsTimeRanges]

def generate_fade_effect_between_clips(clipsObjects, fadeTime):
    return [clip.crossfadein(fadeTime) for clip in clipsObjects]

def generate_preview(filePath, startRange, endRange, introRange=None, outroRange= None,miniClipsCount=3, fadeEffectBetweenClips= 1, fadeEffectPadding = -0.5):
    """
    This function will export generated preview as mp4 next to input path.
    :param filePath: input video path
    :param startRange: mini clips start range
    :param endRange: mini clips end range
    :param introRange: if you want to include intro at the first of preview, enter as : [startRange,endRange]
    :param outroRange: if you want to include outro at the end of preview, enter as : [startRange,endRange]
    :param miniClipsCount: How many mini clips it should have
    :return: Boolean
    """
    assert check_file_exists(filePath), 'pyPreviewBaker => Error, file does not exist'

    clipsTimeRanges = []

    if introRange:
        clipsTimeRanges.append(tuple(introRange))

    miniClips = mini_clips_times(count= miniClipsCount, start_range= startRange, end_range= endRange)

    assert miniClips, 'pyPreviewBaker => Error in generating random mini clips timings, check your range and try again.'

    clipsTimeRanges.extend(miniClips)

    if outroRange:
        clipsTimeRanges.append(tuple(outroRange))

    try:
        fullVideo = generate_full_vieo_object(filePath)
    except:
        print('pyPreviewBaker => Can\'t open input video clip, check and try again.')
        return False
    else:
        print('pyPreviewBaker => Opening input video was successful')

    miniClipsVideos = generate_mini_clips_objects_array(fullVideo, clipsTimeRanges= clipsTimeRanges)

    if fadeEffectBetweenClips:
        clipsFinal = generate_fade_effect_between_clips(clipsObjects=miniClipsVideos, fadeTime=fadeEffectBetweenClips)
    else:
        clipsFinal = miniClipsVideos

    try:
        print('concatenating clips')
        concat_clip = mp.concatenate_videoclips(clipsFinal,
                                                method="compose",
                                                padding = fadeEffectPadding if fadeEffectBetweenClips else 0)
    except:
        print('pyPreviewBaker => mixing mini clips went wrong, please check your ranges and try again')
        return False
    else:
        print('pyPreviewBaker => mixed mini clips successfully')

    try:
        concat_clip.write_videofile(str(pathlib.Path(filePath).parent.joinpath('preview.mp4')))
    except Exception as msg:
        print('pyPreviewBaker => Writing export .mp4 file went wrong',msg)
        return False
    else:
        print('pyPreviewBaker => Export finished successfully.')
    return True
