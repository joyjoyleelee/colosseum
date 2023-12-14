/***
    This file will serve all of the functionality for auctions_create path. It does not use web sockets.
    DB["COLLECTION_LISTINGS] - Stores All Listings -- format is a dictionary marked below
    {creator: '', creator_token: '', title: '', desc: '', time: '', open: bool, bidders: {}, winner: '', bid: int,
    _id: '', img: '/path/image.format'}
 ***/

function create_listing() {
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
    let time = document.getElementById("l-time");
    time = time.value // Initial time value
    // 2) Create listing values and send to the server
    let img = document.getElementById("img_src")
    img = img.src
    const listing = {'title': title, 'desc': desc, 'bid': bid, 'time': time, 'img': img} // Individual listing that will be sent to backend server
    // Make post request to create listing to the server
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
        }
    }
    request.open("POST", "/auctions_create/create-listing");
    request.send(JSON.stringify(listing));
}

function update_my_listings(){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {

        }
    }

}