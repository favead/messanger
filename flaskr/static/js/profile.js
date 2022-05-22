const search = `
<form action="/profile/" method="post" class="search-profile">
  <input type="text" class = "form-control search-input-profile" name = "search" id="search" 
  placeholder="Find for new friends"
  required >
  <input type="submit" value="Search" class="btn btn-primary">
</form>
`

const requests = `
<div class="card-body">
  <ul class="list-group list-group-flush">
      <li class="list-group-item">Username: {{ user.username }}</li>
      <li class="list-group-item">Email: {{ user.email }}</li>
      <button class = "btn btn-primary">Accept</button>
  </ul>
</div>`

const requestClass = 'request-friends-div'
const searchClass = 'search-friends-div'


function toggleClassList(e, btnSearch, btnFrReq){
    [btnSearch, btnFrReq].forEach((elem)=>{
      elem.classList.remove('btn-profile-active')
    })
    e.target.classList.toggle('btn-profile-active')
}

function start() {

  const searchDiv = document.createElement('div')
  searchDiv.innerHTML = search

  const btnSearch = document.getElementById('search')
  const btnFrReq = document.getElementById('fr-req')
  const block = document.querySelector('.friend-list-profile')
  btnSearch.classList.toggle('btn-profile-active')
  const btns = document.querySelector(".button-switch-profile")
  
  btns.addEventListener('click', function(e) {
    if (e.target === btnSearch || e.target ===  btnFrReq){
      toggleClassList(e, btnSearch, btnFrReq)
    }
    if (e.target === btnFrReq) {
      let div = document.createElement('div')
      div.classList.add(requestClass)
      div.innerHTML = requests;
      block.appendChild(div)
    }
    if (e.target == btnSearch){
      block.removeChild(document.querySelector(`.${requestClass}`))
    }
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