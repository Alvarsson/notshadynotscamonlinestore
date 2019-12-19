function search(e) {
    e.addEventListener("input", function() {

        var req = new XMLHttpRequest();
        req.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200) {
                var res_arr = JSON.parse(this.response).data;
                showSearchList(e, res_arr);
            }
        }
        req.open('POST', '/search', true);
        req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        req.send('search_string='+this.value);
    });
}
function showSearchList(e, arr) {
    closeAllLists();
    var currentFocus, a, b, i;
    
    a = document.createElement("div");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    document.getElementById("search_div").appendChild(a);
    for(i = 0; i < arr.length; i++) {
        b = document.createElement('div');
        b.innerHTML = '<a href="/article/' + arr[i][0] + '">' + arr[i][1] + '</a>';
        a.appendChild(b);
    }
}
function closeAllLists() {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
            x[i].parentNode.removeChild(x[i]);
    }
}
document.addEventListener("click", function () {
   closeAllLists();
});
search(document.getElementById("myInput"));
