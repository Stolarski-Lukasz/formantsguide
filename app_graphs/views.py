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


def create_spectrogram(request: HttpRequest):

    # obtaining user data
    cardinal_vowel_str = request.GET.get("cardinal_vowel")[2:]
    cardinal_vowel_int = int(cardinal_vowel_str)
    gender = request.GET.get("phonetician-group")
    window_length = request.GET.get("window-length")
    if window_length == "custom":
        window_length = float(request.GET.get("window-length-input"))
        if window_length > 0.1:
            return JsonResponse({"incorrect_window_length": True})
    show_formants = request.GET.get("show-formants")
    show_F3 = request.GET.get("show-f3")
    add_title = request.GET.get("add-title")
    dynamic_range_initial = request.GET.get("dynamic-range")
    dynamic_range_int = int(float(dynamic_range_initial))
    dynamic_range_str = str(dynamic_range_int)
    db_coeff_str = request.GET.get("db-coefficient")
    db_coeff_int = int(request.GET.get("db-coefficient"))
    colour_scheme = request.GET.get("colour-scheme")
    phoneticians = request.GET.getlist("phoneticians")


    # adjusting user data
    if cardinal_vowel_int < 10:
        cardinal_vowel_str = "0" + str(cardinal_vowel_int)
    else:
        cardinal_vowel_str = str(cardinal_vowel_int)

    try:
    # creating variables based on user data
        if gender == "male":
            folder_or_listofpaths = BASE_DIR + "/data/cardinal_vowels_for_analysis_m/"
            formant_measurements_df = pd.read_table(
                BASE_DIR + "/data/male_means.tsv")
            
            phoneticians_selected = Phonetician.objects.filter(gender="m")
            recordings_found = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int)
            phoneticians_found = Phonetician.objects.filter(recording__in=recordings_found)
            phoneticians_found_list = []
            for query_set in phoneticians_found:
                phoneticians_found_list.append(query_set.official_name)

        elif gender == "female":
            folder_or_listofpaths = BASE_DIR + "/data/cardinal_vowels_for_analysis_f/"
            formant_measurements_df = pd.read_table(
                BASE_DIR + "/data/female_means.tsv")

            phoneticians_selected = Phonetician.objects.filter(gender="f")
            recordings_found = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int)
            phoneticians_found = Phonetician.objects.filter(recording__in=recordings_found)
            phoneticians_found_list = []
            for query_set in phoneticians_found:
                phoneticians_found_list.append(query_set.official_name)

        elif gender == "selected":
            phoneticians_selected = Phonetician.objects.filter(name__in=phoneticians)
            recordings_found = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int)
            # TODO - nie rozumiem co to jest recording__in - tego nie ma ani w jednej ani w drugie tabeli... - to jest co najwyżej nazwa z jednej z tabel
            # TODO - wyjaśnić to kiedyś...
            phoneticians_found = Phonetician.objects.filter(recording__in=recordings_found)
            # print("phoneticians_found", phoneticians_found)
            phoneticians_found_list = []
            for query_set in phoneticians_found:
                phoneticians_found_list.append(query_set.official_name)
            # print("phoneticians_found_list", phoneticians_found_list)
            # official_names_list = phoneticians_found.values_list('official_name', flat=True)
            # print("official names", official_names_list)
            folder_or_listofpaths = []
            for recording in recordings_found:
                folder_or_listofpaths.append(recording.path)
            print("folder_or_listofpaths", folder_or_listofpaths)
            f1 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f1'))
            f1 = int(f1["f1__avg"])
            f2 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f2'))
            f2 = int(f2["f2__avg"])
            f3 = Recording.objects.filter(phonetician__in=phoneticians_selected, vowel=cardinal_vowel_int).aggregate(Avg('f3'))
            f3 = int(f3["f3__avg"])

        # I define formants twice because formants list is needed as an argument to funcitons below, 
        # and then I need formants values in the return object independently if the list exists or not
        if show_formants == "on":
            if gender == "selected":
                formants = [f1, f2, f3]
            else:
                formants = [formant_measurements_df["f1"][cardinal_vowel_int-1],
                            formant_measurements_df["f2"][cardinal_vowel_int-1],
                            formant_measurements_df["f3"][cardinal_vowel_int-1]]
        else:
            formants = None

        if gender != "selected":
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

        # creating graphs
        batch_acoustic_data_processor = BatchAcousticDataProcessor()
        if gender == "selected":
            batch_acoustic_data_processor.get_average_bin_values_listofpaths(listofpaths=folder_or_listofpaths,
                                                            cardinal_vowel=cardinal_vowel_str,
                                                            window_length=window_length,
                                                            output_data_type="spectrogram_and_spectrum")
        else:
            batch_acoustic_data_processor.get_average_bin_values(folder_name=folder_or_listofpaths,
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
                            "f3": f3,
                            "sample_size": batch_acoustic_data_processor.sample_size,
                            "phoneticians_found": phoneticians_found_list
                            })
    except TypeError:
        return JsonResponse({"spectrum_path_and_name": None,
                            "spectrogram_path_and_name": None,
                            "f1": None,
                            "f2": None,
                            "f3": None
                            })


def create_spectrum_slice(request):
    pass
