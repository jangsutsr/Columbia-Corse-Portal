// JS to update form action for rating a particular review
$("[id^=rateareview]").on('click', function (event) {
  // alert(jQuery(this).attr('action'))
  var rid = jQuery(this).data('rid') // Get the rid that was clicked
  var act = $("#rate-review").attr('action')
  // jQuery(this).attr('action', 'page2')
  act = act.concat('/'+rid)
  // update the action with the correction URI
  $("#rate-review").attr('action', act)
})

// JS to update form action for rating a particular review
$("[id^=rateadocument]").on('click', function (event) {
  // alert(jQuery(this).attr('action'))
  var rid = jQuery(this).data('did') // Get the rid that was clicked
  var act = $("#rate-document").attr('action')
  // jQuery(this).attr('action', 'page2')
  act = act.concat('/'+rid)
  // update the action with the correction URI
  $("#rate-document").attr('action', act)
})
