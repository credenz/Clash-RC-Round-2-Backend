var countDownDate = new Date().getTime();

var x = setInterval(function () {

    var now = new Date().getTime();

    var remTime = countDownDate + 7200000 - now;
    var hours = Math.floor((remTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));


    var seconds = Math.floor((remTime / 1000) % 60);
    var minutes = Math.floor((remTime / 1000 / 60) % 60);

    if ((minutes > 0) || (seconds > 0) || (hours > 0)) {
        if (minutes < 10) {
            document.getElementById("min").innerHTML = "0" + minutes;
        }
        else {
            document.getElementById("min").innerHTML = minutes;
        }
        if (seconds < 10) {
            document.getElementById("sec").innerHTML = "0" + seconds;
        }
        else {
            document.getElementById("sec").innerHTML = seconds;

        }

        if (hours < 10) {
            document.getElementById("hour").innerHTML = "0" + hours;
        }
        else {
            document.getElementById("hour").innerHTML = hours;
        }
    }
    else if (minutes == 0 && seconds == 0 && hours==0) {
        document.getElementById("min").innerHTML = "0" + "0";
        document.getElementById("sec").innerHTML = "0" + "0";
        document.getElementById("hour").innerHTML = "0" + "0";

        document.getElementById("min").style.color = "#F32013";
        document.getElementById("sec").style.color = "#F32013";
        document.getElementById("hour").style.color = "#F32013";


    }
}, 1000);