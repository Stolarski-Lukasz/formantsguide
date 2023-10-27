from abc import ABC, abstractclassmethod
import numpy as np
import matplotlib.pyplot as plt
from .my_parselmouth import get_spectrogram_object, get_spectrum_slice_df
from .my_read_files import get_folders_list, get_files_list


class SpectrogramGrapher(ABC):

    @abstractclassmethod
    def draw_spectrogram(self, spectrogram, colour_scheme="Greys", dynamic_range=50):
        pass

    @abstractclassmethod
    def get_average_spectrogram_values(self, folder_name, cardinal_vowel):
        pass

    @abstractclassmethod
    def draw_average_spectrogram(self, average_spectrogram_values, colour_scheme="Greys", duration=1, ntimesteps=3000, dynamic_range=30):
        pass


# the methods in this class take Parselmouth spectrogram as an argument
class ParselmouthSpectrogramGrapher(SpectrogramGrapher):
    """
    For now, this is optimized for the analysis of Cardinal Vowels in my dataset. In the future, try to make it more universal.

    Args:
        SpectrogramGrapher (_type_): _description_
    """

    def __init__(self):
        self.average_spectrogram_values = None
        self.cardinal_vowel = None
        self.Y = None
        self.window_length = None
        self.sample_size = None

    def draw_spectrogram(self, spectrogram, colour_scheme="Greys", dynamic_range=50):
        """
        Draws a single spectrogram based on Parselmouth spectrogram object.

        Args:
            spectrogram (Parselmouth spectrogram): Parselmouth spectrogram
            colour_scheme (str, optional): Defaults to "Greys". Other options: "bone", "afmhot"
            dynamic_range (int, optional): Defaults to 50.
        """
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap=colour_scheme)
        plt.ylim(0, 4000)
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
        plt.show()

    def get_average_spectrogram_values(self, folder_name, cardinal_vowel, window_length="broadband"):
        """
        Generates average values for each frequency bin and multiplies these values to match frequency bins number (so that the data can be x-y plotted)

        Args:
            folder_name (str): path/folder to vowel recordings
            cardinal_vowel (str): e.g. 01, 10, 20
            window_length (str, optional): Defaults to "broadband". Other options are "narrowband" or you can provide an integer value, just like in "get_spectrogram" in get_spectrogram_object in my_parselmouth.py
        """
        self.cardinal_vowel = cardinal_vowel
        self.window_length = window_length
        folders_list = get_folders_list(folder_name)
        print("folders list: ", folders_list)
        singlevowel_means_for_bins_list = []
        sample_size = 0
        for folder in folders_list:
            folder_length = len(folder)
            files_list = get_files_list(folder)
            for file in files_list:
                if file[folder_length:folder_length+2] == cardinal_vowel:
                    print("found: ", file)
                    sample_size += 1
                    spectrogram = get_spectrogram_object(sound_file=file, 
                                                window_length=window_length)
                    means_for_bins = []
                    for bin_array in spectrogram.values:
                        means_for_bins.append(np.mean(bin_array))
                    singlevowel_means_for_bins_list.append(means_for_bins)

        self.Y = spectrogram.y_grid()[:-1]
        self.sample_size = sample_size
        self.cardinal_vowel = cardinal_vowel
        general_means_for_bins = np.mean(np.array(singlevowel_means_for_bins_list), axis=0)
        # creating 2-dimensional np array with means_for_bins repeated the times equal to the number of frequency bins for each bin
        self.average_spectrogram_values = np.tile(general_means_for_bins[:, np.newaxis], len(self.Y))

    def draw_average_spectrogram(self, colour_scheme="Greys", duration=1, dynamic_range=50, db_coeff=10, formants=None, save=False, save_name=None, save_folder="", title=True):
        """
        Draws an average spectrogram. Requires the method get_average_spectrogram_values to be executed first.

        Args:
            colour_scheme (str, optional): Defaults to "Greys". Other options: "bone", "afmhot"
            duration (int, optional): Defaults to 1. Sets the max duration of a spectrogram.
            dynamic_range (int, optional): Defaults to 50.
            db_coeff (int, optional):. Defaults to 10.
            formants (list optional): Defaults to None. Supply a list with spectrogram values to overlay formants on the spectrogram.
            save (bool, optional): Defaults to False. Choose True to save the spectrogram.
            save_name (str, optional): Defaults to None. Choose a specific name you want to save your spectrogram as.
            save_folder (str, optional): Defaults to an empty string. Choose a folder you want to save your spectrogram in, relative to the main executable file.
        """
        plt.figure()
        X = np.linspace(0, duration, len(self.Y))
        sg_db = db_coeff * np.log10(self.average_spectrogram_values)
        plt.pcolormesh(X, self.Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap=colour_scheme)
        if formants:
            f1 = np.array([formants[0]] * len(self.Y))
            plt.plot(X, f1, 'o', markersize=0.8, color='tab:blue')
            f2 = np.array([formants[1]] * len(self.Y))
            plt.plot(X, f2, 'o', markersize=0.8, color='tab:green')
            f3 = np.array([formants[2]] * len(self.Y))
            plt.plot(X, f3, 'o', markersize=0.8, color='gold')
        plt.xlabel("Time [unspecified]", size=13)
        plt.ylabel("Frequency [Hz]", size=13)
        plt.ylim(0, 4000)
         # plt.xticks(visible=False)
        plt.gca().set_xticklabels([])
        plt.gca().get_xaxis().set_ticks([])

        if title:
            plt.title("CV " + str(self.cardinal_vowel) + " average " + self.window_length + " spectrogram " + "(n = " + str(self.sample_size) + ")")

        if save:
            if save_name:
                plt.savefig(save_folder + "CV_" + save_name + "_" + self.window_length + "_average_spectrogram", dpi=200)
            else:
                plt.savefig( self.window_length + "_average_spectrogram", dpi=200)
        # removing frame
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)
        # plt.show()


