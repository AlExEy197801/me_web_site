let peerConnection;  // объект однорангового соединения
let localStream;  // для локального видео
let remoteStream; // для удалённого видео
let rand_name = Math.floor(Math.random() * 1000000000).toString()

let servers = {  // серверы оглушения от google
  iceServers: [
      {
          urls: ['stun:stunserver.org']
      }
  ]
}

const roomName = JSON.parse(document.getElementById('room_name').textContent);

let loc = window.location;
let wsStart = 'ws://';
if (loc.protocol == 'https:') {
     wsStart = 'wss://'
}
const socket = new WebSocket(`${wsStart}${window.location.host}/ws/chat/${roomName}/`);

// const socket = new WebSocket(`ws://192.168.100.4/ws/chat/${roomName}/`);
console.log(window.location.host)
const createOfferButton = document.querySelector('#create-offer')

console.log('localStream:', navigator.mediaDevices.enumerateDevices())
let device = navigator.mediaDevices.enumerateDevices()

let init = async() => {
  localStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
  })  // захватывает камеру

  console.log('localStream', localStream)

  document.getElementById('user-1').srcObject = localStream

  // инициализация сразу после загрузки страницы
  // localStream = await navigator.mediaDevices.getDisplayMedia({
  //     video: true,
  //     audio: false
  // })  // getDisplayMedia -- захватывает экран

  // console.log('localStream:', await navigator.mediaDevices.enumerateDevices())
}

let createOffer = async() => {
  // createPeerConnection('offer-sdp')
  peerConnection = new RTCPeerConnection(servers)

  localStream.getTracks().forEach((track) => {
    peerConnection.addTrack(track, localStream)  // добавляем треки с localStream
  })  // у нас это локальные, для других user'ов удалённые

  peerConnection.ontrack = async(event) => {
      event.streams[0].getTracks().forEach((track) => {
      remoteStream.addTrack(track)
    })
  }

  peerConnection.onicecandidate = async (event) => {
    if(event.candidate){
        document.getElementById('offer-sdp').value = JSON.stringify(peerConnection.localDescription)
        // socket.send(JSON.stringify({'message': sdpType, 'type':'candidate', 'candidate':event.candidate}));
    }
  }

  let offer = await peerConnection.createOffer()  // предложение с

  await peerConnection.setLocalDescription(offer)  // локальным описанием
  // document.getElementById('offer-sdp').value = JSON.stringify(offer)

  // socket.send(JSON.stringify({'type_mes': 'offer', 'message': offer}))

}

let addAnswer = async () => {
  let answer = document.getElementById('answer-sdp').value
  if(!answer) return alert('Retrieve answer from peer first...')

  answer = JSON.parse(answer)

  if(!peerConnection.currentRemoteDescription){
      await peerConnection.setRemoteDescription(answer)
  }
  console.log('answer3')
}

function sendOffer(rand_nam) {
  offer = document.getElementById('offer-sdp').value
  offer = JSON.parse(offer)
  socket.send(JSON.stringify({'type_mes': 'offer', 'message': {'rand_name': rand_nam, 'message': offer} }))
}

init()

socket.onmessage = async function(event) {

  let message = event;
  console.log('\nsocket.onmessage message main--->', message)
  data = JSON.parse(message.data)
  console.log('data = JSON.parse(message.data)---->', data)
  console.log('data.message.type_mes---->', data.type_mes, '\n')
  console.log('data.message.rand_name---->', data.message.rand_name)

  if(data.type_mes == 'hi') {
    createOffer()
    setTimeout(() => sendOffer(data.message.rand_name), 5000);

  } else {
    document.getElementById('answer-sdp').value  = JSON.stringify(data.message.message)
    setTimeout(() => addAnswer(), 10000);
  }
}

document.getElementById('create-offer').addEventListener('click', createOffer)
// document.getElementById('create-answer').addEventListener('click', createAnswer)
document.getElementById('add-answer').addEventListener('click', addAnswer)
