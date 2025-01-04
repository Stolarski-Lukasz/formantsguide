from django.core.management.base import BaseCommand
import pandas as pd
from app_databasecreation.models import Phonetician, Recording
import app_databasecreation.my_read_files as my


# settings
databasepopulation_data_folder = "app_databasecreation/databasecreation_data/"
databasepopulation_data_folder_len = len(databasepopulation_data_folder)
data = pd.read_csv(databasepopulation_data_folder + "allphoneticians 8.csv")
print("janes")
print(data.head())


# obligatory class
class Command(BaseCommand):

    # optional, will be displayed with the flag --help
    help = "Function that populates the database"

    # helper methods
    def _remove_records(self):
        Phonetician.objects.all().delete()
        Recording.objects.all().delete()

    # obligatory function - here you do things
    def handle(self, *args, **options):

        print("If you want indexes starting with 1, first restart database using the method described in Python Matrix.\n Otherwise, this functions automatically removes previous records.")
        print("This code is not a perfect example of database population. Instead, look at the code I used for ESLCorpus")
        
        self._remove_records()

        folders = my.get_folders_list(databasepopulation_data_folder)
        for folder in folders:
            phonetician = Phonetician()

            gender = folder[-2]
            phonetician.gender = gender

            name = folder[databasepopulation_data_folder_len:-3]
            phonetician.name = name

            name_len = len(name)
            official_name = name.replace("_", " ")
            official_name = official_name.title()
            official_name = official_name.replace(" Of ", " of ")
            if official_name == "University of Sheffield Male":
                official_name = "University of Sheffield (male)"
            if official_name == "University of Sheffield Female":
                official_name = "University of Sheffield (female)"
            phonetician.official_name = official_name

            phonetician.save()

            wav_files_list = my.get_files_list(files_folder=folder, file_extension="wav")
            for wav_file in wav_files_list:
                recording = Recording()

                recording.phonetician = phonetician

                file = wav_file
                recording.path = file

                vowel_start_index = databasepopulation_data_folder_len+name_len+3
                vowel_end_index = databasepopulation_data_folder_len+name_len+5
                vowel = wav_file[vowel_start_index:vowel_end_index]
                recording.vowel_str = vowel
                recording.vowel = int(vowel)
                print(name, official_name, vowel)

                recording.f1 = data[(data.speaker == name) & (data.vowel == int(vowel))].iloc[0, 5]
                recording.f2 = data[(data.speaker == name) & (data.vowel == int(vowel))].iloc[0, 6]
                recording.f3 = data[(data.speaker == name) & (data.vowel == int(vowel))].iloc[0, 7]

                recording.save()
