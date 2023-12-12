
function generate(){
    var characters = ["cinna_teacup.png", "hello_kitty.png", "kuromi.png", "melody.png", "pompom.png"];
    var num = Math.floor(Math.random() * characters.length) //Math.random generates a random number between 0 and 1
    var char = document.getElementById("chosen")
    console.log(characters.length)
    console.log(num)
    char.style.visibility = "hidden"
    char.src = "/image/" + characters[num]
    char.style.visibility = "visible"
}