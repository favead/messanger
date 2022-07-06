const styles = {
  friendItem: 'friend-item-messanger',
  friendItemOpenedMessages: 'active-li-messages',
  mainBlock: 'message-card-body',
  messageField:'messages-field',
  messageInputField: 'message-text-field',
  messageButtonField: 'send-message-field-btn'
}


$('document').ready(function(){
  documentReadyHandler()
})


const documentReadyHandler = () => {
  let friends = $(`.${styles.friendItem}`)
  friends.click(friendClickHandler)
}


const friendClickHandler = (e) => {
  const userId = e.target.id
  toggleActiveClass(e)
  removeElemsFromMainBlock()
  $(`.${styles.mainBlock}`).append($(messageTemplate(2)))
}


const toggleActiveClass = (e) => {
  e.currentTarget.classList.remove(styles.friendItemOpenedMessages)
  e.currentTarget.classList.add(styles.friendItemOpenedMessages)
}


const messageTemplate = (currentUserId) => (`
  <div class="messages-field">
  </div>
  <div class="send-message-field">
    <div class="send-message-field-text">
      <textarea name="message" id="${currentUserId}" class="form-control message-text-field"></textarea>
      <button class="send-message-field-btn btn btn-primary">Send</button>
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