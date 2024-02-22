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

let init = async() => {
  // инициализация сразу после загрузки страницы
  localStream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
      audio: false
  })  // getDisplayMedia -- захватывает экран

  document.getElementById('user-1').srcObject = localStream
  // localStream = await navigator.mediaDevices.getUserMedia({
  //     video: true,
  //     audio: true
  // })  // захватывает камеру
  document.getElementById('ttt').value = rand_name
}

// Обработчик открытия соединения
socket.addEventListener('open', (event) => {
    console.log('WebSocket connection opened:', event);
});

// Обработчик закрытия соединения
socket.addEventListener('close', (event) => {
    console.log('WebSocket connection closed:', event);
});

let createOffer = async() => {

  createPeerConnection('offer-sdp')
  let offer = await peerConnection.createOffer()  // предложение с
  await peerConnection.setLocalDescription(offer)  // локальным описанием
  console.log('offer', JSON.stringify(offer))
  document.getElementById('offer-sdp').value = JSON.stringify(offer)
  console.log('передаём на страницу SDP Offer:\n', JSON.stringify(offer))
  sendCreateOffer()
}

let createPeerConnection = async(sdpType) => {
    peerConnection = new RTCPeerConnection(servers)
    console.log('createOffer-servers', servers)
    console.log('createOffer-peerConnection', peerConnection)

    remoteStream = new MediaStream()  // удалённый поток, пока без параметрров
    document.getElementById('user-2').srcObject = remoteStream

    peerConnection.ontrack = async(event) => {
        event.streams[0].getTracks().forEach((track) => {
            remoteStream.addTrack(track)
        })
    }
}

let createAnswer = async () => {
  createPeerConnection('answer-sdp')

  let offer = document.getElementById('offer-sdp').value
  if(!offer) return alert('Retrieve offer from peer first...')

  offer = JSON.parse(offer)
  await peerConnection.setRemoteDescription(offer)

  let answer = await peerConnection.createAnswer()
  await peerConnection.setLocalDescription(answer)

  document.getElementById('answer-sdp').value  = JSON.stringify(answer)
  // socket.send(JSON.stringify({'type_mes': 'answer','message': answer}));
}

socket.addEventListener('open', () => {
  // При открытии соединение тут же отправляем накопленные сообщения
  socket.send(JSON.stringify({'type_mes': 'hi', 'message': {'rand_name': rand_name,}}))
})

function sendAnswer() {
  answer = document.getElementById('answer-sdp').value
  answer = JSON.parse(answer)
  socket.send(JSON.stringify({'type_mes': 'answer', 'message': {'rand_name': rand_name, 'message': answer}}))
}

init()

socket.onmessage = async function(event) {
  let message = event;
  console.log('\nsocket.onmessage message main--->', message)
  data = JSON.parse(message.data)
  console.log('data = JSON.parse(message.data)---->', data)
  console.log('data.type---->', data.type_mes, '\n')
  console.log('data.message.rand_name---->', data.message.rand_name, '\n')

  if(data.type_mes == 'offer' && data.message.rand_name == rand_name) {
    document.getElementById('offer-sdp').value  = JSON.stringify(data.message.message)

    createAnswer()
    setTimeout(() => sendAnswer(), 10000);
  }
}

document.getElementById('create-answer').addEventListener('click', createAnswer)
