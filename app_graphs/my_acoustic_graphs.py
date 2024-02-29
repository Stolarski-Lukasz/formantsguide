from abc import ABC, abstractclassmethod
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class SpectrogramGrapher(ABC):

    @abstractclassmethod
    def draw_spectrogram(self, spectrogram, colour_scheme="Greys", dynamic_range=50):
        pass

    @abstractclassmethod
    def draw_average_spectrogram(self, average_spectrogram_values, colour_scheme="Greys", duration=1, ntimesteps=3000, dynamic_range=30):
        pass


# the methods in this class take Parselmouth spectrogram (or values base on it) as an argument
class ParselmouthSpectrogramGrapher(SpectrogramGrapher):

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
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() -
                       dynamic_range, cmap=colour_scheme)
        plt.ylim(0, 4000)
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
        plt.show()

# this is the absolute values version - the default one
    # def draw_average_spectrogram(self, Y,
    #                              average_spectrogram_values,
    #                              cardinal_vowel,
    #                              sample_size,
    #                              window_length,
    #                              colour_scheme="Greys",
    #                              duration=1,
    #                              dynamic_range=50,
    #                              db_coeff=10,
    #                              formants=None,
    #                              show_f3=False,
    #                              save=False,
    #                              save_name=None,
    #                              save_folder="",
    #                              title=True):
    #     """
    #     Draws an average spectrogram. Requires the method get_average_spectrogram_values to be executed first.

    #     Args:
    #         colour_scheme (str, optional): Defaults to "Greys". Other options: "bone", "afmhot"
    #         duration (int, optional): Defaults to 1. Sets the max duration of a spectrogram.
    #         dynamic_range (int, optional): Defaults to 50.
    #         db_coeff (int, optional):. Defaults to 10.
    #         formants (list optional): Defaults to None. Supply a list with spectrogram values to overlay formants on the spectrogram.
    #         save (bool, optional): Defaults to False. Choose True to save the spectrogram.
    #         save_name (str, optional): Defaults to None. Choose a specific name you want to save your spectrogram as.
    #         save_folder (str, optional): Defaults to an empty string. Choose a folder you want to save your spectrogram in, relative to the main executable file.
    #     """
    #     plt.figure()
    #     X = np.linspace(0, duration, len(Y))
    #     sg_db = db_coeff * np.log10(average_spectrogram_values)
    #     plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() -
    #                    dynamic_range, cmap=colour_scheme, shading='auto')
    #     if formants:
    #         f1 = np.array([formants[0]] * len(Y))
    #         plt.plot(X, f1, 'o', markersize=0.8, color='tab:blue')
    #         f2 = np.array([formants[1]] * len(Y))
    #         plt.plot(X, f2, 'o', markersize=0.8, color='tab:green')
    #         if show_f3 == True:
    #             f3 = np.array([formants[2]] * len(Y))
    #             plt.plot(X, f3, 'o', markersize=0.8, color='gold')
    #     plt.xlabel("Time [unspecified]", size=13)
    #     plt.ylabel("Frequency [Hz]", size=13)
    #     plt.ylim(0, 4000)
    #     # plt.xticks(visible=False)
    #     plt.gca().set_xticklabels([])
    #     plt.gca().get_xaxis().set_ticks([])

    #     if title:
    #         plt.title("CV " + str(cardinal_vowel) + " average " + "quasi-spectrogram " + "(n = " + str(sample_size) + ")")

    #     if save:
    #         if save_name:
    #             plt.savefig(save_folder + save_name, dpi=200)
    #         else:
    #             plt.savefig("average_spectrogram", dpi=200)
    #     # removing frame
    #     for pos in ['right', 'top', 'bottom', 'left']:
    #         plt.gca().spines[pos].set_visible(False)
        
    #     plt.close()

# this is the normalized z-values version - it works
    def draw_average_spectrogram(self, Y,
                                 average_spectrogram_values,
                                 cardinal_vowel,
                                 sample_size,
                                 window_length,
                                 colour_scheme="Greys",
                                 duration=1,
                                 dynamic_range=50,
                                 db_coeff=10,
                                 formants=None,
                                 show_f3=False,
                                 z_score_normalization=False,
                                 save=False,
                                 save_name=None,
                                 save_folder="",
                                 title=True):
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
        X = np.linspace(0, duration, len(Y))
        if z_score_normalization:
            sg_db = average_spectrogram_values
            partial_name = " normalized average quasi-spectrogram "
            print("my_acoustic_graphs z_score_normalization")
            plt.pcolormesh(X, Y, sg_db, cmap=colour_scheme, shading='auto')
        else:
            sg_db = db_coeff * np.log10(average_spectrogram_values)
            partial_name = " average quasi-spectrogram "
            plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() -
                        dynamic_range, cmap=colour_scheme)
        if formants:
            f1 = np.array([formants[0]] * len(Y))
            plt.plot(X, f1, 'o', markersize=0.8, color='tab:blue')
            f2 = np.array([formants[1]] * len(Y))
            plt.plot(X, f2, 'o', markersize=0.8, color='tab:green')
            if show_f3 == True:
                f3 = np.array([formants[2]] * len(Y))
                plt.plot(X, f3, 'o', markersize=0.8, color='gold')
        plt.xlabel("Time [unspecified]", size=13)
        plt.ylabel("Frequency [Hz]", size=13)
        plt.ylim(0, 4000)
        # plt.xticks(visible=False)
        plt.gca().set_xticklabels([])
        plt.gca().get_xaxis().set_ticks([])

        if title:
            plt.title("CV " + str(cardinal_vowel) + partial_name + "(n = " + str(sample_size) + ")")

        if save:
            if save_name:
                plt.savefig(save_folder + save_name, dpi=200)
            else:
                plt.savefig("average_spectrogram", dpi=200)
        # removing frame
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)
        
        plt.close()


