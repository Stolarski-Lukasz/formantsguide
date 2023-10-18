
import {
  add_data_to_info_icon
} from "./formantsguide-vue-auxiliary.js"


const vue_app = Vue.createApp({
  data() {
    return {
      results: false,
      x: 0,
      y: 0,
      phoneticiansList: false
    }
  },
  delimiters: ["${", "}$"],
  methods: {
    showCoordinates(event) {
      this.x = event.offsetX
      this.y = event.offsetY
    },
    showPhoneticiansList(event) {
      this.phoneticiansList = true
      console.log("clicked")
    },
    hidePhoneticiansList(event) {
      this.phoneticiansList = false
      console.log("clicked")
    },
    create_spectrogram(event){
      const user_form = document.querySelector('#userform');
      const request = new XMLHttpRequest();
      
      console.log("here")
      const cardinal_vowel = event.target.id


      const formData = new FormData(user_form);
      console.log(formData)
      formData.append("cardinal_vowel", cardinal_vowel)
      let params = new URLSearchParams(formData);

      console.log(params)
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