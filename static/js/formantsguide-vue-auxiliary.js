// this ia a dummy funcition from before - change it
function add_data_to_info_icon(response_object) {
    let results_icon_info_buttons = document.getElementsByClassName('pca-results-icon-info');
    console.log(results_icon_info_buttons)
    let result_name_counter = 0
    Array.from(results_icon_info_buttons).forEach(function (results_icon_info_button) {
        console.log("sss")
        console.log(response_object['result' + result_name_counter].keyword_audio_start)
        results_icon_info_button.setAttribute('data-keyword-audio-start', response_object['result' + result_name_counter].keyword_audio_start);
        results_icon_info_button.setAttribute('data-keyword-audio-end', response_object['result' + result_name_counter].keyword_audio_end);
        results_icon_info_button.setAttribute('data-concordance-span-audio-start', response_object['result' + result_name_counter].concordance_span_audio_start);
        results_icon_info_button.setAttribute('data-concordance-span-audio-end', response_object['result' + result_name_counter].concordance_span_audio_end);
        results_icon_info_button.setAttribute('data-speaker-name', response_object['result' + result_name_counter].speaker_name);
        results_icon_info_button.setAttribute('data-speaker-gender', response_object['result' + result_name_counter].speaker_gender);
        results_icon_info_button.setAttribute('data-speaker-age', response_object['result' + result_name_counter].speaker_age);
        results_icon_info_button.setAttribute('data-speaker-education', response_object['result' + result_name_counter].speaker_education);
        results_icon_info_button.setAttribute('data-speaker-proficiency', response_object['result' + result_name_counter].speaker_proficiency);
        results_icon_info_button.setAttribute('data-file-name', response_object['result' + result_name_counter].file_name);
        // results_icon_info_button.setAttribute('data-text-function', response_object['result' + result_name_counter].sentence_type);
        // results_icon_info_button.setAttribute('data-audio-file-name', response_object['result' + result_name_counter].audio_file_name);
        // results_icon_info_button.setAttribute('data-textunit-start', response_object['result' + result_name_counter].textunit_start);
        // results_icon_info_button.setAttribute('data-textunit-end', response_object['result' + result_name_counter].textunit_end);
        // results_icon_info_button.setAttribute('data-order-in-chapter', response_object['result' + result_name_counter].order_in_chapter);
        result_name_counter++
    })
}

export {
    add_data_to_info_icon
}