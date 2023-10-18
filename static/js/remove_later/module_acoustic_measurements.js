import { create_element, remove_element } from "./module_elements.js"

// variables need to be specified in the main js document, not necessary here


// export function click_vowel_select_button(vowel_select_button, vowel_file) {
//     vowel_select_button.addEventListener("click", function () {
//         vowel_file.click();
//     });
// };


export function show_loaded_file(vowel_file, f0_input, f1_input, f2_input, f3_input, myCanvas) {
    let file_name = "";
    vowel_file.addEventListener("change", function () {
        if (vowel_file.value) {
            file_name = vowel_file.value.match(
                /[\/\\]([\w\d\s\.\-\(\)]+)$/
            )[1];
            if (file_name.slice(-4) == '.wav' || file_name.slice(-4) == '.mp3') {
                let final_vowel_status_text = 'Status: selected ' + file_name;
                vowel_status_text.innerHTML = final_vowel_status_text;
                vowel_analysis_button.className = "btn btn-success";
                vowel_analysis_button.disabled = false;
                vowel_analysis_button.style.cursor = 'pointer';

                f0_input.value = "";
                f1_input.value = "";
                f2_input.value = "";
                f3_input.value = "";
                measurement_results_submit_button.className = "btn btn-primary";
                measurement_results_submit_button.disabled = true;
                measurement_results_submit_button.style.cursor = 'default';
                remove_element("acoustic_measurements_info_card");
                remove_element("spectrogram");
                create_element({ tag: "div", className: "card card-block d-flex shadow", style_maxWidth: "600px", id: "acoustic_measurements_info_card", parent_id: "acoustic_measurements_left_panel" });
                create_element({ tag: "div", className: "card-body align-items-center", id: "div_inside_info_card", parent_id: "acoustic_measurements_info_card" });
                create_element({ tag: "h5", parent_id: "div_inside_info_card", innerText: "Acoustic analysis may be performed in two ways:" });
                create_element({ tag: "br", parent_id: "div_inside_info_card" });
                create_element({ tag: "div", className: "row", id: "row_inside_div", parent_id: "div_inside_info_card" });
                create_element({ tag: "div", className: "col text-left", id: "div_inside_row", parent_id: "row_inside_div" });
                create_element({ tag: "ol", id: "unordered_list", parent_id: "div_inside_row" });
                create_element({ tag: "li", innerText: "Using the functionality provided on this website. Load an audio file to see the corresponding spectrogram and acoustic measurement results. Change measurement settings if the data obtained are innacurate. The values of formants and F0 can also be manually adjusted in the panel below.", parent_id: "unordered_list" });
                create_element({ tag: "br", parent_id: "unordered_list" });
                create_element({ tag: "li", innerText: 'You can perform the analysis in external speech analysis software ("Praat" is strongly recommended) and write the values of F3, F2, F1 and F0 in the panel below.', parent_id: "unordered_list" });
                spectrogram_info.hidden = true;
                results_info.hidden = true;
                myCanvas.removeLayer( 'dot' );
                myCanvas.render();
            }
            else {
                let final_vowel_status_text = 'wrong file format: choose a "wav" or an "mp3" file';
                vowel_status_text.innerHTML = final_vowel_status_text;
                vowel_analysis_button.className = "btn btn-primary";
                vowel_analysis_button.disabled = true;
                vowel_analysis_button.style.cursor = 'auto';

                f0_input.value = "";
                f1_input.value = "";
                f2_input.value = "";
                f3_input.value = "";
                measurement_results_submit_button.className = "btn btn-primary";
                measurement_results_submit_button.disabled = true;
                measurement_results_submit_button.style.cursor = 'default';
                remove_element("acoustic_measurements_info_card");
                remove_element("spectrogram");
                create_element({ tag: "div", className: "card card-block d-flex shadow", style_maxWidth: "600px", id: "acoustic_measurements_info_card", parent_id: "acoustic_measurements_left_panel" });
                create_element({ tag: "div", className: "card-body align-items-center", id: "div_inside_info_card", parent_id: "acoustic_measurements_info_card" });
                create_element({ tag: "h5", parent_id: "div_inside_info_card", innerText: "Acoustic analysis may be performed in two ways:" });
                create_element({ tag: "br", parent_id: "div_inside_info_card" });
                create_element({ tag: "div", className: "row", id: "row_inside_div", parent_id: "div_inside_info_card" });
                create_element({ tag: "div", className: "col text-left", id: "div_inside_row", parent_id: "row_inside_div" });
                create_element({ tag: "ol", id: "unordered_list", parent_id: "div_inside_row" });
                create_element({ tag: "li", innerText: "Using the functionality provided on this website. Load an audio file to see the corresponding spectrogram and acoustic measurement results. Change measurement settings if the data obtained are innacurate. The values of formants and F0 can also be manually adjusted in the panel below.", parent_id: "unordered_list" });
                create_element({ tag: "br", parent_id: "unordered_list" });
                create_element({ tag: "li", innerText: 'You can perform the analysis in external speech analysis software ("Praat" is strongly recommended) and write the values of F3, F2, F1 and F0 in the panel below.', parent_id: "unordered_list" });
                spectrogram_info.hidden = true;
                results_info.hidden = true;
                myCanvas.removeLayer( 'dot' );
                myCanvas.render();
            };
        }
        else {
            vowel_status_text.innerHTML = "no file selected";
        };
    });
};

