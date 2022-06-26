<template>
  <div class="templ">
    <div class="load" v-if="page == false">
      <h2>Анализ снимка</h2>
      <h3>Выявление аномалий в<br/>
       снимках полости рта</h3>
      <input type="file" class="file" v-on:change="loadFile()" ref="load_btn">
      <div for="file" class="label" v-on:click="clickToLoadFile()">
        <label for="file">Загрузить фото</label>
      </div>
      <h2 class="ahtung">Внимание!</h2>
      <p>Фотография должна быть выполнена
       с использованием вспышки для более точного результата</p>
    </div>
    <div class="show" v-if="page == true">

      <p class="picture"><img :src="photo1" class="photo"></p>    

      <div class="label" v-on:click="uploadFile()">
        <a :href="photo1" download="result">Скачать фото</a>
      </div>
      <div class="back" v-on:click="backToLoad()">
        <label>Вернуться назад</label>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'load-but',
  data(){
    return {
      page: false,
      photo: null,
      imageSrc: null,
      photo1: null,
      photo_name: '',
      publicPath: process.env.BASE_URL
    }
  },
  methods:{
    clickToLoadFile(){
      var btn = this.$refs.load_btn;
      btn.click();
    },

    getBase64Image(img) {
        // Create an empty canvas element
        var canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;

        // Copy the image contents to the canvas
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);

        // Get the data-URL formatted image
        // Firefox supports PNG and JPEG. You could check img.src to
        // guess the original format, but be aware the using "image/jpg"
        // will re-encode the image.
        var dataURL = canvas.toDataURL("image/jpeg");

        return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    },

    getResult(data){
      var file = this.dataURLtoFile(data, 'photo.jpg');
      this.photo1 = URL.createObjectURL(file);
      this.photo_name = file.name;
      console.log(this.photo1);
      this.page = !this.page;
    },

    dataURLtoFile(dataurl, filename) {
        console.log(dataurl.split("''"));
        var arr = dataurl.split("'"),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = window.atob(arr[1]), 
            n = bstr.length, 
            u8arr = new Uint8Array(n);
            
        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }
        
        return new File([u8arr], filename, {type:mime});
    },

    loadFile(){
      this.photo = this.$refs.load_btn.files[0];
      console.log(this.photo);

      let formData = new FormData();
			formData.append('photo', this.photo);
      console.log(formData);
			axios.post('http://127.0.0.1:8000/photo_anal',
				formData, {
				headers: {
				'Content-Type': 'multipart/form-data',
				}}).then(response => (this.getResult(response.data)));
    },

    backToLoad(){
      this.page = !this.page;
    }
  }
}
</script>

<style scoped>

.picture {
  margin-left: -37%;
}

.ahtung{
  margin-top: 15%;
  color: #9F4200;
}
.label{
    background: #9F4200;
    border: #712F00 6px solid;
    border-radius: 67px;
    width:300px;
    height:30px;
    cursor: pointer;
  }

.label label{
  cursor: pointer;
}
.show a{
  cursor: pointer;
  color: #F5F5F5;
  font-family: Raleway;
  text-decoration: none;
}

.back label{
  cursor: pointer;
  color: #F5F5F5;
  font-family: Raleway;
  text-decoration: none;
}

.back{
    background: #9F4200;
    border: #712F00 6px solid;
    border-radius: 67px;
    width:300px;
    height:30px;
    cursor: pointer;
    margin-top: 3%;
  }

.file{
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }
</style>
