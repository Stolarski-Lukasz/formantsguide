from my_acoustic_graphs import ParselmouthSpectrumGrapher
import pandas as pd


gender = "male"
cardinal_vowel_int = 9
window_length = "broadband"
# low contrast - low dynamic_range (30) and low db_coeff (5)
# high contrast - high dynamic_range (70) and high db_coeff (10)
# the higher the darker
dynamic_range = 30
# the lower the darker
db_coeff = 5
save = False


if cardinal_vowel_int < 10:
    cardinal_vowel_str = "0" + str(cardinal_vowel_int)
else:
    cardinal_vowel_str = str(cardinal_vowel_int)
save_name = str(cardinal_vowel_int) + "_" + gender + "_" + "dynrange" + str(dynamic_range) + "_" + "dbcoeff" + str(db_coeff)
if gender == "male":
    audio_folder_name = "/media/luke/WORK/Current Projects/cardinal_vowels_for_analysis_m/"
    formant_measurements_df = pd.read_table("male_means.tsv")
elif gender == "female":
    audio_folder_name = "/media/luke/WORK/Current Projects/cardinal_vowels_for_analysis_f/"
    formant_measurements_df = pd.read_table("female_means.tsv")

if __name__ == "__main__":
    parselmouth_spectrum_grapher = ParselmouthSpectrumGrapher()
    parselmouth_spectrum_grapher.get_average_spectrum_slice_values(folder_name=audio_folder_name,
                                                                cardinal_vowel=cardinal_vowel_str, 
                                                                window_length=window_length)
    parselmouth_spectrum_grapher.draw_average_spectrum_slice()