export function settings_buttons_behaviour(female, male, custom, window_length_input, dynamic_range_input,
    maximum_formant_input, max_number_of_formants_input, pitch_floor_input, pitch_ceiling_input) {
    
        female.addEventListener("change", function () {
        if (female.checked) {
            window_length_input.value = 0.005;
            dynamic_range_input.value = 50;
            maximum_formant_input.value = 5500;
            max_number_of_formants_input.value = 5;
            pitch_floor_input.value = 100;
            pitch_ceiling_input.value = 500;
            custom_settings_button.className = "btn btn-primary";
            custom_settings_button.disabled = true;
            custom_settings_button.style.cursor = 'default';
            standard_quality.checked = true;
            black_on_white.checked = true;
        } 
    });

    male.addEventListener("change", function () {
        if (male.checked) {
            window_length_input.value = 0.005;
            dynamic_range_input.value = 50;
            maximum_formant_input.value = 5000;
            max_number_of_formants_input.value = 5;
            pitch_floor_input.value = 75;
            pitch_ceiling_input.value = 300;
            custom_settings_button.className = "btn btn-primary";
            custom_settings_button.disabled = true;
            custom_settings_button.style.cursor = 'default';
            standard_quality.checked = true;
            black_on_white.checked = true;
        } 
    });

    custom.addEventListener("change", function () {
        if (custom.checked) {
            console.log("changed custom")
            custom_settings_button.className = "btn btn-success";
            custom_settings_button.disabled = false;
            custom_settings_button.style.cursor = 'pointer';
        } 
    });

};


