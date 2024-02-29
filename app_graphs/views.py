from django.shortcuts import render
from .my_parselmouth import BatchAcousticDataProcessor
from .my_acoustic_graphs import ParselmouthSpectrogramGrapher, ParselmouthSpectrumGrapher
import os
import pandas as pd
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpRequest
from app_databasecreation.models import Phonetician, Recording
from django.db.models import Q
from django.db.models import Avg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_graphs(request: HttpRequest):

    # obtaining user data
    cardinal_vowel_str = request.GET.get("cardinal_vowel")[2:]
    cardinal_vowel_int = int(cardinal_vowel_str)
    gender = request.GET.get("phonetician-group")
    window_length = request.GET.get("window-length")
    if window_length == "custom":
        window_length = float(request.GET.get("window-length-input"))
        if window_length > 0.1 or window_length < 0.0005:
            return JsonResponse({"incorrect_window_length": True})
    show_formants = request.GET.get("show-formants")
    show_F3 = request.GET.get("show-f3")
    add_title = request.GET.get("add-title")
    z_score_normalization = request.GET.get("normalize-power")
    dynamic_range_initial = request.GET.get("dynamic-range")
    dynamic_range_int = 50
    dynamic_range_str = "50"
    db_coeff_str = "10"
    db_coeff_int = 10
    if dynamic_range_initial != None:
        dynamic_range_int = int(float(dynamic_range_initial))
        dynamic_range_str = str(dynamic_range_int)
        db_coeff_str = request.GET.get("db-coefficient")
        db_coeff_int = int(request.GET.get("db-coefficient"))
    colour_scheme = request.GET.get("colour-scheme")
    phoneticians = request.GET.getlist("phoneticians")
    print("phoneticians", phoneticians)

    # processing user data
    if cardinal_vowel_int < 10:
        cardinal_vowel_str = "0" + str(cardinal_vowel_int)
    else:
        cardinal_vowel_str = str(cardinal_vowel_int)

    phoneticians_selected = Phonetician.objects.filter(name__in=phoneticians)
    recordings_found = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int)
    phoneticians_found = Phonetician.objects.filter(recording__in=recordings_found)
    if len(phoneticians_found) == 0:
        return JsonResponse({"recordings_not_available": True})
    phoneticians_found_list = []
    for query_set in phoneticians_found:
        phoneticians_found_list.append(query_set.official_name)
    files_list = []
    for recording in recordings_found:
        files_list.append(BASE_DIR + "/" + recording.path)

    f1 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f1'))
    f1 = int(f1["f1__avg"])
    f2 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f2'))
    f2 = int(f2["f2__avg"])
    f3 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f3'))
    f3 = int(f3["f3__avg"])

    if show_formants == "on":
        formants = [f1, f2, f3]
    else:
        formants = None

    if show_F3 == "on":
        show_f3_state = True
    else:
        show_f3_state = False

    if add_title == "on":
        title = True
    else:
        title = False
    
    if z_score_normalization == "on":
        z_score_normalization = True
    else:
        z_score_normalization = False

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

    # creating graphs
    batch_acoustic_data_processor = BatchAcousticDataProcessor()
    batch_acoustic_data_processor.get_average_bin_values(files_list=files_list,
                                                        cardinal_vowel=cardinal_vowel_str,
                                                        z_score_normalization=z_score_normalization,
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
                                                    z_score_normalization=z_score_normalization,
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
                                                            z_score_normalization=z_score_normalization,
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
                        "f3": f3,
                        "sample_size": batch_acoustic_data_processor.sample_size,
                        "phoneticians_found": phoneticians_found_list
                        })

