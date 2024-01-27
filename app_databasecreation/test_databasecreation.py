import my_read_files as my

# settings
databasepopulation_data_folder = "databasecreation_data"
databasepopulation_data_folder_len = len(databasepopulation_data_folder)+1


folders = my.get_folders_list("databasecreation_data")
for folder in folders:
    gender = folder[-2]
    name = folder[databasepopulation_data_folder_len:-3]
    name_len = len(name)
    official_name = name.replace("_", " ")
    official_name = official_name.title()

    wav_files_list = my.get_files_list(files_folder=folder, file_extension="wav")
    for wav_file in wav_files_list:
        file = wav_file
        vowel_start_index = databasepopulation_data_folder_len+name_len+3
        vowel_end_index = databasepopulation_data_folder_len+name_len+5
        vowel = wav_file[vowel_start_index:vowel_end_index]
        