class ParselmouthSpectrumGrapher():

    def __init__(self):
        self.average_spectrum_values = None
        self.average_spectrum_slice_values = None
        self.cardinal_vowel = None
        self.Y = None
        self.sample_size = None

    # I could write a method that just draws spectrum out of sound (Sound > Analyse spectrum > To spectrum)
    def draw_spectrum(self):
        pass

    def draw_spectrum_slice(self, spectrum_slice_df):
        plt.plot(spectrum_slice_df["freq(Hz)"], spectrum_slice_df["pow(dB/Hz)"], 'o', markersize=0.8, color='tab:blue')
        plt.xlabel("Fequency [Hz]")
        plt.ylabel("Power [dB/Hz]")
        plt.xlim(0, 4000)
        plt.show()

    def get_average_spectrum_values(self, folder_name, cardinal_vowel, window_length="broadband"):
        """
        Generates average values for each frequency bin and multiplies these values to match frequency bins number (so that the data can be x-y plotted)

        Args:
            folder_name (str): path/folder to vowel recordings
            cardinal_vowel (str): e.g. 01, 10, 20
            window_length (str, optional): Defaults to "broadband". Other options are "narrowband" or you can provide an integer value, just like in "get_spectrogram" in get_spectrogram_object in my_parselmouth.py
            time_step (float, optional): Defaults to 0.0001.
        """
        self.cardinal_vowel = cardinal_vowel
        self.window_length = window_length
        folders_list = get_folders_list(folder_name)
        singlevowel_means_for_bins_list = []
        sample_size = 0
        for folder in folders_list:
            folder_length = len(folder)
            files_list = get_files_list(folder)
            for file in files_list:
                if file[folder_length:folder_length+2] == cardinal_vowel:
                    print("found: ", file)
                    sample_size += 1
                    spectrogram = get_spectrogram_object(sound_file=file, 
                                                window_length=window_length)
                    means_for_bins = []
                    for bin_array in spectrogram.values:
                        means_for_bins.append(np.mean(bin_array))
                    singlevowel_means_for_bins_list.append(means_for_bins)
        
        self.sample_size = sample_size
        self.Y = spectrogram.y_grid()[:-1]
        general_means_for_bins = np.mean(np.array(singlevowel_means_for_bins_list), axis=0)
        self.average_spectrum_values = general_means_for_bins

    # this only for the draw_spectrum_slice method which is suboptimal - it is only for a specific time point...
    def get_average_spectrum_slice_values(self, folder_name, cardinal_vowel, window_length="broadband"):
        self.window_length = window_length
        folders_list = get_folders_list(folder_name)
        singlevowel_powers = []
        for folder in folders_list:
            folder_length = len(folder)
            files_list = get_files_list(folder)
            for file in files_list:
                if file[folder_length:folder_length+2] == cardinal_vowel:
                    print("found: ", file)
                    spectrogram = get_spectrogram_object(sound_file=file, 
                                                window_length=window_length)
                    spectrum_slice_df = get_spectrum_slice_df(spectrogram_object=spectrogram)
                    singlevowel_powers.append(spectrum_slice_df["pow(dB/Hz)"])
                    # means_for_bins = []
                    # for bin_array in spectrogram.values:
                    #     means_for_bins.append(np.mean(bin_array))
                    # singlevowel_means_for_bins_list.append(means_for_bins)
        print(type(singlevowel_powers))
        average_spectrum_slice_values = np.mean(np.array(singlevowel_powers), axis=0)
        self.average_spectrum_slice_values = average_spectrum_slice_values
        self.Y = spectrogram.y_grid()[:-1]
        # general_means_for_bins = np.mean(np.array(singlevowel_means_for_bins_list), axis=0)

    def draw_average_spectrum(self, db_coeff=10, formants=None, formant_colors=True, save=False, save_name=None, save_folder="", title=True):
        sg_db = db_coeff * np.log10(self.average_spectrum_values)
        plt.plot(self.Y, sg_db, 'o', markersize=0.8, color='dimgrey')
        plt.xlabel("Fequency [Hz]", size=13)
        plt.ylabel("Power [dB/Hz]", size=13)
        plt.xlim(0, 4000)

        if formants:
            f1 = np.array([formants[0]] * len(self.Y))
            f2 = np.array([formants[1]] * len(self.Y))
            f3 = np.array([formants[2]] * len(self.Y))
            if formant_colors:
                plt.plot(f1, sg_db, color='tab:blue')
                plt.plot(f2, sg_db, color='tab:green')
                plt.plot(f3, sg_db, color='gold')
            else:
                plt.plot(f1, sg_db, color='#4f5458')
                plt.plot(f2, sg_db, color='#4f5458')
                plt.plot(f3, sg_db, color='#4f5458')

        if title:
            plt.title("CV " + str(self.cardinal_vowel) + " average " + self.window_length + " spectrum " + "(n = " + str(self.sample_size) + ")")

        # removing frame
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)
        
        plt.grid(color = '#C8C8C8', linewidth = 0.3)

        if save:
            if save_name:
                plt.savefig(save_folder + "CV_" + save_name + "_" + self.window_length + "_average_spectrum", dpi=200)
            else:
                plt.savefig( self.window_length + "_average_spectrum", dpi=200)

        plt.show()

    # this method is suboptimal - it is only for a specific time point...
    def draw_average_spectrum_slice(self):
        plt.plot(self.Y, self.average_spectrum_slice_values, 'o', markersize=0.8, color='tab:blue')
        plt.xlabel("Fequency [Hz]")
        plt.ylabel("Power [dB/Hz]")
        plt.xlim(0, 4000)
        plt.show()