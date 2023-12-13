/*
""" --------------------------------- Database Format -----------------------------------------
    DB["COLLECTION_USERS"] - Stores Emails -- {username: '', password: ''}
    DB["COLLECTION_TOKENS"] - Stores Any Tokens -- {username: '', authToken: ''}
    DB["COLLECTION_EMAILS"] - Stores Emails -- {username: '', password: '', email: ''}
    DB["COLLECTION_LISTINGS] - Stores All Listings -- format is a dictionary marked below
    {creator: '', creator_token: '', time_remaining: '', open: bool, bidders: [], winner: '', bid: int}
    ---------------------------------  ---------------- -----------------------------------------
"""
*/

let socketio = io();

function create_listing(){
  /*
    This function reads the inputs that were typed in by the user.
    Sends it over to the back-end so the server can create the listing.
   */
  console.log("sending create listing info");
  // 1) Collect all the front-end data to create one individual listing
  let title = document.getElementById("l-title");
  title = title.value
  let desc = document.getElementById("l-desc");
  desc = desc.value
  let bid = document.getElementById("l-bid");
  bid = bid.value // Initial bid value
  let endDate = document.querySelector('input[type="datetime-local"]');
  // 2) Create listing values and send to the server
  let img = document.getElementById("img_src")
  img = img.src
  const listing = {'title': title, 'desc': desc, 'bid': bid, 'time': endDate, 'img': img} // Individual listing that will be sent to backend server
  socketio.emit("listing-create", listing)
}

function listing_html(listing_json){
  /* This function will be used fo
  * This function receives a listing as a JSON object and creates the HTML to be displayed
  * {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: [{}],
  * winner: '', bid: int, _id: '', img: '/path/image.format'}
  */
  console.log("Trying to Display This:")
  console.log(listing_json)
  const title = listing_json.title;
  const desc = listing_json.desc;
  const time = listing_json.time;
  const bid= listing_json.bid;
  const lid = listing_json._id;
  const img = listing_json.img;
  const creator = listing_json.creator

  let html = `
    <div class='listing' id="listing_${lid}">
      <h3 class='l-title'>${title}</h3>
      <img class='l-img' src="static/${img}" >
      <p class="l-desc">${desc}</p>
      <input type="tel" id="l-urbid" name="urbid" placeholder="Enter a bid" pattern="[0-9]">
      <button type="button" onclick="">Place Bid</button>
      <button type="button">${bid}</button>
      <p>Time Remaining: <button type="button">${time}</button> </p>
      <button type="button">Author: <span>${creator}</span></button>
      <p class="createdBy">created by <span class="creator">${creator}</span></p>
    </div>
  `


  return html
}

function add_listing(){
  const listing_html_new = listing_html()
}

function placeBid(){
  /* This function is called when user pushes the Place bid button to enter a new bid value */
}

function winner(){

}
// src="{{ url_for('static', filename=filename) }}">

// <div className="listing" id="listing_####">
//             <h3>Roman Shield</h3>
//             <img src="https://www.larpdistribution.com/wp-content/uploads/2020/05/MCI-3312.png">
//             <p>Description Example: This shield is over 1000 years old. Can you believe it? </p>
//             <input type="tel" id="l-urbid" name="urbid" placeholder="Enter a bid" pattern="[0-9]">
//             <button type="button">Place Bid</button>
//             <button type="button">0</button>
//             <p>Time Remaining: <button type="button">0</button> </p>
//             <button type="button">Author: <span>MarcoInThisCase</span></button>
//         </div>

socketio.emit("retrieve_user_listings")
function welcome_auctions_create(){
  /* This function loads as soon as users enter auctions_create.html HTML page.
  * It automatically initiates the web sockets cals to generate stuff for auctions_create
  */
  console.log("Welcome to Auctions Create")
  socketio.emit("retrieve_user_listings")
}
socketio.on("display_user_listings", function (listings_json){
  console.log("displaying user listings from client")
  const gallery_div = document.getElementById("gallery_div_create");
  for (let listing of listings_json){
    let new_html = listing_html(listing)
    gallery_div.innerHTML += new_html
  }
});

function welcome_auctions_won(){
  /* This function loads as soon as users enter auctions_create.html HTML page.
  * It automatically initiates the web sockets cals to generate stuff for auctions_create
  */
}

