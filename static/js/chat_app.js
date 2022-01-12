let Socket=io();
let token=""//percuma dirubah cuk kalo token beda dengan id di server pesannya gak terkirim, coba aja rubah :)
document.getElementsByClassName('chat-button')[0].addEventListener('click',function(){
  let isi_chat=this.parentElement.getElementsByClassName('chat-input')[0].value;
  Socket.emit('request',{data:'send_chat',chat:isi_chat,token:token});
  Socket.emit('request',{data:'retrieve_data',token:token});
});

Socket.on('connect',()=>{
  Socket.emit('request',{data:'initialize'});
});
Socket.on('initialize',(isi_data)=>{
  token=isi_data.data;
})
Socket.on('retrieve_data',(isi_data)=>{
  let data_in=isi_data.data;
  let isi_string="";
  let chat_box=document.getElementsByClassName('main-chat-box')[0];
  for(let x=0;x<data_in.length;x++){
    if(data_in[x].tipe=='2'){
      isi_string+="<div class=\"row\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 notif-container\"><div class=\"col-sm-10 col-md-10 col-lg-8 col-xl-8 join-notif\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 join-name\" ><p>"+data_in[x].id_akun+" telah bergabung</p></div></div></div></div>"
    }
    else if(data_in[x].tipe=='1'){
      if(data_in[x].id_akun!=token){
        isi_string+="<div class=\"row\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12\"><div class=\"col-sm-10 col-md-10 col-lg-8 col-xl-8 incoming-chat\" style=\"float:left\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 sender-name\"><p>"+data_in[x].id_akun+"</p></div><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 chat-box\"><p>"+data_in[x].isi_chat+"</p></div><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 datetime\"><p>"+data_in[x].tanggal+"</p></div></div></div></div>";
      }
      else{
        isi_string+="<div class=\"row\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12\"><div class=\"col-sm-10 col-md-10 col-lg-8 col-xl-8 outcoming-chat\" style=\"float:right\"><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 sender-name\"><p>"+data_in[x].id_akun+"</p></div><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 chat-box\"><p>"+data_in[x].isi_chat+"</p></div><div class=\"col-sm-12 col-md-12 col-lg-12 col-xl-12 datetime\"><p>"+data_in[x].tanggal+"</p></div></div></div></div>"
      }
    }
  }
  chat_box.innerHTML=isi_string;
  chat_box.scrollTop=chat_box.scrollHeight;
});
