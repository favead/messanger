const styles = {
  friendItem: 'friend-item-messanger',
  friendItemOpenedMessages: 'active-li-messages',
  mainBlock: 'message-card-body',
  messageField:'messages-field',
  messageInputField: 'message-text-field',
  messageButtonField: 'send-message-field-btn',
  message: "message",
  fromYou: "message-from-you",
}

const URLS = {
  createMessage: 'messages/create',
  getMessages: 'messages',
  updateMessage: 'messages/update',
  getUserId: 'auth/getId'
}

$('document').ready(function(){
  documentReadyHandler()
})

const documentReadyHandler = () => {
  let friends = $(`.${styles.friendItem}`)
  friends.click(friendClickHandler)
}

const getUserId = () => {
  return $(`.${styles.friendItemOpenedMessages}`)[0].id
}

const friendClickHandler = (e) => {
  toggleActiveClass(e)
  removeElemsFromMainBlock()
  $(`.${styles.mainBlock}`).append($(messagesTemplate(getUserId())))
  showMessageHistory()
  $(`.${styles.messageButtonField}`).click(sendClickHandler)
}

const showMessageHistory = () => {
  let id = getUserId()
  let data = JSON.stringify({'user_id': id})
  
  const callback = (data) => {
    data = parseData(data)
    data.forEach((message)=>{
      showMessage(message)
    })
  }

  sendRequest(URLS.getMessages, data, callback)

}

const sendClickHandler = (e) => {
  let messageContent = $(`.${styles.messageInputField}`)[0]
  let id = getUserId()
  let data = JSON.stringify({'user_id': id, 'content': messageContent.value})
  messageContent.value = ''
  const callback = (data) => {
    data = parseData(data)
    if (data) {
      showMessage(data)
    }
  }
  sendRequest(URLS.createMessage, data, callback)
}

const showMessage = (data) => {
  $(`.${styles.messageField}`).append($(messageTemplate(data)))
  if (data.author == getAuthorId()) {
    $(`.${styles.message}#${data.id}`).addClass(styles.fromYou)
  }
}

const toggleActiveClass = (e) => {
  e.currentTarget.classList.remove(styles.friendItemOpenedMessages)
  e.currentTarget.classList.add(styles.friendItemOpenedMessages)
}

const messageTemplate = (data) => (
  `<div class="${styles.message}-wrapper">
      <div class="${styles.message}" id="${data.id}">
        <p> ${data.content} </p>
      </div>
  </div>`
)

const messagesTemplate = (currentUserId) => (`
  <div class="messages-field">
  </div>
  <div class="send-message-field">
    <div class="send-message-field-text">
      <textarea name="message" id="${currentUserId}" class="form-control ${styles.messageInputField}"></textarea>
      <button class=" ${styles.messageButtonField} btn btn-primary">Send</button>
    </div>
  </div>
`)

const removeElemsFromMainBlock = (stopBlock=null) => {
  const mainBlock = $(`.${styles.mainBlock}`)
  const stopCounter = stopBlock || 0
  const childrens = mainBlock.children()
  let c = childrens.length
  while(c > stopCounter) {
    mainBlock.children().last().remove()
    --c;
  }
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


const parseData = (data) => {
  return data.data
}


const addClickHandlerForBtn = (btnClass, handler) => {
  btnList = $(`.${btnClass}`)
  btnList.click(handler)
}


const appendElemToMainBlock = (elemInnerHtml, classElem) => {
  const elem = $(elemInnerHtml).addClass(classElem)
  $(`.${styles.mainBlock}`).append(elem)
}

const getAuthorId = function current_id() {
  let CURRENT_USER_ID = null 
  sendRequest(URLS.getUserId, null, (data) => {
    if (data.id) {
      CURRENT_USER_ID = data.id
    }
  })
  const getCurrentId = () => {
    return CURRENT_USER_ID
  }
  return getCurrentId
}()