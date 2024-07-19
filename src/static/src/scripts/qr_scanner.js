import QrScanner from './libraries/qr-scanner.min.js';

$(document).ready(function() {
const video_elem = $('#qr-scanner-feed')

$('#qr_code_button').on('click', async function () {

	const qrScanner = new QrScanner(
			video_elem[0],
			result => {
				console.log(result.data)
				window.location = encodeURI(result.data)
				qrScanner.stop()
			},
			{ /* optional attributes */ },
	);

	qrScanner.start();
	$(this).addClass('hidden')
	$(video_elem).removeClass('hide-qr-scanner')

	qrScanner.hasFlash().then(hasFlash => {
		if(hasFlash) {
			$('#flash-toggle').removeClass('hidden');
		}
	});

	await new Promise(resolve => setTimeout(resolve, 15000));

	qrScanner.stop()
	$(video_elem).addClass('hide-qr-scanner')
	$(this).removeClass('hidden')
})
});
