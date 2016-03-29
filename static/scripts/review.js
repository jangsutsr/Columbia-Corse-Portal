// JS to update form action for rating a particular review

$('#rateareview').on('click', function (event) {
  var rid = $('#rateareview').data('rid') // Get the rid that was clicked
  var act = document.getElementById('rate-review').action
  act = act.concat('/'+rid)
  // update the action with the correction URI
  document.getElementById('rate-review').setAttribute("action", act)
})

// JS to update form action for rating a particular review
$('#rateadocument').on('click', function (event) {
  var did = $('#rateadocument').data('did') // Get the rid that was clicked
  var act = document.getElementById('rate-document').action
  act = act.concat('/'+did)
  // update the action with the correction URI
  document.getElementById('rate-document').setAttribute("action", act)
})
