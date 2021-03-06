/* global Handlebars componentHandler widgetPath Sortable formData */
/* exported addWidget deleteWidget addChoice deleteChoice submitForm */

var message = document.querySelector('#message-toast');

/*
 * Enable dragging items around
 */
Sortable.create(document.getElementById('widgets-holder'), {
  animation: 150,
  handle: '.drag-handle',
});


/*
 * Highlight active widget
 */
$('.form-part').click(function() {
  activateFormPart($(this));
});


/**
 * Detect when the user has clicked on a widget and apply some styling to
 * that via the .active-form-part class
 * @param {Object} part - The element to activate
 */
function activateFormPart(part) {
  $('.form-part').removeClass('active-form-part');
  part.addClass('active-form-part');
}

/**
 * Create a new widget from the handlebars template and add it to the
 * form list
 * @param {string} widgetName - Name of the widget to create
 * @param {Object} widgetContents - Contents of the widget to create
 */
function addWidget(widgetName, widgetContents) {
  addWidget.count = ++addWidget.count || 1;       // Like a static var
  let template = $.handlebarTemplates[widgetName]({
    'id': addWidget.count,
    'contents': widgetContents,
  });
  let widget = $(template).appendTo($('#widgets-holder'));
  widget.click(function() {
    activateFormPart($(this));
  });
  activateFormPart(widget);
  componentHandler.upgradeDom();
}

/**
 * Delete a widget from the form list
 * @param {int} id - Id of the widget to delete
 */
function deleteWidget(id) {
  $('#form-part-' + id).remove();
}

/**
 * Clone the last li element of the #choices-list-id, remove some attributes,
 * increment a counter for the name and id, and append it to the ul
 * @param {int} id - Id of the widget that will receive the new choice
 */
function addChoice(id) {
  let element = $('#choices-list-' + id + ' li:last-child').clone();
  let container = element.find('.mdl-textfield');
  let input = element.find('.mdl-textfield__input');
  let label = element.find('.mdl-textfield__label');
  let oldID = input.attr('id');
  let idPrefix = oldID.substring(0, oldID.lastIndexOf('-') + 1);
  let idSuffix = oldID.substring(oldID.lastIndexOf('-') + 1, oldID.length);
  idSuffix = parseInt(idSuffix) + 1;

  /* Remove any value that might have been inserted into the previous box */
  input.val('');

  /* Set new ids */
  input.attr('name', 'choice-' + idSuffix);
  input.attr('id', idPrefix + idSuffix);
  label.attr('for', idPrefix + idSuffix);

  /* Ask MDL to re-upgrade and add to dom */
  container.removeAttr('data-upgraded');
  container.removeClass('is-upgraded');
  element.appendTo($('#choices-list-' + id));
  componentHandler.upgradeDom();

  /* Turn on remove buttons */
  $('#choices-list-' + id).find('.delete-choice').removeAttr('disabled');
}

/**
 * Delete a choice from a widget
 * @param {Object} elem - The element to delete
 */
function deleteChoice(elem) {
  let choice = elem.parentNode.parentNode;
  /* Don't allow removing the last choice item */
  let siblings = $(choice).siblings();
  if (siblings.length > 0) {
    choice.remove();
  }
  if (siblings.length == 1) {
    siblings.find('.delete-choice').attr('disabled', '');
  }
}

/**
 * Delete a choice from a widget
 * @param {Array} array - The array to index
 * @return {Array} array - The indexed array
 */
function indexArray(array) {
  let indexedArray = {};
  $.map(array, function(n, i) {
    indexedArray[n['name']] = n['value'];
  });
  return indexedArray;
}

/**
 * Collect the widgets and submit them to the backend
 */
function submitForm() {
  let widgetForm = {'widgets': []};
  let i = 0;
  let csrfToken = $.cookie('csrftoken');
  $('#widgets-holder').find('form').each(function() {
    widgetForm.widgets[i++] = indexArray($(this).serializeArray());
  });
  widgetForm['meta'] = indexArray($('#form-title').serializeArray());
  widgetForm['options'] = indexArray($('#form-options').serializeArray());
  let data = {
    'csrfmiddlewaretoken': csrfToken,
    'data': JSON.stringify(widgetForm),
  };
  $.post($(location).attr('href'), data, function(response) {
    window.location.href = '/forms/view/list-forms';
  })
  .fail(function(jqXHR) {
    message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
  });
}

let templateList = [
  widgetPath + 'text.hbs',
  widgetPath + 'date.hbs',
  widgetPath + 'multifield.hbs',
  widgetPath + 'paragraph.hbs',
  widgetPath + 'boolean.hbs',
  widgetPath + 'scale.hbs',
  widgetPath + 'signature.hbs',
  widgetPath + 'instructions.hbs',
];

let partialList = [
  widgetPath + 'commonpartials.hbs',
];

$(function() {
  componentHandler.upgradeDom();
  $(document).autoBars({
    main_template_from_list: templateList,
    partial_template_from_list: partialList,
    callback: setupForm,
  });
});

/** Uses the form data to open the form for editing */
function setupForm() {
  Handlebars.registerHelper('if_eq', function(a, b, options) {
    if (a == b) {
      return options.fn(this);
    } else {
      return options.inverse(this);
    }
  });
  if (formData != '') {
    $('#form-name').val(formData.fields.name);
    $('#form-name')[0].parentElement.MaterialTextfield.checkValidity();
    $('#form-name')[0].parentElement.MaterialTextfield.checkDirty();
    $('#form-description').val(formData.fields.description);
    $('#form-description')[0].parentElement.MaterialTextfield.checkValidity();
    $('#form-description')[0].parentElement.MaterialTextfield.checkDirty();
    for (const widget of formData.fields.elements) {
      let type = widget.type;
      switch(widget.type) {
        case 'checkbox':
          type = 'multifield';
          break;
        case 'dropdown':
          type = 'multifield';
          break;
        case 'radio':
          type = 'multifield';
          break;
        case 'slider':
          type = 'scale';
          break;
        case 'stars':
          type = 'scale';
          break;
      }
      addWidget(type, widget);
    }
  }
}
