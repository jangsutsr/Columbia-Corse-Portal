$(document).ready(function() {
	$('.select-school').select2({
		placeholder: "School",
	});
});

//send authentication info to server
$('#user-log-in').click(function(event) {
	event.preventDefault();
	var data = $('#user-login-form').serializeArray();	
	var usrName = data;
	$.ajax({
		url: '/login',
		type: 'POST',
		data: data,
		dataType: 'json',
		success: function(response) {
			if (response.redirect) {
				window.location.href = response.url;	
			} else {
				if ($('#user-log-in').next().length === 0) {
					$('#user-log-in').after('<p style="color:red;">Incorrect UNI/password</p>');	
				}
			}
		},
		error: function(error) {
			console.log(error);		
		}
	});	
});

// Validate email address format.
$('#user-register-form input:eq(1)').focusout(function() {
	var pattern = /@columbia[.]edu$|@barnard[.]edu$/;
	var warningMsg = $(this).next();
	var isValid = true;
	if (!pattern.test($(this).val())) {
		isValid = false;
	}
	if (isValid) {
		if (warningMsg.length !== 0) {
			warningMsg.remove();	
		}	
	} else {
		$(this).val('');	
		if (warningMsg.length === 0) {
			$(this).after('<p style="color:red;">Invalid Email</p>');	
		}
	}
});

// Validate password format
$('#user-register-form input:eq(2)').focusout(function() {
	var passwd = $(this).val();
	var patterns = [/[0-9]/, /[a-z]/, /[A-Z]/];
	var warningMsg = $(this).next();
	var isValid = true;
	if (passwd.length < 6 || passwd.length > 15) {
		isValid = false;	
	} else {
		for (var i=0; i < patterns.length; i++) {
			if (!patterns[i].test(passwd))	{
				isValid = false; break;	
			}
		}	
	}
	if (!isValid) {
		$(this).val('');
		if (warningMsg.length === 0) {
			$(this).after('<p style="color:red;">Invalid password</p>');	
		}
	} else if (warningMsg.length !== 0) {
		warningMsg.remove();	
	}
});

// Submit new user sign-up information
$('#user-sign-up').click(function() {
	var toCheck = $('#user-register-form').serializeArray();	
	var data = {};
	var isValid = true;
	var warningMsg = $(this).next();
	for (var i=0; i < toCheck.length; i++) {
		if (toCheck[i]['value'] === '')	{
			isValid = false; break;	
		} else {
			data[toCheck[i]['name']] = toCheck[i]['value'];	
		}
	}
	if (isValid) {
		if (warningMsg.length !== 0) {
			warningMsg.remove();		
		};	
		$.ajax({
			url: '/register',
			type: 'POST',
			data: data,
			success: function(response) {
				console.log(response);	
			},
			error: function(error) {
				console.log(error);	
			}
		});	
	} else {
		if (warningMsg.length === 0) {
			$(this).after('<p style="color:red;">Please fill out all fields.</p>')	
		}	
	}
});