class SpectrumGrapher(ABC):

    @abstractclassmethod
    def draw_spectrum(self):
        pass

    @abstractclassmethod
    def draw_average_spectrum(self):
        pass



class ParselmouthSpectrumGrapher(SpectrumGrapher):

    # I could write a method that just draws spectrum out of sound (Sound > Analyse spectrum > To spectrum)
    def draw_spectrum(self):
        pass

    def draw_spectrum_slice(self, spectrum_slice_df):
        plt.plot(spectrum_slice_df["freq(Hz)"], spectrum_slice_df["pow(dB/Hz)"],
                 'o', markersize=0.8, color='tab:blue')
        plt.xlabel("Fequency [Hz]")
        plt.ylabel("Power [dB/Hz]")
        plt.xlim(0, 4000)
        plt.show()


# this is the absolute values version - the default one
    # def draw_average_spectrum(self, Y,
    #                           average_spectrum_values,
    #                           cardinal_vowel,
    #                           sample_size,
    #                           window_length,
    #                           db_coeff=10, 
    #                           formants=None, 
    #                           show_f3=False,
    #                           formant_colors=True, 
    #                           save=False, 
    #                           save_name=None, 
    #                           save_folder="", 
    #                           title=True):
    #     sg_db = db_coeff * np.log10(average_spectrum_values)
    #     plt.plot(Y, sg_db, 'o', markersize=0.8, color='dimgrey')
    #     plt.xlabel("Fequency [Hz]", size=13)
    #     plt.ylabel("Power [dB/Hz]", size=13)
    #     plt.xlim(0, 4000)

    #     if formants:
    #         f1 = np.array([formants[0]] * len(Y))
    #         f2 = np.array([formants[1]] * len(Y))
    #         f3 = np.array([formants[2]] * len(Y))
    #         if formant_colors:
    #             plt.plot(f1, sg_db, color='tab:blue')
    #             plt.plot(f2, sg_db, color='tab:green')
    #             if show_f3 == True:
    #                 plt.plot(f3, sg_db, color='gold')
    #         else:
    #             plt.plot(f1, sg_db, color='#4f5458')
    #             plt.plot(f2, sg_db, color='#4f5458')
    #             if show_f3 == True:
    #                 plt.plot(f3, sg_db, color='#4f5458')

    #     if title:
    #         plt.title("CV " + str(cardinal_vowel) + " average " +
    #                   "spectrum " + "(n = " + str(sample_size) + ")")

    #     # removing frame
    #     # for pos in ['right', 'top', 'bottom', 'left']:
    #     #     plt.gca().spines[pos].set_visible(False)

    #     plt.grid(color='#C8C8C8', linewidth=0.3)

    #     if save:
    #         if save_name:
    #             plt.savefig(save_folder + save_name, dpi=200)
    #         else:
    #             plt.savefig(window_length + "_average_spectrum", dpi=200)
    #     plt.close()
        


    

# this is the normalized z-values version - old experimental
    def draw_average_spectrum(self, Y,
                            average_spectrum_values,
                            cardinal_vowel,
                            sample_size,
                            window_length,
                            db_coeff=10, 
                            formants=None, 
                            show_f3=False,
                            formant_colors=True, 
                            z_score_normalization=False,
                            save=False, 
                            save_name=None, 
                            save_folder="", 
                            title=True):
        if z_score_normalization:
            sg_db = average_spectrum_values
            plt.plot(Y, sg_db, 'o', markersize=0.8, color='dimgrey')
            plt.xlabel("Fequency [Hz]", size=13)
            plt.ylabel("Normalized Power [z-scores]", size=13)
            partial_name = " normalized average spectrum "
        else:
            sg_db = db_coeff * np.log10(average_spectrum_values)
            plt.plot(Y, sg_db, 'o', markersize=0.8, color='dimgrey')
            plt.xlabel("Fequency [Hz]", size=13)
            plt.ylabel("Power [dB/Hz]", size=13)
            partial_name = " average spectrum "

        plt.xlim(0, 4000)

        if formants:
            f1 = np.array([formants[0]] * len(Y))
            f2 = np.array([formants[1]] * len(Y))
            f3 = np.array([formants[2]] * len(Y))
            if formant_colors:
                plt.plot(f1, sg_db, color='tab:blue')
                plt.plot(f2, sg_db, color='tab:green')
                if show_f3 == True:
                    plt.plot(f3, sg_db, color='gold')
            else:
                plt.plot(f1, sg_db, color='#4f5458')
                plt.plot(f2, sg_db, color='#4f5458')
                if show_f3 == True:
                    plt.plot(f3, sg_db, color='#4f5458')

        if title:
            plt.title("CV " + str(cardinal_vowel) + partial_name + "(n = " + str(sample_size) + ")")

        plt.grid(color='#C8C8C8', linewidth=0.3)
        # enable the below line for testing
        # plt.xticks(np.arange(0, 4000, 200), fontsize=7)

        if save:
            if save_name:
                plt.savefig(save_folder + save_name, dpi=200)
            else:
                plt.savefig(window_length + "_average_spectrum", dpi=200)
        plt.close()









    # this method is suboptimal - it is only for a specific time point...
    def draw_average_spectrum_slice(self):
        plt.plot(self.Y, self.average_spectrum_slice_values,
                 'o', markersize=0.8, color='tab:blue')
        plt.xlabel("Fequency [Hz]")
        plt.ylabel("Power [dB/Hz]")
        plt.xlim(0, 4000)
        plt.show()
