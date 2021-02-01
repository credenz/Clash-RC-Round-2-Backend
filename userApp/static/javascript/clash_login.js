
     var nam2= document.getElementById('nameee2');
    var d2 = document.getElementById('nllll2');
    var a2 = document.getElementById('emailid2');
    var b2 = document.getElementById('labelemail2');
    var c2 = document.getElementById('labelcontact2');
    var con2 = document.getElementById('con1');
    var nam1= document.getElementById('nameee1');
    var d1 = document.getElementById('nllll1');
    var a1 = document.getElementById('emailid1');
    var b1 = document.getElementById('labelemail1');
    var c1 = document.getElementById('labelcontact1');
    var con1 = document.getElementById('con1');
    var tname = document.getElementById('tm');
    var tnamel = document.getElementById('tml');
    var pswd = document.getElementById('psw');
    var pswdl = document.getElementById('pswl');
    function validateEmail1(emailField){
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

        if (reg.test(emailField.value) == false) 
        {
            // alert('Invalid Email Address');
           a1.setCustomValidity('Enter Valid E-mail ID !');
            return false;
        }
        else{
            a1.setCustomValidity('');
        return true;
    }
}
function validateEmail2(emailField){
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

        if (reg.test(emailField.value) == false) 
        {
            // alert('Invalid Email Address');
           a2.setCustomValidity('Enter Valid E-mail ID !');
            return false;
        }
        else{
            a2.setCustomValidity('');
        return true;
    }
}
   

    function upe2(){
        b2.style.top= '-100px';
        b2.style.left='0px';
        b2.style.color='rgb(200, 223, 231)';
        b2.style.fontSize='18px';
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }

    }
    function upc2(){
        c2.style.top= '-100px';
        c2.style.left='0px';
        c2.style.color='rgb(200, 223, 231)';
        c2.style.fontSize='18px';
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }
    }

    function upt2() {
        d2.style.top= '-100px';
        d2.style.left='0px';
        d2.style.color='rgb(200, 223, 231)';
        d2.style.fontSize='18px';
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }
    }
    function upe1(){
        b1.style.top= '-100px';
        b1.style.left='0px';
        b1.style.color='rgb(200, 223, 231)';
        b1.style.fontSize='18px';
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }

    }
    function upc1(){
        c1.style.top= '-100px';
        c1.style.left='0px';
        c1.style.color='rgb(200, 223, 231)';
        c1.style.fontSize='18px';
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }
    }
    function upt1() {
        d1.style.top= '-100px';
        d1.style.left='0px';
        d1.style.color='rgb(200, 223, 231)';
        d1.style.fontSize='18px';
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }
    }
    function tmc() {
        tnamel.style.top= '-100px';
        tnamel.style.left='0px';
        tnamel.style.color='rgb(200, 223, 231)';
        tnamel.style.fontSize='18px';
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (pswd.value.length==0) {
            pswdl.style.top= '-65px';
            pswdl.style.fontSize='16px';
            pswdl.style.color='rgba(187, 199, 206, 0.685)';
        }
    }
    function ps() {
        pswdl.style.top= '-100px';
        pswdl.style.left='0px';
        pswdl.style.color='rgb(200, 223, 231)';
        pswdl.style.fontSize='18px';
        if (con2.value.length==0) {
            c2.style.top= '-65px';
            c2.style.fontSize='16px';
            c2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a2.value.length==0) {
            b2.style.top= '-65px';
            b2.style.fontSize='16px';
            b2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (con1.value.length==0) {
            c1.style.top= '-65px';
            c1.style.fontSize='16px';
            c1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam2.value.length==0) {
            d2.style.top= '-65px';
            d2.style.fontSize='16px';
            d2.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (a1.value.length==0) {
            b1.style.top= '-65px';
            b1.style.fontSize='16px';
            b1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (nam1.value.length==0) {
            d1.style.top= '-65px';
            d1.style.fontSize='16px';
            d1.style.color='rgba(187, 199, 206, 0.685)';
        }
        if (tname.value.length==0) {
            tnamel.style.top= '-65px';
            tnamel.style.fontSize='16px';
            tnamel.style.color='rgba(187, 199, 206, 0.685)';
        }
    }
