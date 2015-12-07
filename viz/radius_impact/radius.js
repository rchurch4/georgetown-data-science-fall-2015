// radius
yelp_mean_rating_text
//alert(radius_counter % 3)
radius_counter = 1

function change_radius() {
	
	//alert(radius_counter % 3)
	if (radius_counter % 4 == 1) {
		document.getElementById("radius_map").src="dc_10.jpg"
		document.getElementById("radius_text").innerHTML="Radius: 10 miles"
		document.getElementById("yelp_mean_rating_text").innerHTML="Yelp local mean rating: 3.71 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Yelp non-local mean rating: 3.81"
		document.getElementById("tripadvisor_mean_rating_text").innerHTML="TripAdvisor local mean rating: 4.01 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TripAdvisor non-local mean rating: 4.17"
	}
	else if (radius_counter % 4 == 2) {
		document.getElementById("radius_map").src="dc_30.jpg"
		document.getElementById("radius_text").innerHTML="Radius: 30 miles"	
		document.getElementById("yelp_mean_rating_text").innerHTML="Yelp local mean rating: 3.72 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Yelp non-local mean rating: 3.82"	
		document.getElementById("tripadvisor_mean_rating_text").innerHTML="TripAdvisor local mean rating: 4.02 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TripAdvisor non-local mean rating: 4.18"	
	}
	else if (radius_counter % 4 == 3) {
		document.getElementById("radius_map").src="dc_50.jpg"
		document.getElementById("radius_text").innerHTML="Radius: 50 miles"
		document.getElementById("yelp_mean_rating_text").innerHTML="Yelp local mean rating: 3.72 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Yelp non-local mean rating: 3.82"	
		document.getElementById("tripadvisor_mean_rating_text").innerHTML="TripAdvisor local mean rating: 4.03 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TripAdvisor non-local mean rating: 4.18"
	}
	else {
		document.getElementById("radius_map").src="dc_1000.jpg"
		document.getElementById("radius_text").innerHTML="Radius: 1000 miles"
		document.getElementById("yelp_mean_rating_text").innerHTML="Yelp local mean rating: 3.74 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Yelp non-local mean rating: 3.83"	
		document.getElementById("tripadvisor_mean_rating_text").innerHTML="TripAdvisor local mean rating: 4.14 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TripAdvisor non-local mean rating: 4.15"		
	}

	radius_counter += 1
}

