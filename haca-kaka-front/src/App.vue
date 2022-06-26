<template>
  <div class="app">
   <div class="header">
      <img src="./assets/logo.png" class="logo">
    </div>
    <div class="content">
        <load-button/>
    </div>
  </div>
</template>

<script>
import LoadButton from './components/LoadBut.vue';

export default {
  name: 'main-page',
  data() {
    return {
    }
  },
  components: {LoadButton},
}
</script>

<style>
@font-face {
font-family: "Raleway"; 
src: url("./assets/Raleway.ttf") format("truetype"); 
font-style: normal; 
font-weight: normal; 
} 

body{
    background-color: #96D4E1;
    width: 100%;
    height: 100%;
    margin: 0px;
  }
</style>

<style scoped>
  @media (max-width: 3840px) and (min-width: 1280px){
  .header img{
    margin-top:1%;
    margin-left:39%;
  }
  .content{
    width: 300px;
    margin-left:39%;
    margin-top: 3%;
    text-align: center;
    align-content: center;
    font-family: Raleway;
    color: #F5F5F5;
  }}

  @media (max-width: 1280px) and (min-width: 800px){
  .header img{
    margin-top:1%;
    margin-left:35%;
  }
  .content{
    width: 300px;
    margin-left:37%;
    margin-top: 3%;
    text-align: center;
    align-content: center;
    font-family: Raleway;
    color: #F5F5F5;
  }}

  @media (max-width: 800px) and (min-width: 600px){
  .header img{
    margin-top:1%;
    margin-left:23%;
  }
  .content{
    width: 300px;
    margin-left:25%;
    margin-top: 3%;
    text-align: center;
    align-content: center;
    font-family: Raleway;
    color: #F5F5F5;
  }}

  @media (max-width: 600px) and (min-width: 400px){
  .header img{
    margin-top:1%;
    margin-left:14%;
  }
  .content{
    width: 300px;
    margin-left:15%;
    margin-top: 3%;
    text-align: center;
    align-content: center;
    font-family: Raleway;
    color: #F5F5F5;
  }}

  @media (max-width: 400px) and (min-width: 0px){
  .header img{
    margin-top:1%;
    margin-left:10%;
  }
  .content{
    width: 300px;
    margin-left:12%;
    margin-top: 3%;
    text-align: center;
    align-content: center;
    font-family: Raleway;
    color: #F5F5F5;
  }}

  .header{
    border-bottom: #9F4200 3px solid;
    height: 110px;
  }
</style>
