/* exported submitForm */

const message = document.querySelector('#message-toast');

$(function() {
  setupValidation();
  $('.datefield').datepicker({
    onSelect: function() {
      $(this)[0].parentElement.MaterialTextfield.checkValidity();
      $(this)[0].parentElement.MaterialTextfield.checkDirty();
    },
  });
  $('.slider-widget').each(function() {
    updateSliderTooltip($(this));
  });
});

/**
 * Updates the tooltip of a slider with its value
 * @param {Object} container - The element containing the slider
 */
function updateSliderTooltip(container) {
  let value = container.find('.mdl-slider').val();
  container.find('.mdl-tooltip output').html(value);
}

/**
 * Run handlers to make forms check validation only after
 * the user has clicked inside the field
 */
function setupValidation() {
  $('.mdl-textfield__input').one('blur keydown', function() {
    $(this).parent().addClass('touched');
  });
  $('.getmdl-select .mdl-textfield__input').on('focusin', function() {
    $(this).prop('readonly', true);
  });
  $('.getmdl-select .mdl-textfield__input').on('focusout', function() {
    $(this).prop('readonly', false);
  });
}

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
 * Get values from a widget
 */
function getWidgetValue(widget) {
  let inputs = widget.find('input');
  if(inputs.length == 1 || (inputs.length == 0 && widget.find('textarea').length > 0) || (inputs.length == 2 && widget.find('input').length > 0)) {
    return widget.serializeArray()[0]['value'];
  } else {
    let returnArray = [];
    for (const input of inputs) {
      if(input.checked) {
        returnArray.push($('label[for="' + input.id + '"] .choice-label')[0].textContent);
      }
    }
    return returnArray;
  }
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
      widgetForm.widgets[i++] = getWidgetValue($(this));
    } else {
      widgetForm.widgets[i++] = null;
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
  })
  .fail(function(jqXHR) {
    message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
  });
}
