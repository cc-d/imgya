function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
		var previews = document.getElementById('previews');

		var pDiv = document.createElement('div');
		pDiv.setAttribute('class', 'card preview-card')

    	iPreview = document.createElement('img');
    	iPreview.setAttribute('class', 'card-img-top');
    	iPreview.src = e.target.result;
    	mimetype = e.target.result.split(';')[0]
    	mimetype = mimetype.split(':')[1]

    	pDiv.append(iPreview);

    	var smallDiv = document.createElement('div');
    	smallDiv.setAttribute('class', 'card-footer');

    	var smallText = document.createElement('small');
    	smallText.setAttribute('class', 'text-muted');
    	smallText.innerHTML = mimetype;
    	smallDiv.append(smallText);
    	pDiv.append(smallDiv);

    	$('#previews').append(pDiv);
    }
    reader.readAsDataURL(input.files[0]);
  }
}

$(function(ready){
	$("#img-input").change(function() {
	  readURL(this);
	});
});