
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
      spectrogramButton: true
    }
  },
  delimiters: ["${", "}$"],
  methods: {
    showCoordinates(event) {
      this.x = event.offsetX
      this.y = event.offsetY
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
    create_figure(event) {
      // getting data
      const user_form = document.querySelector('#userform');
      const cardinal_vowel = event.target.id
      const formData = new FormData(user_form);
      console.log(formData)
      formData.append("cardinal_vowel", cardinal_vowel)
      let params = new URLSearchParams(formData);

      if (formData.get("formantsCheck")) {
        console.log("formantsCheck registed")
      }
      // else if ()



      const request = new XMLHttpRequest();


      // params = params + "&cardinal_vowel=" + cardinal_vowel
      // console.log(params)
      // request.open('GET', '/search/?' + params.toString());
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