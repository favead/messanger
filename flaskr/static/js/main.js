const searchInput = `
  <form method="post" class="search-profile">
    <input type="text" class = "form-control search-input-profile" name = "search" id="search" 
    placeholder="Find for new friends"
    required >
  </form>
`


const URLS = {
  getAllFriends: 'friends',
  getAllFriendRequests: 'requests',
  acceptFriendRequest: 'requests/update',
  getAllUsersByPartOfName: 'search',
  sendFriendRequest: 'requests/create'
}


const friendRequests = `
  <div class="card-body">
    <ul class="list-group list-group-flush">
    </ul>
  </div>
`


const styles = {
  'btnsBlock':'form-row-profile',
  'searchSectionBtn': 'search',
  'requestSectionBtn': 'fr-req',
  'mainBlock': 'friend-list-profile',
  'forSearchInput': 'search-input',
  'forSearchResults': 'search-results-div',
  'forSearchResult': 'search-result',
  'forSearchResultText': 'search-result-text',
  'forSearchResultButton': 'search-result-btn',
  'forRequests': 'requests-div',
  'forRequest': 'request-div',
  'forRequestText': 'request-text',
  'forRequestBtn': 'request-btn',
  'forActiveSectionBtn': 'btn-profile-active'
}


const generateTemplateForUserInfo = (divClass, pClass, btnClass, username, btnValue) => {
  return `
    <li class="list-group-item search-item-profile">
      <div class = ' ${divClass} '>
        <p class = "tmp-p ${pClass}">Username: ${ username }</p>
        <button class = 'btn btn-primary btn-info-template ${btnClass}' >${btnValue}</button>
      </div>
    </li>
  `
}

// functions above its only const variables which i do not need to change.

//const send_request = (callback, url, body) => {
//}

// main function which handle all 
const documentReadyHandler = () => {
  const searchButton = $(`#${styles.searchSectionBtn}`)
  const requestButton = $(`#${styles.requestSectionBtn}`)
  requestButton.addClass(styles.forActiveSectionBtn)
  searchButtonClickHandler()
  searchButton.click(searchButtonClickHandler)
  requestButton.click(requestButtonClickHandler)
}


const keyUpSearchInputHandler = (e) => {
  let partOfName = e.target.value
  console.log(partOfName)
  if(partOfName === ''){
    removeElemsFromMainBlock(2)
  } else {
    const url = URLS.getAllUsersByPartOfName
    const body = JSON.stringify({'search':partOfName})
    sendRequest(url, body, keyUpSearchInputCallback)
  }
}


const keyUpSearchInputCallback = (data) => {
  console.log('answer')
  removeElemsFromMainBlock(2)
  users = parseData(data)
  users.forEach((user)=> {
    let li = generateTemplateForUserInfo(
      styles.forSearchResult,
      styles.forSearchResultText,
      styles.forSearchResultButton,
      user.username,
      'Add'
    )
    appendElemToMainBlock(li, '')
  })
  const handler = (e) => {
    let wrapElem = e.currentTarget.parentElement || e.currentTarget.parent()
    const username = wrapElem.children[0].outerText.split(': ')[1]
    const url = URLS.sendFriendRequest
    const body = JSON.stringify({'username': username})
    sendRequest(url, body, (data)=>{return null})
    wrapElem.parentElement.remove()
  }
  addClickHandlerForBtn(styles.forSearchResultButton, handler)
}


const searchButtonClickHandler = () => {
  toggleClassListForBtns()
  removeElemsFromMainBlock()
  appendElemToMainBlock(searchInput, styles.forSearchInput)
  searchInputElement = $(`.${styles.forSearchInput}`)
  searchInputElement.on('input', keyUpSearchInputHandler)
}


const requestButtonClickHandler = () => {
  toggleClassListForBtns()
  removeElemsFromMainBlock()
  getAllFriendRequests()
}

const getAllFriendRequests = () => {
  const url = URLS.getAllFriendRequests
  const body = JSON.stringify(null)
  sendRequest(url, body, getAllFriendRequestsCallback)
}


const getAllFriendRequestsCallback = (data) => {
  removeElemsFromMainBlock(2)
  let friendRequests = parseData(data)
  friendRequests.forEach((item) => {
    let li = generateTemplateForUserInfo(
      styles.forRequest,
      styles.forRequestText,
      styles.forRequestBtn,
      item.username,
      'Accept'
    )
    appendElemToMainBlock(li, '')
  })
  const handler = (e) => {
    let wrapElem = e.currentTarget.parentElement || e.currentTarget.parent()
    const username = wrapElem.children[0].outerText.split(': ')[1]
    const url = URLS.acceptFriendRequest
    const body = JSON.stringify({'username': username})
    sendRequest(url, body, (data)=>{return null})
    wrapElem.parentElement.remove()
  }
  addClickHandlerForBtn(styles.forRequestBtn, handler)
}


const addClickHandlerForBtn = (btnClass, handler) => {
  btnList = $(`.${btnClass}`)
  btnList.click(handler)
}


const appendElemToMainBlock = (elemInnerHtml, classElem) => {
  const elem = $(elemInnerHtml).addClass(classElem)
  $(`.${styles.mainBlock}`).append(elem)
}


const removeElemsFromMainBlock = (stopBlock=null) => {
  const mainBlock = $(`.${styles.mainBlock}`)
  const stopCounter = stopBlock || 1
  const blockWithButtons = stopBlock || $(`.${styles.btnsBlock}`)
  const childrens = mainBlock.children()
  let c = childrens.length
  while(c > stopCounter) {
    mainBlock.children().last().remove()
    --c;
  }
}


const parseData = (data) => {
  return data.data
}


const toggleClassListForBtns = () => {
  const searchButton = $(`#${styles.searchSectionBtn}`)
  const requestButton = $(`#${styles.requestSectionBtn}`)
  const btns = [searchButton, requestButton]
  btns.forEach((btn)=>{
    btn.toggleClass(styles.forActiveSectionBtn)
  })
}


const sendRequest = (url, body, callback) => {
  $.ajax({
    method: "POST",
    url: url,
    data: body,
    contentType: 'application/json; charset=utf-8'
  })
  .done(callback)
}

$('document').ready(function(){
  documentReadyHandler()
})