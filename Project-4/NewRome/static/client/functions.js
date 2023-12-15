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

let socketio = io({transports: ['websocket'], upgrade: true});

function create_listing(page_id){
  /*
    This function reads the inputs that were typed in by the user.
    Sends it over to the back-end so the server can create the listing.
   */
  // 1) Collect all the front-end data to create one individual listing
  let title = document.getElementById(`l-title_${page_id}`);
  title = title.value
  let desc = document.getElementById(`l-desc_${page_id}`);
  desc = desc.value
  let bid = document.getElementById(`l-bid_${page_id}`);
  bid = bid.value // Initial bid value
  let time = document.getElementById(`l-time_${page_id}`)  ;
  time = time.value // Initial time value
  // 2) Create listing values and send to the server
  let img = document.getElementById(`img_src_${page_id}`)
  img = img.src
  const listing = {'title': title, 'desc': desc, 'bid': bid, 'time': time, 'img': img} // Individual listing that will be sent to backend server
  socketio.emit("listing-create", listing)
}

function listing_html(listing_json){
  /* This function will be used fo
  * This function receives a listing as a JSON object and creates the HTML to be displayed
  * {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: [{}],
  * winner: '', bid: int, _id: '', img: '/path/image.format'}
  */
  const title = listing_json.title;
  const desc = listing_json.desc;
  const time = listing_json.time;
  const bid= listing_json.bid;
  const lid = listing_json._id;
  const img = listing_json.img;
  const creator = listing_json.creator
  const winner = listing_json.winner

  let html = `
    <div class='listing' id="listing_${lid}">
      <h3 class='l-title' id="title_${lid}">${title}</h3>
      <img class='l-img' id="img_${lid}" src="/static/${img}" >
      <textarea id="desc_${lid}" name="description" rows="4" cols="40" disabled>${desc}</textarea>
      <input type="number" id="bid_${lid}" class="center" name="urbid" placeholder="Enter a bid" pattern="[0-9]">
      <button type="button" id="place_bid_${lid}" onclick="place_Bid('${lid}')">Place Bid</button>
      <button type="button" id="bid_display_${lid}">${bid}</button>
      <p>Time Remaining: <button id="time_${lid}" type="button">${time}</button> </p>
      <button type="button">Author: <span id="creator_${lid}">${creator}</span></button>
      <br><span class="winner_podium" hidden id="winner_${winner}">Winner: <span >${winner}</span></span>
    </div>
  `

  return html
}


function listing_html_m(listing_json){
  /* This function will be used to display my auctions_create.html
  * This function receives a listing as a JSON object and creates the HTML to be displayed
  * {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: [{}],
  * winner: '', bid: int, _id: '', img: '/path/image.format'}
  */
  const title = listing_json.title;
  const desc = listing_json.desc;
  const time = listing_json.time;
  const bid= listing_json.bid;
  const lid = listing_json._id;
  const img = listing_json.img;
  const creator = listing_json.creator

  let html = `
    <div class='listing' id="listing_m${lid}">
      <h3 class='l-title' id="title_m${lid}">${title}</h3>
      <img class='l-img' id="img_m${lid}" src="/static/${img}" >
      <textarea id="desc_m${lid}" name="description" rows="4" cols="40" disabled>${desc}</textarea>
      <input type="number" id="bid_m${lid}" class="center" name="urbid" placeholder="Enter a bid" pattern="[0-9]" disabled>
      <button type="button" id="place_bid_m${lid}">Place Bid</button>
      <button type="button" id="bid_display_m${lid}">${bid}</button>
      <p>Time Remaining: <button id="time_m${lid}" type="button">${time}</button> </p>
      <button type="button">Author: <span id="creator_m${lid}">${creator}</span></button>
    </div>
  `

  return html
}

