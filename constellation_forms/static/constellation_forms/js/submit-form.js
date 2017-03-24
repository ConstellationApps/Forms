/* exported addWidget deleteWidget addChoice deleteChoice submitForm */

/**
 * Collect the widgets and submit them to the backend
 */
function submitForm() {
  let widgetForm = {'widgets': []};
  let i = 0;
  let csrfToken = $.cookie('csrftoken');
  $('#widgets-holder').find('form').each(function() {
    console.log($(this).serializeArray());
    widgetForm.widgets[i++] = $(this).serializeArray()[0]['value'];
  });
  let data = {
    'csrfmiddlewaretoken': csrfToken,
    'data': JSON.stringify(widgetForm),
  };
  $.post($(location).attr('href'), data, function(response) {
    window.location.href = response.url;
  });
}
