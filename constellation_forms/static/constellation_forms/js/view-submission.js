$('#visibility-toggle').change(function() {
  if (this.checked) {
    $('.log-private').hide(100);
  } else {
    $('.log-private').show(100);
  }
});


