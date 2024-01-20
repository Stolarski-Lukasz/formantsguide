from django.shortcuts import render
from .my_parselmouth import BatchAcousticDataProcessor
from .my_acoustic_graphs import ParselmouthSpectrogramGrapher, ParselmouthSpectrumGrapher
import os
import pandas as pd
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpRequest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_spectrogram(request: HttpRequest):

    # obtaining user data
    cardinal_vowel_str = request.GET.get("cardinal_vowel")[2:]
    cardinal_vowel_int = int(cardinal_vowel_str)
    gender = request.GET.get("phonetician-group")
    window_length = request.GET.get("window-length")
    show_formants = request.GET.get("show-formants")
    show_F3 = request.GET.get("show-f3")
    print("here we go", show_F3)
    add_title = request.GET.get("add-title")
    # TODO - correct mistakes when the user inputs a float
    dynamic_range_str = request.GET.get("dynamic-range")
    dynamic_range_int = int(request.GET.get("dynamic-range"))
    db_coeff_str = request.GET.get("db-coefficient")
    db_coeff_int = int(request.GET.get("db-coefficient"))
    colour_scheme = request.GET.get("colour-scheme")
    phoneticians = request.GET.getlist("phoneticians")

    # adjusting user data
    if window_length == "custom":
        window_length = float(request.GET.get("window-length-input"))

    if cardinal_vowel_int < 10:
        cardinal_vowel_str = "0" + str(cardinal_vowel_int)
    else:
        cardinal_vowel_str = str(cardinal_vowel_int)

    # creating variables based on user data
    if gender == "male":
        audio_folder_name = BASE_DIR + "/data/cardinal_vowels_for_analysis_m/"
        formant_measurements_df = pd.read_table(
            BASE_DIR + "/data/male_means.tsv")
    elif gender == "female":
        audio_folder_name = BASE_DIR + "/data/cardinal_vowels_for_analysis_f/"
        formant_measurements_df = pd.read_table(
            BASE_DIR + "/data/female_means.tsv")
    elif gender == "custom":
        audio_folder_name = BASE_DIR + "/data/cardinal_vowels_for_analysis/"
        formant_measurements_df = pd.read_table(
            BASE_DIR + "/data/all_means.tsv")

    # I define formants twice because formants list is needed as an argument to funcitons below, 
    # and then I need formants values in the return object independently if the list exists or not
    if show_formants == "on":
        formants = [formant_measurements_df["f1"][cardinal_vowel_int-1],
                    formant_measurements_df["f2"][cardinal_vowel_int-1],
                    formant_measurements_df["f3"][cardinal_vowel_int-1]]
    else:
        formants = None

    f1 = int(formant_measurements_df["f1"][cardinal_vowel_int-1])
    f2 = int(formant_measurements_df["f2"][cardinal_vowel_int-1])
    f3 = int(formant_measurements_df["f3"][cardinal_vowel_int-1])

    if show_F3 == "on":
        show_f3_state = True
    else:
        show_f3_state = False

    if add_title == "on":
        title = True
    else:
        title = False

    if colour_scheme == "black-on-white":
        colour_scheme = "Greys"
    elif colour_scheme == "white-on-black":
        colour_scheme = "bone"
    elif colour_scheme == "flames":
        colour_scheme = "afmhot"

    # other settings
    save = True
    spectrogram_save_folder = BASE_DIR + "/media/spectrograms/"
    spectrum_save_folder = BASE_DIR + "/media/spectrums/"
    time_stamp = datetime.now().strftime('%Y_%m_%d %H_%M_%S_%f')
    time_stamp = time_stamp.replace(' ', '_')
    spectrogram_save_name = "CV_" + cardinal_vowel_str + "_" + gender + "_" + "dynrange" + dynamic_range_str + \
        "_" + "dbcoeff" + db_coeff_str + "_" + "average_spectrogram" + "_" + time_stamp
    spectrum_save_name = "CV_" + cardinal_vowel_str + "_" + gender + "_" + "dynrange" + dynamic_range_str + \
        "_" + "dbcoeff" + db_coeff_str + "_" + "average_spectrum" "_" + time_stamp

    # creating spectrograms
    # parselmouth_spectrogram_grapher = ParselmouthSpectrogramGrapher()
    # parselmouth_spectrogram_grapher.get_average_spectrogram_values(folder_name=audio_folder_name,
    #                                                             cardinal_vowel=cardinal_vowel_str,
    #                                                             window_length=window_length)
    # parselmouth_spectrogram_grapher.draw_average_spectrogram(formants=formants,
    #                                                          colour_scheme=colour_scheme,
    #                                                         dynamic_range=dynamic_range_int,
    #                                                         db_coeff=db_coeff_int,
    #                                                         save=save,
    #                                                         save_name=save_name,
    #                                                         save_folder=save_folder,
    #                                                         title=title)
    batch_acoustic_data_processor = BatchAcousticDataProcessor()
    batch_acoustic_data_processor.get_average_bin_values(folder_name=audio_folder_name,
                                                         cardinal_vowel=cardinal_vowel_str,
                                                         window_length=window_length,
                                                         output_data_type="spectrogram_and_spectrum")

    parselmouth_spectrum_grapher = ParselmouthSpectrumGrapher()
    parselmouth_spectrum_grapher.draw_average_spectrum(Y=batch_acoustic_data_processor.Y,
                                                       average_spectrum_values=batch_acoustic_data_processor.average_spectrum_values,
                                                       cardinal_vowel=batch_acoustic_data_processor.cardinal_vowel,
                                                       sample_size=batch_acoustic_data_processor.sample_size,
                                                       window_length=batch_acoustic_data_processor.window_length,
                                                       formants=formants,
                                                       show_f3=show_f3_state,
                                                       db_coeff=db_coeff_int,
                                                       save=save,
                                                       save_name=spectrum_save_name,
                                                       save_folder=spectrum_save_folder,
                                                       title=title)

    parselmouth_spectrogram_grapher = ParselmouthSpectrogramGrapher()
    parselmouth_spectrogram_grapher.draw_average_spectrogram(Y=batch_acoustic_data_processor.Y,
                                                             average_spectrogram_values=batch_acoustic_data_processor.average_spectrogram_values,
                                                             cardinal_vowel=batch_acoustic_data_processor.cardinal_vowel,
                                                             sample_size=batch_acoustic_data_processor.sample_size,
                                                             window_length=batch_acoustic_data_processor.window_length,
                                                             formants=formants,
                                                             show_f3=show_f3_state,
                                                             colour_scheme=colour_scheme,
                                                             dynamic_range=dynamic_range_int,
                                                             db_coeff=db_coeff_int,
                                                             save=save,
                                                             save_name=spectrogram_save_name,
                                                             save_folder=spectrogram_save_folder,
                                                             title=title)

    return JsonResponse({"spectrum_path_and_name": "/media/spectrums/" + spectrum_save_name + ".png",
                         "spectrogram_path_and_name": "/media/spectrograms/" + spectrogram_save_name + ".png",
                         "f1": f1,
                         "f2": f2,
                         "f3": f3
                         })


def create_spectrum_slice(request):
    pass