export function vowel_analysis(vowel_analysis_button, vowel_status_text, vowel_file, 
    f0_input, f1_input, f2_input, f3_input, female, spectrogram_info, high_quality, standard_quality, low_quality,
    black_on_white, white_on_black, flames) {
    
    // setting up variable names
    let image_quality = "";
    let colour_scheme = "";

    // adding click event
    vowel_analysis_button.addEventListener('click', function (e) {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                
                // removing spinner
                remove_element("the_spinner");
                
                // obtaining measurement results
                let json_response = xhr.responseText;
                let response_object = JSON.parse(json_response);
                let f0_mean = response_object.f0_mean;
                let f1_mean = response_object.f1_mean;
                let f2_mean = response_object.f2_mean;
                let f3_mean = response_object.f3_mean;
                let acoustic_measurements_id = response_object.acoustic_measurements_id;
                
                // spectrogram insertion
                let spectrogram_name_and_path = response_object.spectrogram_name_and_path;
                remove_element("acoustic_measurements_info_card");
                remove_element("spectrogram");
                create_element({ tag: "img", src: spectrogram_name_and_path, width: "800", height: "600", id: "spectrogram", parent_id: "acoustic_measurements_left_panel" });

                // adding info panel on how to interpret spectrogram
                spectrogram_info.hidden = false;

                // filling in form inputs
                f0_input.value = f0_mean;
                f1_input.value = f1_mean;
                f2_input.value = f2_mean;
                f3_input.value = f3_mean;
                
                //updating info text
                let file_name = vowel_file.value.match(
                    /[\/\\]([\w\d\s\.\-\(\)]+)$/
                )[1];
                vowel_status_text.innerHTML = "Status: showing analysis of " + file_name;
                
                // activating measurement_results_submit_button
                measurement_results_submit_button.className = "btn btn-success";
                measurement_results_submit_button.disabled = false;
                measurement_results_submit_button.style.cursor = 'pointer';
                console.log(acoustic_measurements_id)
                measurement_results_submit_button.dataset.acousticMeasurementsId = acoustic_measurements_id;
                
            };
        };

        // collecting data to be sent to server
        var file = vowel_file.files[0];
        var formData = new FormData();
        formData.append('file', file);

        let window_length = window_length_input.value;
        let dynamic_range = dynamic_range_input.value;
        let maximum_formant = maximum_formant_input.value;
        let max_number_of_formants = max_number_of_formants_input.value;
        let pitch_floor = pitch_floor_input.value;
        let pitch_ceiling = pitch_ceiling_input.value;

        formData.append('window_length', window_length);
        formData.append('dynamic_range', dynamic_range);
        formData.append('maximum_formant', maximum_formant);
        formData.append('max_number_of_formants', max_number_of_formants);
        formData.append('pitch_floor', pitch_floor);
        formData.append('pitch_ceiling', pitch_ceiling);

        // for now high_quality radio button is hidden in html
        if (high_quality.checked) {
            image_quality = "high"
        } else if (standard_quality.checked) {
            image_quality = "standard"
        } else if (low_quality.checked) {
            image_quality = "low"
        };
        formData.append('image_quality', image_quality);

        if (black_on_white.checked) {
            colour_scheme = "Greys"
        } else if (white_on_black.checked) {
            colour_scheme = "bone"
        } else if (flames.checked) {
            colour_scheme = "afmhot"
        };
        formData.append('colour_scheme', colour_scheme);

        // activating spinner
        create_element({ tag: "div", className: "spinner-border spinner-border-sm text-primary", role: "status", id: "the_spinner", parent_id: "vowel_analysis_button", style_marginLeft: "1em" });

        // sending the request
        xhr.open('POST', '/vowel_analysis/', true);
        xhr.send(formData);
    });
};


export function activate_submit_measurements_button() {
    f0_input.addEventListener('change', function () {
        if (f0_input.value != "" && f1_input.value != "" && f2_input.value != "" && f3_input.value != "") {
            measurement_results_submit_button.className = "btn btn-success";
            measurement_results_submit_button.disabled = false;
            measurement_results_submit_button.style.cursor = 'pointer';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        } else {
            measurement_results_submit_button.className = "btn btn-primary";
            measurement_results_submit_button.disabled = true;
            measurement_results_submit_button.style.cursor = 'default';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        }
    })
    f1_input.addEventListener('change', function () {
        if (f0_input.value != "" && f1_input.value != "" && f2_input.value != "" && f3_input.value != "") {
            measurement_results_submit_button.className = "btn btn-success";
            measurement_results_submit_button.disabled = false;
            measurement_results_submit_button.style.cursor = 'pointer';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        } else {
            measurement_results_submit_button.className = "btn btn-primary";
            measurement_results_submit_button.disabled = true;
            measurement_results_submit_button.style.cursor = 'default';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        }
    })
    f2_input.addEventListener('change', function () {
        if (f0_input.value != "" && f1_input.value != "" && f2_input.value != "" && f3_input.value != "") {
            measurement_results_submit_button.className = "btn btn-success";
            measurement_results_submit_button.disabled = false;
            measurement_results_submit_button.style.cursor = 'pointer';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        } else {
            measurement_results_submit_button.className = "btn btn-primary";
            measurement_results_submit_button.disabled = true;
            measurement_results_submit_button.style.cursor = 'default';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        }
    })
    f3_input.addEventListener('change', function () {
        if (f0_input.value != "" && f1_input.value != "" && f2_input.value != "" && f3_input.value != "") {
            measurement_results_submit_button.className = "btn btn-success";
            measurement_results_submit_button.disabled = false;
            measurement_results_submit_button.style.cursor = 'pointer';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        } else {
            measurement_results_submit_button.className = "btn btn-primary";
            measurement_results_submit_button.disabled = true;
            measurement_results_submit_button.style.cursor = 'default';
            measurement_results_submit_button.dataset.acousticMeasurementsId = "None";
        }
    })
};
