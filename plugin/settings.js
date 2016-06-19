
  $(document).ready(function() {  
   			chrome.storage.sync.get('logged', function(data) {if (data.logged==1){

   	 		$('#login').addClass('invisible');
   	  		$('#id').addClass('invisible');
   	  		$('#logout').removeClass('invisible');
   	  		$('#info').addClass('invisible');
   	  		$('#logged_info').removeClass('invisible');

   	  	}
   	  	else {
   	  			$('#logged_info').addClass('invisible');


   	  	}
   	  });
      

   		$('#logout').addClass('invisible');
   		$('#login').prop('disabled',true);  

   		$('#id').on('input',function() { var myLength = $("#id").val().length;

        if(myLength == 36){   $('#login').prop('disabled',false); }

  			} );


   		//login click function
    $('#login').click(function() {  
    	id=$('input').val();
    	alert(id);
    	var data={'id':id}
//call ajax post to get contacts

	  
	 $.ajax({
  type: "POST",
  url: 'https://localhost:8000/contacts',
  data: JSON.stringify(data),
  success: function(data){


  			var feed; feed=data.result[0]['contacts'];  

  			alert("contacts"+JSON.stringify(feed));	
  			alert(feed);
  			 

  			chrome.storage.sync.set({'contact_list': JSON.stringify(feed)}, function() { alert("Name list saved");});		
	  			
  			// var name_list=[];var mail_list=[];
	  		// 	for (var i=0;i<feed.length;i++)
	  		// 	{
	  		// 		name_list.push(feed[i]['name']);//alert("name:"+entry['name']);
	  		// 		mail_list.push(feed[i]['email']);
	  		// 	}
	  		// 	alert('name[0]'+name_list[0]);
	  		// 	alert('mail[0]'+mail_list[0]);
	  		// 	alert(name_list);


	  			   // chrome.storage.sync.set({'contact_name': JSON.stringify(name_list)}, function() { alert("Name list saved");});		
	  			   // chrome.storage.sync.set({'contact_mail': JSON.stringify(mail_list)}, function() { alert("Mail list saved");});		

   			   // 	chrome.storage.sync.get('contact_name',function(data){dataList=JSON.parse(data.contact_name); alert("d:"+data.contact_name[0]);});









				 
    			


},
  contentType: 'application/json;charset=UTF-8'
});

    	url="https://localhost:8000/auth"
    	$.ajax({
 			 type: "POST",
  			 url: url,
  
  			 success: function(data){ alert(data);

  			 	if(data=="1"){


  		  
       				 // Get a value saved in a form.
       				 var theValue = $('input').val();
       				 // Check that there's some code there.
      
        			// Save it using the Chrome extension storage API.
        			 chrome.storage.sync.set({'id': theValue}, function(data) {	alert(data);});		
        			 chrome.storage.sync.set({'logged': 1}, function() {
         			 // Notify that we saved.
         			  alert('loggedin');
         			  $('#login').addClass('invisible');
   	  		$('#id').addClass('invisible');
   	  		$('#logout').removeClass('invisible');
   	  		$('#info').addClass('invisible');
   	  		$('#logged_info').removeClass('invisible');

        					});

         				chrome.storage.sync.get('id', function(data) { alert('stored id:'+ data.id); });
        
      
         					}
		
		     	 else alert("Error!Cannot login");},
  				data: JSON.stringify(data),
  				contentType: 'application/json;charset=UTF-8'

			});

   			}); //login click ends 



    //logout button click
    $('#logout').click(function(){

    	
    						     chrome.storage.sync.set({'logged': 0}, function() { });		

    		        			 chrome.storage.sync.remove('id',function(){alert("Logged out ");});	
    		        			 chrome.storage.sync.remove('contact_mail',function(){alert("Removed  mail");});	
    		        			 chrome.storage.sync.remove('contact_name',function(){alert(" Removed name ");});	


   	 		$('#login').removeClass('invisible');
   	  		$('#id').removeClass('invisible');
   	  		$('#logout').addClass('invisible');
   	  		$('#info').removeClass('invisible');
   	  		$('#logged_info').addClass('invisible');




    });


  		} );

 