function listing_html_w(listing_json){
  /* This function will be used display winnings auctions_won.html
  * This function receives a listing as a JSON object and creates the HTML to be displayed
  * {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: [{}],
  * winner: '', bid: int, _id: '', img: '/path/image.format'}
  */

  const title = listing_json.title;
  const desc = listing_json.desc;
  const time = listing_json.time;
  const bid= listing_json.bid;
  const lid = listing_json._id;
  const img = listing_json.img;
  const creator = listing_json.creator

  let html = `
    <div class='listing' id="listing_w${lid}">
      <h3 class='l-title' id="title_w${lid}">${title}</h3>
      <img class='l-img' id="img_w${lid}" src="/static/${img}" >
      <textarea id="desc_w${lid}" name="description" rows="4" cols="40" disabled>${desc}</textarea>
      <input type="tel" id="bid_w${lid}" class="center" name="urbid" placeholder="Enter a bid" pattern="[0-9]" disabled>
      <button type="button" id="place_bid_w${lid}">Place Bid</button>
      <button type="button" id="bid_display_w${lid}">${bid}</button>
      <p>Time Remaining: <button id="time_w${lid}" type="button">${time}</button> </p>
      <button type="button">Author: <span id="creator_w${lid}">${creator}</span></button>
    </div>
  `

  return html
}

function update_listing(listing_json){
  /*** This function automatically updates listing information ***/
  // Get the new times and bid from the database (listing_json)
  const listing = listing_json
  const id = listing._id;
  const new_time = listing.time;
  const new_bid = listing.bid;
  const winner = listing.winner
  // Get the elements in the web page
  console.log(listing_json)
  console.log("id: " + id)
  console.log("time: " + new_time)
  const elem_time = document.getElementById(`time_${id}`);
  const elem_bid = document.getElementById(`bid_display_${id}`);
  const elem_list = document.getElementById(`listing_${id}`)
  // Update the values to be the correct new ones
  elem_time.innerHTML = new_time;
  elem_bid.innerHTML = new_bid;
  // Update the styling
  if (winner != "") {
    elem_time.style.color = "red";
    const elem_winner = document.getElementById(`winner_${id}`);
    elem_winner.removeAttribute("hidden");
  }
}


function clear_auctions_my(username){
  /*** This function clears the visible history in auctions_create ***/
  const gallery = document.getElementById(`gallery_div_${username}`);
  if (gallery != null){
    gallery.innerHTML = "";
  }
}

function clear_auctions_list(){
  /*** This function clears the visible history in auctions_list ***/
  const gallery = document.getElementById("gallery_div_list");
  if (gallery != null){
    gallery.innerHTML = "";
  }
}

function clear_auctions_won(username){
  /*** This function clears the visible history in auctions_won ***/
  const gallery = document.getElementById(`gallery_div_won_${username}`);
  if (gallery != null){
    gallery.innerHTML = "";
  }
}

function clear_auctions() {
  /*** This function clears the visible history in ALL auctions pages ***/
  clear_auctions_my();
  clear_auctions_won();
  clear_auctions_list();
}

function place_Bid(lid){
  /* This function is called when user pushes the Place bid button to enter a new bid value */
  let price  = document.getElementById("bid_" + lid);
  price = price.value;
  const list =JSON.stringify( {'iditem': lid,'price': price} );// Individual listing that will be sent to backend server
  socketio.emit("update_bid", list);
}

socketio.on("update_bid_client", function (data){
  const id = data.id;
  const new_bid = data.new_bid;
  document.getElementById(`bid_display_${id}`).innerHTML = new_bid;
});

socketio.on("display_user_listings", function (listings_json){
  const username = listings_json[1];
  const listings = listings_json[0];
  clear_auctions_my(username);
  const gallery_div = document.getElementById(`gallery_div_${username}`);
  for (let listing of listings){
    let new_html_m = listing_html_m(listing);
    if (gallery_div != null) {
      gallery_div.innerHTML += new_html_m;
    } // Display my auctions
  }
});

socketio.on("display_updated_listings", function (listings_json){
  const gallery_div = document.getElementById("gallery_div_list");
  for (let list of listings_json){
    update_listing(list); //
  }
})
socketio.on("display_open_listings", function (listings_json){
  clear_auctions_list();
  const gallery_div = document.getElementById("gallery_div_list");
  for (let listing of listings_json){
    let new_html = listing_html(listing);
    if (gallery_div != null){
      gallery_div.innerHTML += new_html;
    }
  }
});

socketio.on("display_won_listings", function (listings_json){
  // console.log("displaying won listings from client")
  // console.log(listings_json)
  const username = listings_json[1];
  const listings = listings_json[0];
  clear_auctions_won(username);
  const gallery_div = document.getElementById(`gallery_div_won_${username}`);
  for (let listing of listings){
    let new_html = listing_html_w(listing);
    if (gallery_div != null){
      gallery_div.innerHTML += new_html;
    }
  }
});

