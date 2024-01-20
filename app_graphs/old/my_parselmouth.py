import parselmouth
from parselmouth.praat import call
import pickle
import pandas as pd
import math
from scipy.stats.mstats import gmean
import io



def get_spectrogram_object(sound_file, window_length="broadband"):
    """
    Args:
        sound_file (.wav audio file): a recording of a vowel in the .wav format.
        window_length (str or float, optional): Defaults to "broadband". Use "narrowband" for a narrowband spectrogram, or supply a float value for a custom window length.

    Returns: Parcelmouth spectrogram object
    """
    if window_length == "broadband":
        window_length = 0.005
    elif window_length == "narrowband":
        window_length = 0.03
    sound = parselmouth.Sound(sound_file)
    spectrogram_object = sound.to_spectrogram(window_length=window_length, 
                                       time_step=0.0001, 
                                       frequency_step=1)
    return spectrogram_object


def get_spectrum_slice_df(spectrogram_object, time_point=0):
    """
    This function is suboptimal - it is only for a specific time point . For "average spectrum values" across whole duration, use "get_average_spectrum_values"

    Args:
        spectrogram_object (Parcelmouth spectrogram object)

    Returns:
        dataframe: spectrum slice values for a given time point in a spectrogram
    """
    spectrum_slice_object = spectrogram_object.to_spectrum_slice(time_point)
    spectrum_slice_list = call(spectrum_slice_object, "List", "no", "yes", "no", "no", "no", "yes")
    # this changes the spectrum_slice_list variable into something that pandas can read
    buffer = io.StringIO(spectrum_slice_list)
    spectrum_slice_df = pd.read_table(buffer)
    # * I also obtained the same by saving the variable to a tsv file and then reading it normally
    # with open('spectrum_slice_list.tsv', 'w') as out:
    #     out.write(spectrum_slice_list)
    # spectrum_slice_df = pd.read_table("spectrum_slice_list.tsv")
    return spectrum_slice_df


def get_spectral_traits(sound_file, gender):
    """
    Args:
        sound_file (.wav audio file): a recording of a vowel in the .wav format.
        gender (str): "m" for male speaker and "f" for female speaker

    Returns:
        list: F0  and the first 3 formants. Also, basic Praat settings are returned as a string.
    """
    results = []
    if gender == "m":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 75, 300)
        f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
        formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        # f4_mean = call(formants, "Get mean", 4, 0, 0, "hertz")
        results = [f0_mean, f1_mean, f2_mean, f3_mean, "settings 5 5000"]
    elif gender == "f":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 100, 500)
        f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
        formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        # f4_mean = call(formants, "Get mean", 4, 0, 0, "hertz")
        results = [f0_mean, f1_mean, f2_mean, f3_mean, "settings 5 5500"]
    return results


def get_spectral_traits_smart(sound_file, gender):
    """
    The same as "get_spectral_traits", but uses pcv_gpclassifier to optimize settings for high-back articulations by men

    Args:
        sound_file (.wav audio file): a recording of a vowel in the .wav format.
        gender (str): "m" for male speaker and "f" for female speaker

    Returns:
        list: F0  and the first 3 formants. Also, basic Praat settings are returned as a string.
    """
    results = []
    if gender == "m":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 75, 300)
        f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
        formants = call(sound, "To Formant (burg)", 0, 6, 5000, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        sr = (f0_mean / 168) ** (1 / 3) * 168
        y = math.log10(f1_mean / sr)
        z = math.log10(f2_mean / f1_mean)
        x = math.log10(f3_mean / f2_mean)

        open_object = open("pcv_gpclassifier.pickle", "rb")
        pcv_gpclassifier = pickle.load(open_object)  # the object will be stored as "classifier"
        open_object.close()

        df = pd.DataFrame({"y": [y],
                           "z": [z],
                           "x": [x]})

        vowel_classification = pcv_gpclassifier.predict(df[['y', 'z', 'x']])

        if vowel_classification[0] == "cv_7" or vowel_classification[0] == "cv_8":
            results = [f0_mean, f1_mean, f2_mean, f3_mean, "settings 6 5000"]
        else:
            formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
            f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
            f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
            f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
            results = [f0_mean, f1_mean, f2_mean, f3_mean, "settings 5 5000"]
    elif gender == "f":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 100, 500)
        f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
        formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        results = [f0_mean, f1_mean, f2_mean, f3_mean, "settings 5 5500"]
    return results


