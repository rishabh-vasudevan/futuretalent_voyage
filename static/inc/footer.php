
<!-- Footer Section -->
<footer>
	<div class="container">
		<p>© 2021 Voyage Rooms & Apartment. All Rights Reserved.</p>
	</div>
</footer>

<!-- Footer Section End -->

<!-- Jquery Library -->
<script src="js/jquery-3.6.0.min.js"></script>

<!-- Bootstrap Library JS -->
<script src="js/bootstrap.min.js"></script>

<!-- Image Slider JS -->
<script src="src/js/lightslider.js"></script> 
<script>
$(document).ready(function() {
    $('#image-gallery').lightSlider({
        gallery:true,
        item:1,
        thumbItem:9,
        slideMargin: 0,
        speed:800,
        auto:true,
        loop:true,
        onSliderLoad: function() {
            $('#image-gallery').removeClass('cS-hidden');
        }  
    });
});
</script>
</body>
</html>