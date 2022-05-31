searchCallback = (data, block) => {
  data = parseData(data)
}


parseData = (data) => {
  return JSON.parse(data).data
}


const styles = {
  'forSearchInput': 'search-input',
  'forSearchResults': 'search-results-div',
  'forSearchResult': 'search-result',
  'forSearchResultText': 'search-result-text',
  'forSearchResultButton': 'search-result-btn',
  'forRequests': 'requests-div',
  'forRequest': 'request-div',
  'forRequestText': 'request-text',
  'forRequestBtn': 'request-btn'
}


const generateTemplateForUserInfo = (classname, username, btnValue) => {
  return `
    <li class="list-group-item search-item-profile">
      <div class = ' ${classname} '>
        <p class = "tmp-p">Username: ${ username }</p>
        <button class = 'btn btn-primary btn-info-template' >${btnValue}</button>
      </div>
    </li>
  `
}


const send_request = (callback, url, body) => {
}