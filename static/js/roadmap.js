const steps = document.querySelectorAll(".step");
const contents = document.querySelectorAll(".step-content");

const nextBtn = document.getElementById("next");
const prevBtn = document.getElementById("prev");

let current = 0;

function updateUI() {

    steps.forEach((step, index) => {
        step.classList.toggle("step-active", index <= current);
    });

    contents.forEach((content, index) => {
        content.classList.toggle("step-active", index === current);
    });

    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === contents.length - 1;
}

nextBtn.addEventListener("click", () => {

    if (current < contents.length - 1) {
        current++;
        updateUI();
    }

});

prevBtn.addEventListener("click", () => {

    if (current > 0) {
        current--;
        updateUI();
    }

});

updateUI();