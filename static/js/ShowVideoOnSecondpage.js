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
                $(document.getElementById("video_list")).html("");
                for(var i = 0; i < data.length; i++){
                //     var top = '{% for result in '+ data +' %}';
                    var content = 
                        '<div class="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12 mb-5">' +
                        '<figure className="effect-ming tm-video-item">' +
                        '<img src="https://img.youtube.com/vi/'+ data[i]["video_id"] +'/mqdefault.jpg" alt="Image" class="img-fluid" />' +
                        '<figcaption class="d-flex align-items-center justify-content-center">' +
                        '<h2>watch</h2>' +
                        '<a href="https://www.youtube.com/watch?v='+ data[i]["video_id"] +'" target="_blank">View more</a>' +
                        '</figcaption></figure>' +
                        '<div class="d-flex flex-column justify-content-between tm-text-gray">' +
                        '<span class="titles"> Title:<em>' + data[i]["Title"] + '</em> </span>' +
                        '<span class="keywords"> Keywords:<em>' + data[i]["keywords"] + '</em> </span>' +
                        '</div> </div>';
                    // var end = '{% endfor %}'
                    var result = content
                    $(document.getElementById("video_list")).append(result)
                };
            },
            error: function (error) {
                alert("error");
            },
        });
    }

}