// $.get("/Grammar_data", function (grammar_result) {
//   console.log(grammar_result.length);
// });
$.ajax({
  url: "/Grammar_data",
  type: "GET",
  dataType: "json",
  success: function (Jdata) {
    // alert("SUCCESS!!!");
    console.log(Jdata.length);
    for (var i = 0; i < Jdata.length; i++) {
      console.log(Jdata[i]["Title"]);
    }
  },

  error: function () {
    // alert("ERROR!!!");
    console.log("傳遞文法資料錯誤");
  },
});
