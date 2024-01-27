
import {
  add_data_to_info_icon
} from "./formantsguide-vue-auxiliary.js"


const vue_app = Vue.createApp({
  data() {
    return {
      results: false,
      x: 0,
      y: 0,
      phoneticiansList: false,
      spectrogramButton: true,
      spectrogramPathAndName: false,
      spectrumPathAndName: false,
      cardinalVowel: "",
      phoneticianGroup: "",
      sampleSize: 0,
      phoneticiansFound: 0,
      windowLength: 0,
      f1: 0,
      f2: 0,
      f3: 0,
      showF3: false,
      diagramPathAndName: "/static/img/IPA_vowel_diagram.jpg",
      recordingsNotAvailable: false,
      incorrectWindowLength: false
    }
  },
  delimiters: ["${", "}$"],
  methods: {
    showCoordinates(event) {
      this.x = event.offsetX
      this.y = event.offsetY
    },
    toggleNumbering(event) {
      if (event.target.checked == true) {
        this.diagramPathAndName = "/static/img/IPA_vowel_diagram_numbered.jpg"
      } else {
        this.diagramPathAndName = "/static/img/IPA_vowel_diagram.jpg"
      }
    },
    enablePhoneticiansList(event) {
      var phoneticians = document.getElementById("phoneticians")
      phoneticians.disabled = false

      // Iterate through all the options and deselect them
      var options = phoneticians.options;
      for (var i = 0; i < options.length; i++) {
        options[i].selected = false;
      }
      var danielJones = document.getElementById("daniel-jones")
      danielJones.selected = true
    },
    disablePhoneticiansList(event) {
      var phoneticians = document.getElementById("phoneticians")
      phoneticians.disabled = true

      var options = phoneticians.options;
      for (var i = 0; i < options.length; i++) {
        if (event.target.id == "male-phoneticians-radio") {
          if (options[i].className == "male") {
            options[i].selected = true
          } else {
            options[i].selected = false
          }
        } else if (event.target.id == "female-phoneticians-radio") {
          if (options[i].className == "female") {
            options[i].selected = true
          } else {
            options[i].selected = false
          }
        }
      }
    },
    enableWindowLengthInput(event) {
      var windowLengthInput = document.getElementById("window-length-input")
      windowLengthInput.disabled = false
    },
    disableWindowLengthInput(event) {
      var windowLengthInput = document.getElementById("window-length-input")
      windowLengthInput.disabled = true
      if (event.target.id == "broadband-radio") {
        windowLengthInput.value = "0.005"
      } else if (event.target.id == "narrowband-radio") {
        windowLengthInput.value = "0.03"
      }
    },
    toggleShowF3Checkbox(event) {
      var showF3Checkbox = document.getElementById("show-f3")
      if (event.target.checked == true) {
        showF3Checkbox.disabled = false
      } else {
        showF3Checkbox.disabled = true
        showF3Checkbox.checked = false
        this.showF3 = false
      }
    },
    create_figure(event) {
      // reset figures
      this.spectrogramPathAndName = false
      this.spectrumPathAndName = false
      this.recordingsNotAvailable = false
      this.incorrectWindowLength = false

      // get data
      const user_form = document.querySelector('#userform');
      const cardinal_vowel = event.target.id


      // create parameters for get request
      const formData = new FormData(user_form);
      formData.append("cardinal_vowel", cardinal_vowel)
      let params = new URLSearchParams(formData);

      // updating global variables
      // TODO adjust sample size for "selected"
      this.cardinalVowel = cardinal_vowel.slice(2)
      this.phoneticianGroup = formData.get("phonetician-group")
      this.windowLength = formData.get("window-length")
      // TODO
      var showF3Checkbox = document.getElementById("show-f3")
      if (showF3Checkbox.checked == true) {
        this.showF3 = true
      } else {
        this.showF3 = false
      }

      const request = new XMLHttpRequest();
      // handle response
      request.addEventListener('readystatechange', () => {
        if (request.readyState === 4 && request.status === 200) {
          console.log("response")
          let json_response = request.responseText;
          let response_object = JSON.parse(json_response);
          if (response_object.incorrect_window_length) {
            this.incorrectWindowLength = true
          }
          else if (response_object.f1 == null) {
            this.recordingsNotAvailable = true
            console.log("here")
          } else {
            this.f1 = response_object.f1
            this.f2 = response_object.f2
            this.f3 = response_object.f3
            console.log(response_object.spectrogram_path_and_name)
            this.spectrogramPathAndName = response_object.spectrogram_path_and_name
            this.spectrumPathAndName = response_object.spectrum_path_and_name
            this.sampleSize = response_object.sample_size
            this.phoneticiansFound = response_object.phoneticians_found
          }
        }
      })

      request.open('GET', '/create_spectrogram/?' + params.toString());
      request.send();
    },
    search(event) {
      const user_form = document.querySelector('#userform');

      // handling response
      const request = new XMLHttpRequest();
      request.addEventListener('readystatechange', () => {
        if (request.readyState === 4 && request.status === 200) {
          let json_response = request.responseText;
          let response_object = JSON.parse(json_response);
          let results_array = []
          let result_name_counter = 0
          for (let result in response_object) {
            results_array.push(response_object['result' + result_name_counter].parts)
            result_name_counter += 1
          }
          this.results = true
          this.results_arrayofarrays = results_array

          Vue.nextTick(function () {
            add_data_to_info_icon(response_object)
          })
        }
      })
      const formData = new FormData(user_form);
      const params = new URLSearchParams(formData);
      request.open('GET', '/search/?' + params.toString());
      request.send();
    }
  }
})


vue_app.mount('#vue_wrapper')