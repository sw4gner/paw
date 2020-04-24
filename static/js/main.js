chartColors = {
"red": "rgb(255, 99, 132)",
"orange": "rgb(255, 159, 64)",
"yellow": "rgb(255, 205, 86)",
"green": "rgb(75, 192, 192)",
"blue": "rgb(54, 162, 235)",
"purple": "rgb(153, 102, 255)",
"grey": "rgb(201, 203, 207)"
};

chartColorsKeys = [
	"blue",
	"grey",
	"red",
	"orange",
	"green",
	"yellow",
	"purple",
];

colorArray = ['#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
        '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
        '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
        '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
        '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
        '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
        '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
        '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
        '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
        '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];


if (window.localStorage.getItem('offset')==null) {
    offset=Math.floor(Math.random()*colorArray.length);
    window.localStorage.setItem('offset', offset);
} else {
    offset=parseInt(window.localStorage.getItem('offset'));
}


function getColor(idx) {
    idx+=offset;
	return colorArray[idx%colorArray.length];
}

function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}