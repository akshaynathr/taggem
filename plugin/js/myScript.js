 



window.onload=function() {


	var dataList;
	chrome.storage.sync.get('contact_list',function(data){dataList=(data.contact_list);  
	var jList=JSON.parse(dataList);
 
	 
	var usernames = new Bloodhound({
    	datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    	queryTokenizer: Bloodhound.tokenizers.whitespace,
    	local:jList
                    //$.map(data, function (name) {
     //    return {

     //      	  name: name

     //   	 		};
    		
		});
usernames.initialize();


// $('#friendList').tagsinput({
//     typeaheadjs: [{
//           minLength: 0,
//           highlight: false,
//     },{
//         minlength: 3,
//         name: 'userames',
//         displayKey: 'name',
//         valueKey: 'name',
//         source: usernames.ttAdapter()
//     }],
//     freeInput: false
// });

var elt = $('#friendList');
elt.tagsinput({
  itemValue: 'email',
  itemText: 'name',
  typeaheadjs: {
    name: 'users',
    displayKey: 'name',
    templates: {
    empty: [
      '<div class="empty-message">',
        'unable to find any of your friend',
      '</div>'
    ].join('\n'),
    suggestion: function(data) {
    return '<p><strong>' + data.name + '\n'+'</strong> ' + data.email + '</p>';}
  },
    source: usernames.ttAdapter()
    
  }
});
   
}); //function callback ends//////////////////////////////////////////////////////////////////////////

$('#main_row').hide().fadeIn(2000);

//$('#friendList').change(function() { $("#loading").removeClass("invisible"); });

var tagbtn= document.getElementById('tagbtn');

 var url;
	 var title;

	 var queryInfo = {
    active: true,
    currentWindow: true
  };
	 chrome.tabs.query(queryInfo, function(tabs) {
     
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
      
     title=tab.title;

      var message= document.getElementById('message');

      message.value=title;
    


}
);
 

tagbtn.addEventListener('click',test);
function test()
{		

	

	chrome.storage.sync.get('logged', function(data) {if(data.logged==0){window.location='settings.html';}      else { 
		//get auth id from storage
	var id;
	chrome.storage.sync.get('id', function(data) { id=data.id;});


	//get handle to input box and button
	var friendList=document.getElementById('friendList');
	 var message= document.getElementById('message');

	 var friend= $('#friendList').tagsinput('items');

	 var recepient=[];
	 for(var i in friend){
	 
	 	recepient.push(friend[i]['email']);

	 }

	 alert(recepient);

		 //check any of them is empty
	 frndVal=friendList.value;
	 msgVal=message.value;
	 if(frndVal.trim()=='') { alert("Enter friends");}

	 else if(msgVal.trim()==''){ alert("No message entered");}

	 else{






	
	 
	 // //alert(friend);
	 var url;
	 var title;

	 var queryInfo = {
    active: true,
    currentWindow: true
  };
	 chrome.tabs.query(queryInfo, function(tabs) {
     
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
     url = tab.url;
      

	   //  alert(url);

	 function success(data) {if(data=="Error"){alert("Error in sending. please try again")} else { alert("Your friends are tagged :)");  $('#loading img').attr('src','tick.png');}}


	 var bundle= {'msg':message.value, 'link':url, 'id':id,'recepient':recepient }
	 var data=bundle;//JSON.stringify(bundle);
	 //alert(data);
	 $('#tagbtn').remove();
	 $('#loading').removeClass('invisible');
	 
	 $.ajax({
  type: "POST",
  url: 'https://localhost:8000/mail',
  data: JSON.stringify(bundle),
  success: success,
  contentType: 'application/json;charset=UTF-8'
});
}
);

}
}//function test ends

} );//function chrome ends

}

}
 