#!/usr/bin/python3.6


timer_html = '''
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <title></title>
  <meta name="author" content="">
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">

</head>

<body>

<input id='time' type='number' value='120' onsubmit='void(0);'>
<input id='custom' type='text' value='' onsubmit='void(0);' placeholder="custom url">
<select id='sound'>
  <option value="https://sampleswap.org/samples-ghost/VOCALS and SPOKEN WORD/MALE MISC/79[kb]ah_yeah!.aif.mp3">Ah yea!</option>
  <option value="https://sampleswap.org/samples-ghost/VOCALS and SPOKEN WORD/MALE MISC/1143[kb]applause-thank-you.aif.mp3">applause thank you</option>
  <option value="https://sampleswap.org/samples-ghost/VOCALS and SPOKEN WORD/MALE MISC/154[kb]evil-wicked-spooky-laugh.wav.mp3">evil laugh</option>
  <option value="https://sampleswap.org/samples-ghost/VOCALS and SPOKEN WORD/MALE MISC/134[kb]what_time_is_it.aif.mp3">what time?</option>
  <option value="https://sampleswap.org/samples-ghost/VOCALS and SPOKEN WORD/silly lo-fidelity orgasms/43[kb]i_wanna_make_you_cum.aif.mp3">make you cum</option>
  <option value="http://fia4awagner.pythonanywhere.com/static/Lubeitup.mp3">lube it up</option>
  <option value="custom">custom</option>

</select>
<button onclick='startTimer()'>Start</button>
<hr>
<span id='timer' style='font-size:35vw;'>0:00</span>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script>
var secs=0;
function startTimer() {
	var timelimit = parseInt($('#time').val());
	var audio;

	if ($('#sound').val() == 'custom') {
		audio = new Audio($('#custom').val());
	} else {
		audio = new Audio($('#sound').val());
	}

	setInterval(function () {
		secs--;
		if (secs <= 0) {
			secs = timelimit;
			audio.play();
		}
		minutes = Math.floor(secs / 60);
		seconds = secs % 60;
		$('#timer').html(minutes + ':'+ (seconds<10 ? '0' : '') + seconds)
	}, 1000);
}
</script>
</body>

</html>
'''