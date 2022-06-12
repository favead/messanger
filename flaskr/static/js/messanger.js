const styles = {
  friendItem: 'friend-item-messanger'
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
}

const messageTemplate = `
  <div class="messages-field">
    <p>tet</p>
  </div>
  <div class="send-message-field">
    <div class="send-message-field-text">
      <textarea name="message" id="2" class="form-control message-text-field"></textarea>
      <button class="send-message-field-btn btn btn-primary">Send</button>
    </div>
  </div>
`