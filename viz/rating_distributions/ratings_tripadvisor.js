// Ratings Distribution - Local vs. Non-local d3 Bar Graphs
// TripAdvisor
// Version 1.3

// References:
// 1) d3 bar graph template: http://bl.ocks.org/mbostock/3885304
// 1b) d3 bar graph tutorial: https://github.com/mbostock/d3/wiki/Selections#data
// 2) using a div container for svg: professor singh's js5.html example
// 3) updating d3 data: http://bl.ocks.org/d3noob/7030f35b72de721622b8
// 3b) updating d3 data: http://bl.ocks.org/RandomEtc/cff3610e7dd47bef2d01#index.html
// 4) meaning of "+" operator in javascript: http://stackoverflow.com/questions/26950879/d3-operator-before-object-call
// 5) understanding javascript: http://www.w3schools.com/js/
// 6) event listener for button: http://stackoverflow.com/questions/21685943/change-button-text-using-d3js

// set up svg	
var svg_tripadvisor_ratings = d3.select("#bar_graph_ratings_tripadvisor")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
// variable for alternating behavior
var current_tripadvisor_graph = "local";

// here we import the data and proceed with callback functions.
d3.tsv("ratings_local_tripadvisor.tsv", type, draw_tripadvisor);	

// finish bar graph
function draw_tripadvisor(error, data) {

	if (error) throw error;

	x.domain(data.map(function(d) { return d.rating; }));
	//y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
	y.domain([0, .45]);

	svg_tripadvisor_ratings.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	svg_tripadvisor_ratings.append("g")
		.attr("class", "y axis")
		.call(yAxis);
		
	svg_tripadvisor_ratings.append("text")
		.attr("class", "smalltext")
		.attr("transform", "rotate(-90)")
		.attr("y", 6)
		.attr("dy", ".71em")
		.style("text-anchor", "end")
		.text("Frequency");

	svg_tripadvisor_ratings.selectAll("bar")
		.data(data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("x", function(d) { return x(d.rating); })
		.attr("width", x.rangeBand())
		.attr("y", function(d) { return y(d.frequency); })
		.attr("height", function(d) { return height - y(d.frequency); });

}

// coerce frequency to numeric
function type(d) { 
  d.frequency = +d.frequency;
  return d;
}

// switches data of bar graph between local and non-local
function update_data_tripadvisor() {
	
	if (current_tripadvisor_graph=="local") {
		d3.tsv("ratings_nonlocal_tripadvisor.tsv", type, draw_new_tripadvisor);
		d3.select("#title_ratings_tripadvisor").text("Non-Local Reviewers")
		current_tripadvisor_graph="non-local";
	}
	else {
		d3.tsv("ratings_local_tripadvisor.tsv", type, draw_new_tripadvisor);
		d3.select("#title_ratings_tripadvisor").text("Local Reviewers")		
		current_tripadvisor_graph="local";
	}
	
}

// function that transitions to new bar graph
function draw_new_tripadvisor(error, data) {

	if (error) throw error;
	  
	x.domain(data.map(function(d) { return d.rating; }));
	//y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
	y.domain([0, .45]);

    // Select the section we want to apply our changes to
    var svg_tripadvisor_ratings = d3.select("#bar_graph_ratings_tripadvisor")  // .transition();
	
	var bars = svg_tripadvisor_ratings.selectAll(".bar")
		.data(data) 
		//.data(data, function(d) { return d.rating; }) 
		
	bars.exit()
		.transition()
		.duration(300)
		.attr("y", y(0))
		.attr("height", height - y(0))
		.style('fill-opacity', 1e-6)
		.remove();

	bars.enter().append("rect")
		.attr("class", "bar")
		.attr("y", y(0))
		.attr("height", height - y(0));

	bars.transition().duration(300)
		.attr("x", function(d) { return x(d.rating); }) 
		.attr("width", x.rangeBand()) 
		.attr("y", function(d) { return y(d.frequency); })
		.attr("height", function(d) { return height - y(d.frequency); }); 
	
}