def get_spectral_traits_gmf0(sound_file, gender):
    """
    The same as "get_spectral_traits", but returns geometric mean F0 instead of arithmetic mean F0

    Args:
        sound_file (.wav audio file): a recording of a vowel in the .wav format.
        gender (str): "m" for male speaker and "f" for female speaker

    Returns:
        list: F0  and the first 3 formants. Also, basic Praat settings are returned as a string.
    """
    results = []
    if gender == "m":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 75, 300)
        number_of_frames = call(f0, "Get number of frames")
        pitch_listing = []
        for frame_number in range(1, number_of_frames+1):
            # time = call(f0, "Get time from frame number", frame_number)
            # print(time)
            pitch_in_frame = call(f0, "Get value in frame", frame_number, "Hertz")
            if math.isnan(pitch_in_frame) != True:
                pitch_listing.append(pitch_in_frame)
        f0_gmean = gmean(pitch_listing)
        formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        results = [f0_gmean, f1_mean, f2_mean, f3_mean, "settings 5 5000"]
    elif gender == "f":
        sound = parselmouth.Sound(sound_file)
        f0 = call(sound, "To Pitch", 0, 100, 500)
        number_of_frames = call(f0, "Get number of frames")
        pitch_listing = []
        for frame_number in range(1, number_of_frames+1):
            pitch_in_frame = call(f0, "Get value in frame", frame_number, "Hertz")
            if math.isnan(pitch_in_frame) != True:
                pitch_listing.append(pitch_in_frame)
        f0_gmean = gmean(pitch_listing)
        formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        results = [f0_gmean, f1_mean, f2_mean, f3_mean, "settings 5 5500"]
    return results


def get_millers_coordinates(f0_mean, f1_mean, f2_mean, f3_mean):
    """
    Args:
        f0_mean (float)
        f1_mean (float)
        f2_mean (float)
        f3_mean (float)

    Returns:
        list: Miller's Auditory Perceptual Space coordinates
    """
    sr = (f0_mean / 168) ** (1 / 3) * 168
    log_f1_sr = math.log10(f1_mean / sr)
    log_f2_f1 = math.log10(f2_mean / f1_mean)
    log_f3_f2 = math.log10(f3_mean / f2_mean)
    return [log_f1_sr, log_f2_f1, log_f3_f2]


# the two functions below are for fine-tuning pitch and formant measurements
# ! I have not tested them recently and I am not sure what parselmouth_sound is - it may be just .wav audio file
############################################################################


def get_pitch_ac(sound_file,
                 parselmouth_sound,
                 time_step=0,
                 pitch_floor=75,
                 max_number_of_candidates=15,
                 very_accurate="no",
                 silence_threshold=0.03,
                 voicing_threshold=0.45,
                 octave_cost=0.01,
                 octave_jump_cost=0.35,
                 voiced_unvoiced_cost=0.14,
                 pitch_ceiling=600):
    f0 = call(parselmouth_sound, "To Pitch (ac)", time_step, pitch_floor, max_number_of_candidates, very_accurate,
              silence_threshold, voicing_threshold, octave_cost, octave_jump_cost, voiced_unvoiced_cost, pitch_ceiling)
    f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
    return f0_mean


def get_formants_burg(sound_file,
                      parselmouth_sound,
                      time_step=0,
                      max_number_of_formants=5,
                      maximum_formant=5500,
                      window_length=0.025,
                      pre_emphasis_from=50):
    formants = call(parselmouth_sound, "To Formant (burg)", time_step, max_number_of_formants, maximum_formant,
                    window_length, pre_emphasis_from)
    f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
    f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
    f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
    f4_mean = call(formants, "Get mean", 4, 0, 0, "hertz")
    results = ["empty_place", f1_mean, f2_mean, f3_mean, f4_mean]
    return results
