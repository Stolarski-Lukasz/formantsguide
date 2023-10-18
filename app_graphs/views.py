from django.shortcuts import render
from .my_acoustic_graphs import ParselmouthSpectrogramGrapher
import os
import pandas as pd
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpRequest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_spectrogram(request: HttpRequest):

    # User data
    ###########
    gender = request.GET.get("phonetician_group")
    print(gender)
    cardinal_vowel_str = request.GET.get("cardinal_vowel")[2:]
    print(cardinal_vowel_str)
    # userform_gender = request.GET.getlist("userform_gender")
    # userform_age = request.GET.getlist("userform_age")
    # userform_education = request.GET.getlist("userform_education")
    # userform_proficiency = request.GET.getlist("userform_proficiency")
    # userform_concordance_window_size = int(request.GET.get("userform_concordance_window_size"))

    print("django responds")
    # gender = "male"
    # cardinal_vowel_int = 9
    window_length = "broadband"
    # low contrast - low dynamic_range (30) and low db_coeff (5)
    # high contrast - high dynamic_range (70) and high db_coeff (10)
    # the higher the darker
    dynamic_range = 30
    # the lower the darker
    db_coeff = 7
    save = True
    save_folder = BASE_DIR + "/media/spectrograms/"
    title = False

    time_stamp = datetime.now().strftime('%Y_%m_%d %H_%M_%S_%f')
    time_stamp = time_stamp.replace(' ', '_')


    # if cardinal_vowel_int < 10:
    #     cardinal_vowel_str = "0" + str(cardinal_vowel_int)
    # else:
    #     cardinal_vowel_str = str(cardinal_vowel_int)
    save_name = cardinal_vowel_str + "_" + gender + "_" + "dynrange" + str(dynamic_range) + "_" + "dbcoeff" + str(db_coeff) + "_" + time_stamp
    if gender == "male":
        audio_folder_name = "/media/luke/WORK/Current Projects/cardinal_vowels_for_analysis_m/"
        formant_measurements_df = pd.read_table(BASE_DIR + "/data/male_means.tsv")
    elif gender == "female":
        audio_folder_name = "/media/luke/WORK/Current Projects/cardinal_vowels_for_analysis_f/"
        formant_measurements_df = pd.read_table("female_means.tsv")

    parselmouth_spectrogram_grapher = ParselmouthSpectrogramGrapher()
    parselmouth_spectrogram_grapher.get_average_spectrogram_values(folder_name=audio_folder_name,
                                                                cardinal_vowel=cardinal_vowel_str, 
                                                                window_length=window_length)
    parselmouth_spectrogram_grapher.draw_average_spectrogram(formants=[formant_measurements_df["f1"][cardinal_vowel_int-1], 
                                                                    formant_measurements_df["f2"][cardinal_vowel_int-1], 
                                                                    formant_measurements_df["f3"][cardinal_vowel_int-1]],
                                                                    dynamic_range=dynamic_range,
                                                                    db_coeff=db_coeff,
                                                                    save=save,
                                                                    save_name=save_name,
                                                                    save_folder=save_folder,
                                                                    title=title)
        
    return JsonResponse({'resulting_audio_file': "something"})




def create_spectrum_slice(request):
    pass
