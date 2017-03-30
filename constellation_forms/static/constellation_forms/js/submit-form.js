/* exported submitForm */

$('.mdl-textfield__input').one('blur keydown', function() {
  $(this).parent().addClass('touched');
});

/**
 * Turns on invalid CSS for every textfield,
 * regardless of whether it's been entered yet
 */
function turnOnValidCSS() {
  $('.mdl-textfield__input').each(function() {
    $(this).parent().addClass('touched');
  });
}

/**
 * Validate a widget
 */
function validate(elem) {
  return elem.get()[0].checkValidity();
}

/**
 * Collect the widgets and submit them to the backend
 */
function submitForm() {
  turnOnValidCSS();
  let widgetForm = {'widgets': []};
  let i = 0;
  let csrfToken = $.cookie('csrftoken');
  let valid = true;
  $('#widgets-holder').find('form').each(function() {
    if (valid && !validate($(this))) {
      $('.mdl-layout').animate({
        scrollTop: $(this).offset().top - $('.mdl-layout__content').offset().top,
      }, 200);
      valid = false;
    }
    let widget = $(this).serializeArray();
    if (widget.length > 0) {
      widgetForm.widgets[i++] = $(this).serializeArray()[0]['value'];
    }
  });
  if (!valid) {
    return false;
  }
  let data = {
    'csrfmiddlewaretoken': csrfToken,
    'data': JSON.stringify(widgetForm),
  };
  $.post($(location).attr('href'), data, function(response) {
    window.location.href = '/forms/view/list-submissions';
  });
}
