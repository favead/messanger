const search = `
<form method="post" class="search-profile">
  <input type="text" class = "form-control search-input-profile" name = "search" id="search" 
  placeholder="Find for new friends"
  required >
</form>
`


const userInfoTemplate = (id, username, email, btnValue) => {
  return `
    <li class="list-group-item search-item-profile">
      <div class = "tmp">
        <p class = "tmp-p">Username: ${ username }</p>
        <button class = "btn btn-primary btn-info-template" id = ${id} >${btnValue}</button>
      </div>
    </li>
  `
}


const requests = `
<div class="card-body">
  <ul class="list-group list-group-flush">
  </ul>
</div>`


const requestClass = 'request-friends-div'
const searchClass = 'search-friends-div'


function toggleClassList(e){
  btn = document.querySelectorAll('.btn-profile-active')
  btn.forEach((elem)=>{
    elem.classList.remove('btn-profile-active')
  })
  e.target.classList.toggle('btn-profile-active')
}


function createBlock(classStr, inner, block) {
  let div = document.createElement('div')
  div.classList.add(classStr)
  div.innerHTML = inner
  block.appendChild(div)
}


function start() {
  get_data_about_requests()

  const searchDiv = document.createElement('div')
  searchDiv.innerHTML = search
  const btnSearch = document.getElementById('search')
  const btnFrReq = document.getElementById('fr-req')
  const block = document.querySelector('.friend-list-profile')
  btnSearch.classList.toggle('btn-profile-active')
  const btns = document.querySelector(".button-switch-profile")

  searchLogic(block, btnFrReq, btnSearch)

  btns.addEventListener('click', function(e) {
    if (e.target === btnFrReq) {
      deleteBlocks(block, searchClass, 'user-search-res')
      toggleClassList(e, btnSearch, btnFrReq)
      createBlock(requestClass, requests, block)
    }
    if (e.target == btnSearch){
      toggleClassList(e, btnSearch, btnFrReq)
      searchLogic(block, btnFrReq, btnSearch)
    }
  })


}


function deleteBlocks(block, class1, class2 = null){
  k = document.querySelectorAll(`.${class1}`)
  if (k) {
    k.forEach((elem)=>{
      block.removeChild(elem)
    })
  }
  b = document.querySelectorAll(`.${class2}`)
  console.log(b)
  if (b.length > 0) {
    b.forEach((elem)=>{
      block.removeChild(elem)
    })
  }
}


function searchLogic(block, btnFrReq, btnSearch){
  deleteBlocks(block, requestClass)
  createBlock(searchClass, search, block)
  const searchInput = document.querySelector('.search-input-profile')
  searchInput.addEventListener('keyup', function(e) {
  let search = e.target.value
  if (!search) {
    k = document.querySelector(`.user-search-res`)
    if (k) {
      block.removeChild(k)
    }
    } else {
      let jsondata = JSON.stringify({'search': search})
      let data = null
      send_search_request(jsondata, 'search', block)
    }
    addFriendBtn = document.querySelectorAll()
  })
}


function get_requests(){
  if (get_data_about_requests()) {
  }
}


function get_data_about_requests(){
  const data = send_request(null, 'requests')
  return data
}

function send_search_request(jsondata, url, block) {
  callb = (data, block) => {
    data = JSON.parse(data).data
    if (data) {
      showSearchResults(block, data, searchClass)
    } else {
      k = document.querySelector(`.user-search-res`)
      if (k) {
        block.removeChild(k)
      }
    }
  }
  send_request(jsondata, url, callb, block)
}


function send_request(body, url, callback, block) {
  const xhr = new XMLHttpRequest()
  let data = null
  xhr.open('POST', url)
  xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
  xhr.onreadystatechange = function() {
    if(xhr.readyState != 4){
      return;
    }
    data = xhr.response
    if (callback){
      callback(data, block)
    }
  }
  if (body) {
    xhr.send(body)
  } else {
    xhr.send()
  }
}

function showSearchResults(block, data, blockClass) {
  k = document.querySelector(`.user-search-res`)
  if (k) {
    block.removeChild(k)
  }
  data.forEach((item, i)=>{
    arr = item[`${i}`]
    k = userInfoTemplate(arr[0], arr[1], arr[2], 'Send request')
    createBlock('user-search-res', k, block)
  })
}


document.addEventListener('DOMContentLoaded',start)


let b = `
{% if users %}
  <div class="search-results card-form">
    <div class="card-body">
      <ul class="list-group list-group-flush">
        {% for user in users %}
          <li class="list-group-item">Username: {{ user.username }}</li>
          <li class="list-group-item">Email: {{ user.email }}</li>
          <form action="/profile/add_friend" method="post">
            <input type="hidden" value="{{ user.username }}" name = "username" required>
            <input type="hidden" value="{{ user.email }}" name = "email" required>
            <button type="submit" class = "btn btn-primary">Add friend</button>
          </form>
        {% endfor %}
      </ul>
    </div>
  </div>        
{% endif %}
`