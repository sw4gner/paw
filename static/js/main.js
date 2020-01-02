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
]

function getColor(idx) {
	return chartColors[chartColorsKeys[idx%chartColorsKeys.length]]
}

function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}