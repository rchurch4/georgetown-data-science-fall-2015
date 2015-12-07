// Annual Mean Rating
// TripAdvisor
// Version 1
// based on line graph tutorial: http://bl.ocks.org/d3noob/7030f35b72de721622b8


var year_tripadvisor_is_local = "local"

// Set the dimensions of the canvas / graph
var margin_year_tripadvisor = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin_year_tripadvisor.left - margin_year_tripadvisor.right,
    height = 270 - margin_year_tripadvisor.top - margin_year_tripadvisor.bottom;

// Parse the date / time
var parseDate_year_tripadvisor = d3.time.format("%Y").parse;

// Set the ranges
var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis_year_tripadvisor = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis_year_tripadvisor = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var valueline_year_tripadvisor = d3.svg.line()
    .x(function(d) { return x(d.year); })
    .y(function(d) { return y(d.mean_rating); });
    
// Adds the svg canvas
var svg_year_tripadvisor = d3.select("#line_graph_tripadvisor_year")
    .append("svg")
        .attr("width", width + margin_year_tripadvisor.left + margin_year_tripadvisor.right)
        .attr("height", height + margin_year_tripadvisor.top + margin_year_tripadvisor.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin_year_tripadvisor.left + "," + margin_year_tripadvisor.top + ")");

// Get the data
d3.tsv("tripadvisor_annual_local.tsv", function(error, data) {
    data.forEach(function(d) {
        d.year = parseDate_year_tripadvisor(d.year);
        d.mean_rating = +d.mean_rating;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.year; }));
    y.domain([3, 5]);

    // Add the valueline path.
    svg_year_tripadvisor.append("path")
        .attr("class", "line")
        .attr("d", valueline_year_tripadvisor(data));

    // Add the X Axis
    svg_year_tripadvisor.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis_year_tripadvisor);

    // Add the Y Axis
    svg_year_tripadvisor.append("g")
        .attr("class", "y axis")
        .call(yAxis_year_tripadvisor);

});



// ** Update data section (Called from the onclick)
function update_data_tripadvisor() {
	
	if (year_tripadvisor_is_local == "local") {
	// new	
	year_tripadvisor_is_local = "nonlocal"
	d3.select("#title_ratings_tripadvisor_year").text("Non-Local Reviewers")
		
    // Get the data again
    d3.tsv("tripadvisor_annual_nonlocal.tsv", function(error, data) {
       	data.forEach(function(d) {
	    	d.year = parseDate_year_tripadvisor(d.year);
	    	d.mean_rating = +d.mean_rating;
	    });

    	// Scale the range of the data again 
    	x.domain(d3.extent(data, function(d) { return d.year; }));
	    y.domain([3, 5]);

    // Select the section we want to apply our changes to
    var svg_year_tripadvisor = d3.select("#line_graph_tripadvisor_year").transition();

    // Make the changes
        svg_year_tripadvisor.select(".line")   // change the line
            .duration(750)
            .attr("d", valueline_year_tripadvisor(data));
        svg_year_tripadvisor.select(".x.axis") // change the x axis
            .duration(750)
            .call(xAxis_year_tripadvisor);
        svg_year_tripadvisor.select(".y.axis") // change the y axis
            .duration(750)
            .call(yAxis_year_tripadvisor);

    });		
	}
	else {
	// new
	year_tripadvisor_is_local = "local"
	d3.select("#title_ratings_tripadvisor_year").text("Local Reviewers")
	
    // Get the data again
    d3.tsv("tripadvisor_annual_local.tsv", function(error, data) {
       	data.forEach(function(d) {
	    	d.year = parseDate_year_tripadvisor(d.year);
	    	d.mean_rating = +d.mean_rating;
	    });

    	// Scale the range of the data again 
    	x.domain(d3.extent(data, function(d) { return d.year; }));
	    y.domain([3, 5]);

    // Select the section we want to apply our changes to
    var svg_year_tripadvisor = d3.select("#line_graph_tripadvisor_year").transition();

    // Make the changes
        svg_year_tripadvisor.select(".line")   // change the line
            .duration(750)
            .attr("d", valueline_year_tripadvisor(data));
        svg_year_tripadvisor.select(".x.axis") // change the x axis
            .duration(750)
            .call(xAxis_year_tripadvisor);
        svg_year_tripadvisor.select(".y.axis") // change the y axis
            .duration(750)
            .call(yAxis_year_tripadvisor);

    });		
	}
	

}
