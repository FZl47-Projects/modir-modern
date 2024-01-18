
// ------------------------- Otp resend timer and btn ------------------- //
const ResendBtn = document.getElementById("resendBtn");
const ResendTimer = document.getElementById("resendTimer");

let time = [0, 30, 0];
let valid_send = false;

function resendCode(e){
    e.preventDefault();

    if(valid_send) {
        fetch("/account/register/send-code/", {
        method: "GET",
        headers: {
          Accept: "application/json, text/plain, */*",
          "Content-Type": "application/json",
        },
      }).then((res) => function (){
          time = [0, 30, 0];
          valid_send = false;
          interval = setInterval(timer, 10);
      });
    }
}

function timer(){
    ResendTimer.innerHTML = "(" + time[0] + ":" + time[1] + ")";
    time[2]++;

    if(time[2] >= 100){
        time[2] = 0;
        --time[1];

        if(time[1] < 0) {
            --time[0];

            if(time[0] <= 0){
                clearInterval(interval);
                time[0] = 1; time[1] = 59; time[2] = 0;
                valid_send = true;

                ResendBtn.classList.remove('d-none');
            }

            time[1] = 59;
        }
    }
}

let interval = setInterval(timer, 10);
ResendBtn.addEventListener("click", resendCode);
