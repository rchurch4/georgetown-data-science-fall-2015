// Ratings Distribution - Local vs. Non-local d3 Bar Graphs
// Global Variables
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

// global variables
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
	.ticks(10, "%")