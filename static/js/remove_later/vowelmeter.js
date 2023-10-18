import { create_element, remove_element } from "./module_elements.js"
import { click_vowel_select_button, 
  show_loaded_file, settings_buttons_behaviour,
  vowel_analysis, 
  activate_submit_measurements_button 
} from "./module_acoustic_measurements.js"
import { draw_vq, 
  draw_coordinate_grid,
  submit_measurement_results, 
  grid_switch_behaviour
 } from "./module_automatic_placement.js"



////// ACOUSTIC MEASUREMENTS START /////
////////////////////////////////////////

// VARIABLE DECLARATIONS
const vowel_select_button = document.getElementById("vowel_select_button");
const vowel_file = document.getElementById("vowel_file");
const vowel_analysis_button = document.getElementById("vowel_analysis_button");
const vowel_status_text = document.getElementById("vowel_status_text");
let f0_input = document.getElementById("f0_input");
let f1_input = document.getElementById("f1_input");
let f2_input = document.getElementById("f2_input");
let f3_input = document.getElementById("f3_input");
let female = document.getElementById("customRadioInline1");
let male = document.getElementById("customRadioInline2");
let custom = document.getElementById("customRadioInline3");
let window_length_input = document.getElementById("window_length_input");
let dynamic_range_input = document.getElementById("dynamic_range_input");
let maximum_formant_input = document.getElementById("maximum_formant_input");
let max_number_of_formants_input = document.getElementById("max_number_of_formants_input");
let pitch_floor_input = document.getElementById("pitch_floor_input");
let pitch_ceiling_input = document.getElementById("pitch_ceiling_input");
let custom_settings_button = document.getElementById("custom_settings_button");

let spectrogram_info = document.getElementById("spectrogram_info");
let measurement_results_submit_button = document.getElementById("measurement_results_submit_button");
let high_quality = document.getElementById("high_quality");
let standard_quality = document.getElementById("standard_quality");
let low_quality = document.getElementById("low_quality");
let black_on_white = document.getElementById("black_on_white");
let white_on_black = document.getElementById("white_on_black");
let flames = document.getElementById("flames");

var myCanvas = new layeredCanvas( "theCanvas" );

// FUNCTIONS
click_vowel_select_button(vowel_select_button, vowel_file);
show_loaded_file(vowel_file, f0_input, f1_input, f2_input, f3_input, myCanvas);
// I did not insert "standard_quality" and "black_and_white" as parameters in the main script (they are in the module), and it still works fine... - some variables do not need to be specified
settings_buttons_behaviour(female, male, custom, window_length_input, dynamic_range_input,
  maximum_formant_input, max_number_of_formants_input, pitch_floor_input, pitch_ceiling_input);
vowel_analysis(vowel_analysis_button, vowel_status_text, vowel_file, f0_input,
   f1_input, f2_input, f3_input, female, spectrogram_info, high_quality, standard_quality, low_quality,
   black_on_white, white_on_black, flames);
activate_submit_measurements_button();

////// ACOUSTIC MEASUREMENTS ENDED /////
////////////////////////////////////////



///// AUTOMATIC PLACEMENT START /////
/////////////////////////////////////

// VARIABLE DECLARATIONS
const grid_switch = document.getElementById("grid_switch");
const results_info = document.getElementById("results_info");
const results_info_contents = document.getElementById("results_info_contents");
let base_size = 800;
let margin = 0.1*base_size;

// FUNCTIONS
grid_switch_behaviour(grid_switch, base_size, margin, myCanvas);
draw_vq(base_size, margin, myCanvas);
draw_coordinate_grid(base_size, margin, myCanvas);
submit_measurement_results(measurement_results_submit_button, f0_input,
  f1_input, f2_input, f3_input, base_size, margin, myCanvas, results_info, results_info_contents)

///// AUTOMATIC PLACEMENT ENDED /////
/////////////////////////////////////


// image download button functionality START
////////////////////////////////////////////

// VARIABLE DECLARATIONS
const image_download_button = document.getElementById('image_download_button');
const image_download = document.getElementById('image_download');
const canvas = document.querySelector('canvas');

// FUNCTIONS
image_download.addEventListener('click', function (e) {
    var dataURL = canvas.toDataURL('image/png');
    image_download.href = dataURL;
});

// image download button functionality ENDED
////////////////////////////////////////////