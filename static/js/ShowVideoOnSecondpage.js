function AskDataFromServer(){
    var keyword = $(document.getElementById("search_bar")).val()
    if (keyword == ""){
        alert("請輸入關鍵字");
    }
    else{
        $.ajax({
            url: "/search",
            type: "POST",
            dataType: "json",
            data:{
                keyword: keyword,
            },
            success: function (data){
                console.log(data)
            }

        });
    }

}